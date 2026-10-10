<p align="center">
  <img src="docs/images/app-icon.svg" width="128" height="128" alt="字在的圖示">
</p>

<h1 align="center">ZiZai 字在輸入法</h1>

<p align="center">免費的 macOS／Windows 中文輸入法</p>

字在是以大易輸入法的拆碼規則為基礎的中文字根（形碼）輸入法，支援 macOS 與 Windows，為正體中文（繁體）設計。內建字根表，裝好就能打字；也可以匯入自己的 `.cin` 字根表、補字、改輸入碼。

## 下載

<p align="center">
  <a href="https://github.com/zizai-ime/zizai-ime/releases/download/v1.1.0/ZiZai-Mac-Universal-1.1.0.zip"><img src="docs/images/download-macos.svg" width="229" height="76" alt="下載字在（macOS 13 以上）"></a>
  <a href="https://github.com/zizai-ime/zizai-ime/releases/download/v1.1.0/ZiZai-Win-x64-1.1.0.zip"><img src="docs/images/download-windows-x64.svg" width="310" height="76" alt="下載字在（Windows 10、11，64 位元）"></a>
  <a href="https://github.com/zizai-ime/zizai-ime/releases/download/v1.1.0/ZiZai-Win-x86-1.1.0.zip"><img src="docs/images/download-windows-x86.svg" width="310" height="76" alt="下載字在（Windows 10，32 位元）"></a>
</p>

<p align="center">版本 1.1.0｜發布日期 <發布當天填>｜<a href="https://github.com/zizai-ime/zizai-ime/releases/tag/v1.1.0">更新內容與 SHA-256</a></p>

- **macOS**：macOS 13 以上，支援 Apple 晶片與 Intel。下載後解壓縮，按兩下 `ZiZai.pkg` 安裝，見 [安裝與使用](docs/安裝與使用.md)。
- **Windows**：Windows 10、11，64 位元或 32 位元，下載的檔案不同；不知道是哪一種，見 [安裝與使用（Windows）](docs/安裝與使用（Windows）.md) 的系統需求。安裝程式與輸入法還沒有數位簽章：Windows 會跳出安全警告，請先照說明核對 SHA-256，再決定要不要安裝；「智慧型應用程式控制」開著的電腦，或公司、學校管理的電腦，可能裝不起來，或裝好了也載入不了字在。

## 特色

- **內建字根表**：「字在自建字根表（依規則自建，非官方）」，收錄 7 萬多字，包含 Unicode 擴充區。擴充區的字要另外安裝全字庫字型才看得到，見 [安裝與使用](docs/安裝與使用.md#擴充區的字)。內建字根表的輸入碼，是依全字庫的部件與筆順重新產生的，所以有些字的拆法可能和你習慣的不同。需要的話，可以在「字在設定」的「擴充字根表」分頁，替這些字加上你習慣的輸入碼。
- **三碼與四碼並存**：三碼（推導，非官方）和四碼不用切換。
- **資料更新**：字根表改好之後，不必重新安裝字在：在「字在設定」的首頁按「檢查更新」，下載資料更新包，看過改了哪些字再換上。見 [安裝與使用](docs/安裝與使用.md#版本與更新)。
- **擴充與自訂**：支援 `.cin` 格式（OpenVanilla、PIME、hime 等輸入法使用的碼表格式），可以補字、自訂輸入碼、停用不要的字。請使用你有權使用的 `.cin` 檔，匯入的字根表只供你自己使用。字在不附、也不提供下載任何第三方的字根表檔案。
- **標點與符號**：按 `=` 再按一顆鍵，見 [符號字根表](docs/符號字根表.md)。
- **不連網的輸入法**：輸入法本體不含任何連網程式，預設不記錄打字內容；「字在設定」只在你按「檢查更新」或下載資料更新包時，才連到 GitHub。不放廣告、沒有追蹤。見 [隱私權政策](PRIVACY.md)。

## 安裝與使用

macOS 見 [安裝與使用](docs/安裝與使用.md)，Windows 見 [安裝與使用（Windows）](docs/安裝與使用（Windows）.md)。

## 問題與建議

請到 [Issues](https://github.com/zizai-ime/zizai-ime/issues) 回報。Issues 是公開的，請不要貼上字根表內容、詞庫或打字內容。

## 使用條款與資料來源

字在免費，但不開放原始碼，使用條款見 [LICENSE.md](LICENSE.md)。這個儲存庫只放說明文件，安裝檔放在 [Releases](https://github.com/zizai-ime/zizai-ime/releases)，資料更新包放在 [zizai-ime/zizai-data](https://github.com/zizai-ime/zizai-data/releases)。

內建字根表以大易輸入法的拆碼規則為基礎，碼由程式依字在的取碼規則、全字庫的部件與筆順資料，以及人工指定與調整的字根清單產生，不是任何輸入法廠商的官方字根表。

**資料來源**

- 拆字資料：數位發展部，2026，「[CNS11643 中文標準交換碼全字庫](https://www.cns11643.gov.tw)」（屬性資料 20260805 版）。此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。政府資料開放授權條款： https://data.gov.tw/license
- 字頻：國家教育研究院〈民國112年語料字頻表〉（《解讀媒體字詞：新聞與社群媒體用語調查（112年）》附錄 1），只使用「字」與「字頻」兩欄。國家教育研究院未參與本產品，亦不代表其建議、認可或贊同。
- 圖示裡的「字」：思源黑體 TC（SIL Open Font License 1.1）轉出的外框。
- 其他第三方元件的授權聲明隨安裝檔附上。

© 2026 字在開發小組
