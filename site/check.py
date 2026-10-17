#!/usr/bin/env python3
"""檢查建好的官網：每頁的標頭、站內連結與錨點、不向第三方發請求、sitemap 與 robots。

用法：python3 site/check.py [_site]
有任何問題就印出來並以 1 結束。
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE_DIR = Path(__file__).resolve().parent


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.title = ""
        self._in_title = False
        self.meta: dict[str, list[str]] = {}
        self.links: list[tuple[str, str]] = []  # (tag.attr, url)
        self.canonical: list[str] = []
        self.jsonld: list[str] = []
        self._in_jsonld = False
        self._buf = ""
        self.styles: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta.setdefault(key, []).append(a.get("content", ""))
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canonical.append(a.get("href", ""))
            else:
                self.links.append(("link.href", a.get("href", "")))
        if tag == "a" and "href" in a:
            self.links.append(("a.href", a["href"]))
        for attr in ("src", "srcset", "poster", "data"):
            if attr in a and tag != "a":
                self.links.append((f"{tag}.{attr}", a[attr]))
        if tag == "script":
            if a.get("type") == "application/ld+json":
                self._in_jsonld = True
                self._buf = ""
            else:
                self.links.append(("script", a.get("src", "(內嵌)")))
        if tag == "style":
            self._in_style = True
            self._buf = ""
        if "style" in a:
            self.styles.append(a["style"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_jsonld:
            self.jsonld.append(self._buf)
            self._in_jsonld = False
        if tag == "style" and self._in_style:
            self.styles.append(self._buf)
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld or self._in_style:
            self._buf += data


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else SITE_DIR.parent / "_site").resolve()
    cfg = tomllib.loads((SITE_DIR / "site.toml").read_text(encoding="utf-8"))
    site_url = cfg["site_url"].rstrip("/") + "/"
    base = urlsplit(site_url).path
    errors: list[str] = []

    pages: dict[str, PageParser] = {}
    for f in sorted(out.rglob("*.html")):
        p = PageParser()
        p.feed(f.read_text(encoding="utf-8"))
        pages[str(f.relative_to(out))] = p

    def local_file(path: str) -> Path | None:
        if not path.startswith(base):
            return None
        rel = unquote(path[len(base):])
        target = out / rel
        if rel == "" or rel.endswith("/"):
            target = target / "index.html"
        return target

    # V2 每頁的標頭
    titles: dict[str, str] = {}
    descs: dict[str, str] = {}
    for name, p in pages.items():
        t = p.title.strip()
        d = (p.meta.get("description") or [""])[0].strip()
        if not t:
            errors.append(f"{name}: 沒有 <title>")
        if not d:
            errors.append(f"{name}: 沒有摘要")
        if len(p.canonical) != 1 or not p.canonical[0].startswith(site_url):
            errors.append(f"{name}: canonical 不對：{p.canonical}")
        for key in ("og:title", "og:description", "og:url", "og:image"):
            if not p.meta.get(key):
                errors.append(f"{name}: 沒有 {key}")
        if t in titles:
            errors.append(f"{name}: <title> 和 {titles[t]} 重複")
        if d in descs:
            errors.append(f"{name}: 摘要和 {descs[d]} 重複")
        titles[t] = name
        descs[d] = name

    home = pages.get("index.html")
    if home is None:
        errors.append("沒有首頁")
    else:
        if not home.meta.get("apple-itunes-app") or "app-id=" not in home.meta["apple-itunes-app"][0]:
            errors.append("首頁沒有 Smart App Banner")
        found = False
        for raw in home.jsonld:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"首頁的結構化資料不是正確的 JSON：{exc}")
                continue
            if data.get("@type") == "SoftwareApplication":
                found = True
        if not found:
            errors.append("首頁沒有 SoftwareApplication 結構化資料")

    # V3 站內連結、錨點、圖片；V4 不向第三方發請求
    checked = 0
    for name, p in pages.items():
        for kind, url in p.links:
            parts = urlsplit(url)
            external = bool(parts.scheme or parts.netloc)
            if external:
                if kind != "a.href":
                    errors.append(f"{name}: {kind} 指到站外：{url}")
                continue
            if kind == "script":
                errors.append(f"{name}: 有 <script>：{url}")
                continue
            checked += 1
            if url.startswith("#"):
                target_page = p
                frag = url[1:]
            else:
                target = local_file(parts.path)
                if target is None:
                    errors.append(f"{name}: 連結不在基本路徑底下：{url}")
                    continue
                if not target.exists():
                    errors.append(f"{name}: 壞連結：{url}")
                    continue
                frag = parts.fragment
                target_page = pages.get(str(target.relative_to(out))) if target.suffix == ".html" else None
            if frag:
                frag = unquote(frag)
                if target_page is None or frag not in target_page.ids:
                    errors.append(f"{name}: 找不到錨點：{url}")
        for css in p.styles:
            for u in re.findall(r"url\(\s*['\"]?([^'\")]+)", css):
                if urlsplit(u).scheme or u.startswith("//"):
                    errors.append(f"{name}: 樣式的 url() 指到站外：{u}")

    for css_file in out.rglob("*.css"):
        text = css_file.read_text(encoding="utf-8")
        for u in re.findall(r"url\(\s*['\"]?([^'\")]+)", text):
            if urlsplit(u).scheme or u.startswith("//"):
                errors.append(f"{css_file.name}: url() 指到站外：{u}")
        if "@import" in text:
            errors.append(f"{css_file.name}: 有 @import")

    # V6 sitemap 與 robots
    sitemap = (out / "sitemap.xml").read_text(encoding="utf-8") if (out / "sitemap.xml").exists() else ""
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
    expected = {site_url + pg["path"] for pg in cfg["pages"]}
    if set(locs) != expected:
        errors.append(f"sitemap.xml 的網址不對：多了 {set(locs) - expected}，少了 {expected - set(locs)}")
    robots = (out / "robots.txt").read_text(encoding="utf-8") if (out / "robots.txt").exists() else ""
    if f"Sitemap: {site_url}sitemap.xml" not in robots:
        errors.append("robots.txt 沒有指到 sitemap")

    print(f"頁面 {len(pages)} 個；站內連結、錨點與圖片 {checked} 個；sitemap {len(locs)} 個網址")
    for e in errors:
        print("問題：" + e)
    print("問題：0 個" if not errors else f"問題：{len(errors)} 個")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
