#!/usr/bin/env python3
"""建置字在官網。

建置時讀儲存庫裡的 README.md、LICENSE.md、PRIVACY.md、docs/*.md 與 docs/images/，
套上 site/template.html，輸出到 --out（預設 _site/）。說明頁的內容不抄進 site/。

用法：python3 site/build.py [--out _site]
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
import sys
import tomllib
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from string import Template
from urllib.parse import quote, unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token

SITE_DIR = Path(__file__).resolve().parent
REPO = SITE_DIR.parent

ALERTS = {
    "NOTE": "備註",
    "TIP": "提示",
    "IMPORTANT": "重要",
    "WARNING": "警告",
    "CAUTION": "小心",
}
ALERT_RE = re.compile(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*(?:\n|$)")


@dataclass
class Page:
    source: str
    path: str
    title: str
    description: str
    nav: str | None
    template: str | None = None


@dataclass
class Config:
    site_url: str
    base_path: str
    site_name: str
    lang: str
    repo_url: str
    app_store_id: str
    og_image: str
    og_image_width: int
    og_image_height: int
    og_image_alt: str
    google_site_verification: str
    pages: list[Page]


def load_config() -> Config:
    raw = tomllib.loads((SITE_DIR / "site.toml").read_text(encoding="utf-8"))
    site_url = raw["site_url"]
    if not site_url.endswith("/"):
        site_url += "/"
    base_path = urlsplit(site_url).path or "/"
    pages = [
        Page(p["source"], p["path"], p["title"], p["description"], p.get("nav"),
             p.get("template"))
        for p in raw["pages"]
    ]
    return Config(
        site_url=site_url,
        base_path=base_path,
        site_name=raw["site_name"],
        lang=raw["lang"],
        repo_url=raw["repo_url"],
        app_store_id=str(raw["app_store_id"]),
        og_image=raw["og_image"],
        og_image_width=int(raw["og_image_width"]),
        og_image_height=int(raw["og_image_height"]),
        og_image_alt=raw["og_image_alt"],
        google_site_verification=raw.get("google_site_verification", "").strip(),
        pages=pages,
    )


# ---------- 標題錨點：照 GitHub 的做法 ----------


def github_slug(text: str) -> str:
    """GitHub 的標題錨點：轉小寫，只留字母、記號、數字、連接號、空白與「-」，空白換成「-」。"""
    out = []
    for ch in text.lower():
        cat = unicodedata.category(ch)
        if cat[0] in ("L", "M", "N") or cat == "Pc" or ch in (" ", "-"):
            out.append(ch)
    return "".join(out).replace(" ", "-")


def inline_text(token: Token) -> str:
    parts = []
    for child in token.children or []:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return "".join(parts)


def heading_ids(state) -> None:
    seen: dict[str, int] = {}
    tokens = state.tokens
    for i, tok in enumerate(tokens):
        if tok.type != "heading_open":
            continue
        slug = github_slug(inline_text(tokens[i + 1]))
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        tok.attrSet("id", slug if n == 0 else f"{slug}-{n}")


# ---------- GitHub 的提示框（> [!TIP]） ----------


def gh_alerts(state) -> None:
    tokens = state.tokens
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if (
            tok.type == "blockquote_open"
            and i + 2 < len(tokens)
            and tokens[i + 1].type == "paragraph_open"
            and tokens[i + 2].type == "inline"
        ):
            inline = tokens[i + 2]
            m = ALERT_RE.match(inline.content)
            if m:
                kind = m.group(1)
                tok.attrSet("class", f"markdown-alert markdown-alert-{kind.lower()}")
                inline.content = inline.content[m.end():]
                title = Token("html_block", "", 0)
                title.content = f'<p class="markdown-alert-title">{ALERTS[kind]}</p>\n'
                tokens.insert(i + 1, title)
                if not inline.content.strip():
                    # 標記自己一行、後面沒有字：拿掉空段落。
                    del tokens[i + 2 : i + 5]
        i += 1


def make_markdown() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": False})
    md.enable(["table", "strikethrough", "linkify"])
    md.core.ruler.after("block", "gh_alerts", gh_alerts)
    md.core.ruler.push("heading_ids", heading_ids)
    return md


# ---------- 連結改寫 ----------

ATTR_RE = re.compile(r'(\s(?:href|src)=)(["\'])(.*?)\2', re.S)


class LinkRewriter:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.by_source = {p.source: p for p in cfg.pages}
        self.errors: list[str] = []

    def page_url(self, page: Page) -> str:
        return self.cfg.base_path + page.path

    def resolve(self, source: str, url: str) -> str:
        url = html.unescape(url)
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or url.startswith("#") or url.startswith("//"):
            return url
        path = unquote(parts.path)
        frag = parts.fragment
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
        if target in self.by_source:
            new = self.page_url(self.by_source[target])
        elif target.startswith("docs/images/"):
            new = self.cfg.base_path + "images/" + quote(target[len("docs/images/"):])
        else:
            self.errors.append(f"{source}: 找不到連結的目標 {url}")
            return url
        if frag:
            new += "#" + frag
        return new

    def rewrite(self, source: str, body: str) -> str:
        def sub(m: re.Match) -> str:
            new = self.resolve(source, m.group(3))
            return f"{m.group(1)}{m.group(2)}{html.escape(new, quote=True)}{m.group(2)}"

        return ATTR_RE.sub(sub, body)


# ---------- 輸出 ----------


def wrap_tables(body: str) -> str:
    body = body.replace("<table>", '<div class="table-scroll"><table>')
    return body.replace("</table>", "</table></div>")


def nav_html(cfg: Config, current: Page | None) -> str:
    items = []
    for p in cfg.pages:
        if not p.nav:
            continue
        attr = ' aria-current="page"' if p is current else ""
        items.append(
            f'<li><a href="{html.escape(cfg.base_path + p.path)}"{attr}>{html.escape(p.nav)}</a></li>'
        )
    return "\n".join(items)


def json_ld(cfg: Config, page: Page) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "字在輸入法",
        "alternateName": "ZiZai",
        "description": page.description,
        "url": cfg.site_url,
        "image": cfg.site_url + "images/app-icon.svg",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "macOS, Windows, Linux, Android, iOS",
        "inLanguage": cfg.lang,
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TWD"},
        "author": {"@type": "Organization", "name": "字在開發小組"},
    }
    text = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{text}\n</script>'


SHOW_RE = re.compile(r"<!-- site:show (.*?) -->", re.S)
HIDE_RE = re.compile(r"<!-- site:hide -->.*?<!-- /site:hide -->\n?", re.S)


def site_markers(body: str) -> str:
    """README 裡給官網用的標記（HTML 註解，GitHub 上看不到）：
    site:hide 到 /site:hide 之間的內容官網不顯示；site:show 裡的 HTML 只在官網顯示。"""
    body = HIDE_RE.sub("", body)
    return SHOW_RE.sub(lambda m: m.group(1), body)


def render_html(cfg: Config, tpl: Template, page: Page, body: str, *,
                canonical: bool = True, current: Page | None = None,
                extra: list[str] | None = None, extra_body: str = "") -> str:
    is_home = page.path == ""
    full_title = page.title if is_home else f"{page.title}｜{cfg.site_name}"
    e = lambda s: html.escape(s, quote=True)  # noqa: E731
    url = cfg.site_url + page.path
    canonical_tags = (
        f'<link rel="canonical" href="{e(url)}">\n<meta property="og:url" content="{e(url)}">'
        if canonical else '<meta name="robots" content="noindex">'
    )
    return tpl.substitute(
        lang=e(cfg.lang),
        title=e(full_title),
        description=e(page.description),
        canonical_tags=canonical_tags,
        og_type="website" if is_home else "article",
        og_title=e(page.title),
        og_image=e(cfg.site_url + cfg.og_image),
        og_image_width=cfg.og_image_width,
        og_image_height=cfg.og_image_height,
        og_image_alt=e(cfg.og_image_alt),
        site_name=e(cfg.site_name),
        base=e(cfg.base_path),
        extra_head="\n".join(extra or []),
        extra_body=extra_body,
        nav=nav_html(cfg, current),
        body=body,
        page_class="home" if is_home else "doc",
        repo_url=e(cfg.repo_url),
        privacy_url=e(cfg.base_path + "privacy/"),
        terms_url=e(cfg.base_path + "terms/"),
    )


# ---------- 首頁專用範本（site/home.html） ----------
# 首頁的版面在 home.html；版本、下載連結、商店連結、需求與提醒都從 README 的「下載」節解析，
# 「問題與建議」「使用條款與資料來源」兩節照 README 轉出。以後只改 README 就能更新。

H2_SPLIT_RE = re.compile(r'(?=<h2 id=")')
H2_ID_RE = re.compile(r'<h2 id="([^"]+)"')
DL_LINK_RE = re.compile(
    r'<a href="[^"]+"><img src="[^"]*/images/([\w-]+)\.(?:svg|png)"[^>]*></a>')
ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<td>(.*?)</td>", re.S)
PARA_RE = re.compile(r"<p( align=\"center\")?>(.*?)</p>", re.S)

# 下載按鈕圖檔 → 版本表「系統」欄
DL_IMAGES = {
    "download-macos": "macOS",
    "download-windows": "Windows",
    "download-linux": "Linux",
    "badge-google-play": "Android",
    "badge-app-store": "iPhone、iPad",
}


# 版本表「系統」欄 → 下載區的分組
DESKTOP_SYSTEMS = ("macOS", "Windows", "Linux")
MOBILE_SYSTEMS = ("Android", "iPhone、iPad")
MOBILE_NOTE_RE = re.compile(r"[^。>]*Google Play、App Store[^。<]*。")


def readme_sections(body: str) -> dict[str, str]:
    """把轉好的 README 依 h2 切開：{標題錨點: 那一節的 HTML（含 h2）}。"""
    out = {}
    for part in H2_SPLIT_RE.split(body):
        m = H2_ID_RE.match(part)
        if m:
            out[m.group(1)] = part
    return out


def download_cards(cfg: Config, section: str) -> tuple[str, str, str, str]:
    """從 README「下載」節取電腦版與手機版的卡片、版本說明連結與提醒。
    分組依版本表的「系統」欄，不看列的順序；不認得的系統就建置失敗。"""
    buttons = {}
    for m in DL_LINK_RE.finditer(section):
        if m.group(1) in DL_IMAGES:
            buttons[DL_IMAGES[m.group(1)]] = m.group(0)
    by_nav = {p.nav: p for p in cfg.pages if p.nav}
    desktop, mobile = [], []
    for row in ROW_RE.findall(section):
        cells = CELL_RE.findall(row)
        if len(cells) < 3:
            continue  # 表頭
        system, version, need = (c.strip() for c in cells[:3])
        if system in DESKTOP_SYSTEMS:
            group = desktop
        elif system in MOBILE_SYSTEMS:
            group = mobile
        else:
            raise SystemExit(f"錯誤：README 版本表的系統「{system}」不屬於電腦版或手機版")
        if system not in buttons or system not in by_nav:
            raise SystemExit(f"錯誤：README 的下載節找不到「{system}」的下載按鈕或安裝說明頁")
        guide = html.escape(cfg.base_path + by_nav[system].path, quote=True)
        group.append(
            '<article class="dl-card reveal">\n'
            f'<h4>{system}</h4>\n'
            f'<p class="dl-version">版本 {version}</p>\n'
            f'<p class="dl-need">{need}</p>\n'
            f'<p class="dl-button">{buttons[system]}</p>\n'
            f'<p class="dl-guide"><a href="{guide}">安裝與使用</a></p>\n'
            '</article>'
        )
    if len(desktop) != len(DESKTOP_SYSTEMS) or len(mobile) != len(MOBILE_SYSTEMS):
        raise SystemExit(f"錯誤：README 的版本表解析出電腦版 {len(desktop)} 個、手機版 {len(mobile)} 個平台")
    links, notes = [], []
    for centered, inner in PARA_RE.findall(section):
        if "<img" in inner:
            continue
        if centered:
            links.extend(re.findall(r'<a href="[^"]+">[^<]*</a>', inner))
        else:
            notes.append(f"<p>{inner}</p>")
    return "\n".join(desktop), "\n".join(mobile), "\n".join(links), "\n".join(notes)


def render_home_body(cfg: Config, body: str, template: str) -> str:
    secs = readme_sections(body)
    try:
        dl, support, terms = secs["下載"], secs["問題與建議"], secs["使用條款與資料來源"]
        install = secs["安裝與使用"]
    except KeyError as exc:
        raise SystemExit(f"錯誤：README 少了「{exc.args[0]}」這一節") from None
    desktop, mobile, release_links, notes = download_cards(cfg, dl)
    m = MOBILE_NOTE_RE.search(install)
    if not m:
        raise SystemExit("錯誤：README「安裝與使用」節找不到手機版的安裝說明句")
    mobile_note = m.group(0).strip()
    tpl = Template((SITE_DIR / template).read_text(encoding="utf-8"))
    return tpl.substitute(
        base=html.escape(cfg.base_path, quote=True),
        desktop_cards=desktop,
        mobile_cards=mobile,
        mobile_note=mobile_note,
        release_links=release_links,
        download_notes=notes,
        support_section=support,
        terms_section=terms,
    )


def render_page(cfg: Config, md: MarkdownIt, rw: LinkRewriter, tpl: Template, page: Page) -> str:
    src = (REPO / page.source).read_text(encoding="utf-8")
    body = wrap_tables(rw.rewrite(page.source, site_markers(md.render(src))))
    extra = []
    extra_body = ""
    if page.template:
        body = render_home_body(cfg, body, page.template)
        stem = Path(page.template).stem
        extra.append(f'<link rel="stylesheet" href="{html.escape(cfg.base_path)}assets/{stem}.css">')
        extra_body = f'<script src="{html.escape(cfg.base_path)}assets/{stem}.js" defer></script>'
    if page.path == "":
        extra.append(f'<meta name="apple-itunes-app" content="app-id={cfg.app_store_id}">')
        if cfg.google_site_verification:
            # Search Console 的「HTML 標記」驗證：只放在首頁，驗證通過後要一直留著。
            extra.append('<meta name="google-site-verification" content="'
                         + html.escape(cfg.google_site_verification, quote=True) + '">')
        extra.append(json_ld(cfg, page))
    return render_html(cfg, tpl, page, body, current=page, extra=extra, extra_body=extra_body)


def render_404(cfg: Config, tpl: Template) -> str:
    """找不到網頁時 GitHub Pages 顯示的頁面。連結都用絕對路徑，在任何深度都能用。"""
    page = Page(source="", path="404.html", title="找不到這一頁",
                description="找不到這一頁。可以從首頁或各平台的安裝與使用找你要的內容。", nav=None)
    links = "\n".join(
        f'<li><a href="{html.escape(cfg.base_path + p.path)}">{html.escape(p.title)}</a></li>'
        for p in cfg.pages if p.nav
    )
    body = (
        "<h1>找不到這一頁</h1>\n"
        "<p>這個網址沒有網頁，可能是打錯了，或是網頁已經搬走。可以從下面的連結找你要的內容：</p>\n"
        f"<ul>\n{links}\n</ul>\n"
    )
    return render_html(cfg, tpl, page, body, canonical=False)


def write_sitemap(cfg: Config, out: Path) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in cfg.pages:
        lines.append(f"  <url><loc>{html.escape(cfg.site_url + p.path)}</loc></url>")
    lines.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {cfg.site_url}sitemap.xml\n", encoding="utf-8"
    )


def build(out: Path) -> list[str]:
    cfg = load_config()
    md = make_markdown()
    rw = LinkRewriter(cfg)
    tpl = Template((SITE_DIR / "template.html").read_text(encoding="utf-8"))

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(REPO / "docs" / "images", out / "images",
                    ignore=shutil.ignore_patterns(".DS_Store"))
    shutil.copytree(SITE_DIR / "static", out / "assets",
                    ignore=shutil.ignore_patterns(".DS_Store"))
    (out / ".nojekyll").write_text("", encoding="utf-8")

    written = []
    for page in cfg.pages:
        dest = out / page.path / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render_page(cfg, md, rw, tpl, page), encoding="utf-8")
        written.append(str(dest.relative_to(out)))
    (out / "404.html").write_text(render_404(cfg, tpl), encoding="utf-8")
    written.append("404.html")
    write_sitemap(cfg, out)

    if rw.errors:
        for err in rw.errors:
            print("錯誤：" + err, file=sys.stderr)
        raise SystemExit(1)
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description="建置字在官網")
    ap.add_argument("--out", default=str(REPO / "_site"), help="輸出資料夾（預設 _site/）")
    args = ap.parse_args()
    out = Path(args.out).resolve()
    for name in build(out):
        print(name)
    print(f"完成：{out}")


if __name__ == "__main__":
    main()
