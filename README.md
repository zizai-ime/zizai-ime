<p align="center">
  <img src="docs/images/app-icon.svg" width="128" height="128" alt="字在的圖示">
</p>

<h1 align="center">ZiZai 字在輸入法</h1>

<p align="center">免費的 macOS／Windows／Linux 中文輸入法</p>

「字在」是以大易輸入法的字根為基礎，依字的部件與筆順重新拆碼的中文字根輸入法，為正體中文（繁體）設計。內建字根表，裝好就能打字；也能匯入自己的 `.cin` 字根表、補字、改輸入碼。

## 下載

<p align="center">
  <a href="https://github.com/zizai-ime/zizai-ime/releases/download/v1.1.0/ZiZai-Mac-Universal-1.1.0.zip"><img src="docs/images/download-macos.svg" width="187" height="76" alt="下載字在（macOS 13 以上）"></a>
  <a href="docs/安裝與使用（Windows）.md#下載"><img src="docs/images/download-windows.svg" width="187" height="76" alt="下載字在（Windows 10、11）"></a>
  <a href="docs/安裝與使用（Linux）.md#下載與核對"><img src="docs/images/download-linux.svg" width="187" height="76" alt="下載字在（Linux，x86_64）"></a>
</p>

<p align="center">版本 1.1.0｜發布日期 2026-10-11｜<a href="https://github.com/zizai-ime/zizai-ime/releases/tag/v1.1.0">更新內容與 SHA-256</a>｜<a href="https://github.com/zizai-ime/zizai-ime/releases">各版更新內容</a></p>

| 系統 | 需求 | 安裝說明 |
|---|---|---|
| macOS | macOS 13 以上，支援 Apple 晶片與 Intel | [安裝與使用](docs/安裝與使用.md) |
| Windows | Windows 10、11。64 位元與 32 位元的檔案不同，在安裝說明選 | [安裝與使用（Windows）](docs/安裝與使用（Windows）.md) |
| Linux | x86_64。Ubuntu 24.04、26.04 與 Debian 13 用 `.deb` ，Fedora 43、44 用 `.rpm` ，其他發行版用 `.tar.gz` 。IBus 與 Fcitx5 都能用 | [安裝與使用（Linux）](docs/安裝與使用（Linux）.md) |

Windows 版與 Linux 版還沒有數位簽章，安裝前請先照安裝說明核對 SHA-256。Windows 會跳出安全警告；開了「智慧型應用程式控制」或由公司、學校管理的電腦，可能裝不起來，或裝好了也用不了字在。

## 特色

- **內建字根表**：「字在自建字根表（依部件與筆順規則自建）」，收錄 7 萬多字，含 Unicode 擴充區的字（見備註）。輸入碼依全字庫的部件，以及該字的筆順重新拆字產生，有些字的拆法可能和你習慣的不同，可以在「字在設定」的「擴充字根表」分頁替這些字加上你習慣的輸入碼。
- **三碼與四碼並存**：三碼（由四碼推導）和四碼都能直接打，不用切換。
- **資料更新**：字根表有更新時，在「字在設定」的首頁按「檢查更新」，下載資料更新檔，看過改了哪些字再套用，不必重裝字在。見 [安裝與使用](docs/安裝與使用.md#版本與更新)。
- **擴充與自訂**：支援 `.cin` 格式，可以補字、自訂輸入碼、停用不要的字。請使用你有權使用的 `.cin` 檔，匯入的字根表只供你自己使用。「字在」不附、也不提供下載任何第三方的字根表檔案。
- **標點與符號**：按 `=` 再按一顆鍵，見 [符號字根表](docs/符號字根表.md)。
- **打字不連網**：輸入法本體沒有連網的功能，預設不記錄打字內容。只有在「字在設定」按「檢查更新」或下載資料更新檔時，才會連到 GitHub，不會自動連網，也不會送出你的任何資料。不放廣告、沒有追蹤，見 [隱私權政策](PRIVACY.md)。

**備註**

1. Unicode 擴充區的字，大多要另外安裝全字庫字型才看得到，安裝方式見 [安裝與使用](docs/安裝與使用.md#擴充區的字)。
2. 不安裝也沒關係，電腦原本的文字顯示不受影響；看不到的字，預設不會出現在候選字視窗。

## 安裝與使用

macOS 見 [安裝與使用](docs/安裝與使用.md)，Windows 見 [安裝與使用（Windows）](docs/安裝與使用（Windows）.md)，Linux 見 [安裝與使用（Linux）](docs/安裝與使用（Linux）.md)。

## 問題與建議

請到 [Issues](https://github.com/zizai-ime/zizai-ime/issues) 回報。Issues 是公開的，請不要貼上字根表內容、詞庫或打字內容。

## 使用條款與資料來源

「字在」是免費的中文輸入法，但目前沒有開放原始碼，使用條款見 [LICENSE.md](LICENSE.md)。這個儲存庫只放說明文件；安裝檔在 [Releases](https://github.com/zizai-ime/zizai-ime/releases)，資料更新檔在 [zizai-ime/zizai-data](https://github.com/zizai-ime/zizai-data/releases)。

內建字根表以大易輸入法的字根為基礎，拆字碼由程式依字在的取碼規則、全字庫的部件與筆順資料，以及人工指定與調整的字根清單產生，不是任何輸入法廠商的官方字根表。

**資料來源**

- 拆字資料：數位發展部，2026，「[CNS11643 中文標準交換碼全字庫](https://www.cns11643.gov.tw)」（屬性資料 20260805 版）。此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。政府資料開放授權條款： https://data.gov.tw/license
- 字頻：國家教育研究院〈民國112年語料字頻表〉（《解讀媒體字詞：新聞與社群媒體用語調查（112年）》附錄 1），只使用「字」與「字頻」兩欄。國家教育研究院未參與本產品，亦不代表其建議、認可或贊同。
- 圖示裡的「字」：思源黑體 TC（SIL Open Font License 1.1）轉出的外框。
- 其他第三方元件的授權聲明隨安裝檔附上。

© 2026 字在開發小組
