<!-- site:hide -->

<p align="center">
  <img src="docs/images/app-icon.svg" width="128" height="128" alt="字在的圖示">
</p>

<!-- /site:hide -->

<h1 align="center">ZiZai 字在輸入法</h1>

<p align="center">免費的 macOS／Windows／Linux／Android／iOS 中文輸入法</p>

「字在」是以大易輸入法的字根為基礎，依字的部件與筆順重新拆碼的中文字根輸入法，為正體中文（繁體）設計。內建字根表，裝好就能打字；也能匯入自己的 `.cin` 字根表、補字、改輸入碼。

想先看整體的樣子：[功能預覽影片（手繪動畫，約半分鐘）](https://youtu.be/HSc9Hmme0D4)。

## 下載

<p align="center">
  <a href="https://github.com/zizai-ime/zizai-ime/releases/download/v1.4.0/ZiZai-Mac-Universal-1.4.0.zip"><img src="docs/images/download-macos.svg" width="187" height="76" alt="下載字在（macOS 13 以上）"></a>
  <a href="docs/guide-windows.md#下載"><img src="docs/images/download-windows.svg" width="187" height="76" alt="下載字在（Windows 10、11）"></a>
  <a href="docs/guide-linux.md#下載與核對"><img src="docs/images/download-linux.svg" width="187" height="76" alt="下載字在（Linux，x86_64）"></a>
</p>

<p align="center">
  <a href="https://apps.apple.com/tw/app/%E5%AD%97%E5%9C%A8-%E4%B8%AD%E6%96%87%E8%BC%B8%E5%85%A5%E6%B3%95/id6821223548"><img src="docs/images/badge-app-store.svg" width="152" height="56" alt="在 App Store 下載字在（iPhone、iPad）"></a>&emsp;
  <a href="https://play.google.com/store/apps/details?id=studio.mosil.ime.zizai"><img src="docs/images/badge-google-play.png" width="188" height="56" alt="在 Google Play 下載字在（Android）"></a>
</p>

<p align="center">版本見下表｜<a href="https://github.com/zizai-ime/zizai-ime/releases">各版更新內容</a></p>

| 系統 | 版本 | 需求 | 安裝說明 |
|---|---|---|---|
| macOS | [1.4.0](https://github.com/zizai-ime/zizai-ime/releases/tag/v1.4.0) | macOS 13 以上，支援 Apple 晶片與 Intel | [安裝與使用](docs/guide-macos.md) |
| Windows | [1.4.0](https://github.com/zizai-ime/zizai-ime/releases/tag/v1.4.0) | Windows 10、11。64 位元與 32 位元的檔案不同，在安裝說明選 | [安裝與使用（Windows）](docs/guide-windows.md) |
| Linux | [1.4.0](https://github.com/zizai-ime/zizai-ime/releases/tag/v1.4.0) | x86_64。Ubuntu 24.04、26.04 與 Debian 13 用 `.deb` ，Fedora 43、44 用 `.rpm` ，其他發行版用 `.tar.gz` 。IBus 與 Fcitx5 都能用 | [安裝與使用（Linux）](docs/guide-linux.md) |
| Android | [1.1.0](https://play.google.com/store/apps/details?id=studio.mosil.ime.zizai)（1.4.0 審查中） | Android 8 以上 | 從 Google Play 安裝，打開字在照畫面上的步驟設定 |
| iPhone、iPad | [1.4.0](https://apps.apple.com/tw/app/%E5%AD%97%E5%9C%A8-%E4%B8%AD%E6%96%87%E8%BC%B8%E5%85%A5%E6%B3%95/id6821223548) | iOS 17、iPadOS 17 以上 | 從 App Store 安裝，打開字在照畫面上的步驟設定 |

Android 版 1.4.0 上架之前，Google Play 上的 1.1.0 只有大易；這一頁寫到 Android 的四種輸入法、注音打詞與動態字序，都是 1.4.0 的功能。

注音打詞 1.4.0 起五個平台都有；首碼聯想與字彙建議 macOS、Windows、Linux 版有，手機版（Android、iPhone、iPad）沒有。

Windows 版與 Linux 版還沒有數位簽章，安裝前請先照安裝說明核對 SHA-256。Windows 會跳出安全警告；開了「智慧型應用程式控制」或由公司、學校管理的電腦，可能裝不起來，或裝好了也用不了字在。

## 特色

- **內建字根表**：「字在自建字根表（依部件與筆順規則自建）」，收錄 7 萬多字，含 Unicode 擴充區的字（見備註）。輸入碼依全字庫的部件，以及該字的筆順重新拆字產生，有些字的拆法可能和你習慣的不同，可以在「字在設定」的「擴充字根表」分頁替這些字加上你習慣的輸入碼。
- **四種輸入法**：五個平台都有大易、倉頡、標準注音、倚天 26 鍵（標準注音的另一種鍵盤排列）四種輸入法：macOS 在輸入法選單切換，Windows 在工作列的「中」「英」按鈕按右鍵切換，Linux 在輸入法選單切換，手機長按鍵盤上的「英／中」鍵切換。標準注音 1.4.0 起可以打詞（五個平台都有）。見 [安裝與使用](docs/guide-macos.md#輸入法)。
- **三碼與四碼並存**：三碼（由四碼推導）和四碼都能直接打，不用切換。
- **推導二碼**（macOS、Windows、Linux）：大易的三碼、四碼字，也能用第一碼加最後一碼打出，排在原有的二碼字之後；不需要時可以在「字在設定」關閉。
- **注音打詞**（1.4.0 起，五個平台都有）：標準注音預設打詞，打第一個鍵就有候選，可以連打幾個字再選詞，也可以每個字只打聲母；選過的詞會往前排。想一個字一個字選，可以在「字在設定」（手機版是字在 App 的「打字方式」）切回逐字。倚天 26 鍵這一種排列，這一版還是逐字選字。見 [注音打詞](docs/guide-macos.md#注音打詞)。手機版的候選列分兩行，上面是詞、下面是第一個字的候選，見 [Android](docs/guide-android.md#注音打詞) 與 [iPhone、iPad](docs/guide-ios.md#注音打詞)。
- **首碼聯想與字彙建議**（1.4.0 起，macOS、Windows、Linux 版的大易與標準注音；標準注音打詞或逐字都有；手機版沒有）：送出一個字後，打下一個字的第一個鍵，游標旁會提示接在後面的詞；組字中按 Tab，只有一個詞就直接送出，兩個以上時在提示裡輪流選，按空白鍵送出，或直接打下一個字（首碼聯想，預設開啟）。也可以打開字彙建議：剛送出字、還沒打下一個字時，先用淡色顯示可能接著打的詞，用同樣的方式按 Tab 採用，建議顯示在游標旁的小窗；終端機這類 App 可以設成不顯示（預設關閉）。用這兩個功能送出的詞，之後也會往前排。詞庫收常用詞、教育部《國語辭典簡編本》《成語典》的詞條，以及國家教育研究院樂詞網各領域的名詞（在「字在設定」勾選要用的領域，預設只有高中以下的教科書名詞，勾得再多也不會拖慢）；大易、倚天、字在這類輸入法名稱也打得出來。字在與任何輸入法廠商沒有合作或隸屬關係，也未經其背書。見 [首碼聯想](docs/guide-macos.md#首碼聯想) 與 [字彙建議](docs/guide-macos.md#字彙建議)。
- **動態字序**（五個平台都有）：依你自己選過的字調整候選順序，選了才會換位。候選不論幾個，選過的字比前面的字常選得夠多就往前排；很久沒選的字會慢慢退回去。所有打法共用一份次數：在一種打法常選的字，在另一種打法選到時也會很快往前。macOS 版不想讓某一組換位，在候選字視窗按右鍵選「還原這組的順序」；手機版在候選列長按候選選「還原這組的順序」。標準注音打詞時（五個平台都有），選過的詞也會往前排。
- **資料更新**：字根表有更新時，在「字在設定」的首頁按「檢查更新」，下載資料更新檔，看過改了哪些字再套用，不必重裝字在。見 [安裝與使用](docs/guide-macos.md#版本與更新)。
- **擴充與自訂**：支援 `.cin` 格式，可以補字、自訂輸入碼、停用不要的字。請使用你有權使用的 `.cin` 檔，匯入的字根表只供你自己使用。除了由全字庫開放資料轉出的倉頡形碼表，「字在」不附、也不提供下載任何第三方的字根表檔案。
- **標點與符號**：按 `=` 再按一顆鍵，見 [符號字根表](docs/symbols.md)。
- **打字不連網**：輸入法本體沒有連網的功能，也不保存打字紀錄：動態字序在這台裝置上記下你選過的每個字詞各選了幾次（單字所有打法共用一份）與調整過的候選位置，不記句子、前後文、時間；手機版另把注音打詞時一個字一個字選出來、詞庫沒有的詞記進「我的詞庫（注音詞）」，可以關掉。首碼聯想與字彙建議只在打字當下看你剛送出的幾個字，不存下來。只有在「字在設定」按「檢查更新」或下載資料更新檔時，才會連到 GitHub，不會自動連網，也不會送出你的任何資料。不放廣告、沒有追蹤，見 [隱私權政策](PRIVACY.md)。

**備註**

1. Unicode 擴充區的字，大多要另外安裝全字庫字型才看得到，安裝方式見 [安裝與使用](docs/guide-macos.md#擴充區的字)。
2. 不安裝也沒關係，電腦原本的文字顯示不受影響；看不到的字，預設不會出現在候選字視窗。

## 安裝與使用

macOS 見 [安裝與使用](docs/guide-macos.md)，Windows 見 [安裝與使用（Windows）](docs/guide-windows.md)，Linux 見 [安裝與使用（Linux）](docs/guide-linux.md)。Android 與 iPhone、iPad 從 Google Play、App Store 安裝，打開字在照畫面上的步驟設定。

## 問題與建議

請到 [Issues](https://github.com/zizai-ime/zizai-ime/issues) 回報。Issues 是公開的，請不要貼上字根表內容、詞庫或打字內容。

## 使用條款與資料來源

「字在」是免費的中文輸入法，但目前沒有開放原始碼，<!-- site:hide -->使用條款見 [LICENSE.md](LICENSE.md)。這個儲存庫只放說明文件；<!-- /site:hide --><!-- site:show 見<a href="LICENSE.md">使用條款</a>。 -->安裝檔在 [Releases](https://github.com/zizai-ime/zizai-ime/releases)，資料更新檔在 [zizai-ime/zizai-data](https://github.com/zizai-ime/zizai-data/releases)。

內建字根表以大易輸入法的字根為基礎，拆字碼由程式依字在的取碼規則、全字庫的部件與筆順資料，以及人工指定與調整的字根清單產生，不是任何輸入法廠商的官方字根表。字在與任何輸入法廠商沒有合作或隸屬關係，也未經其背書。

**資料來源**

- 拆字資料：數位發展部，2026，「[CNS11643 中文標準交換碼全字庫](https://www.cns11643.gov.tw)」（屬性資料 20260805 版）。此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。政府資料開放授權條款： https://data.gov.tw/license
- 字頻：國家教育研究院〈民國112年語料字頻表〉（《解讀媒體字詞：新聞與社群媒體用語調查（112年）》附錄 1），只使用「字」與「字頻」兩欄。國家教育研究院未參與本產品，亦不代表其建議、認可或贊同。
- 詞與詞頻（1.4.0 起，注音打詞、首碼聯想與字彙建議；手機版只有注音打詞用的詞）：
  - 國家教育研究院「臺灣華語文能力基準」三等七級詞語表與通用詞頻表（[國家教育研究院華語文語料庫](https://coct.naer.edu.tw/page.jsp?ID=4)），依創用 CC「姓名標示 4.0 國際」（CC BY 4.0）授權條款使用，授權條款： https://creativecommons.org/licenses/by/4.0/deed.zh-hant 。只取詞語、注音與詞頻欄位，通用詞頻表取詞頻較高的詞，已經轉換成輸入法內部的格式。國家教育研究院未參與本產品，亦不代表其認可。
  - 教育部《[國語辭典簡編本](https://dict.concised.moe.edu.tw/)》與《[成語典](https://dict.idioms.moe.edu.tw/)》，著作人：教育部，依創用 CC「姓名標示－禁止改作 3.0 臺灣」（CC BY-ND 3.0 臺灣）授權條款使用，授權條款： https://creativecommons.org/licenses/by-nd/3.0/tw/ 。只取詞條與讀音兩個欄位，不含釋義、例句與其他內容。教育部未參與本產品，亦不代表其認可。
  - 國家教育研究院[樂詞網](https://terms.naer.edu.tw/)下載專區的詞彙包（教科書名詞、學術名詞、雙語詞彙與兩岸對照名詞），取得日期 2026-11-13，依國家教育研究院「[政府網站資料開放宣告](https://terms.naer.edu.tw/mysite/about/2/)」使用並註明出處；其中有些詞彙包是樂詞網收錄、以其他機關名義提供的名詞，一樣取自樂詞網並註明出處。另含[政府資料開放平臺](https://data.gov.tw/)上國家教育研究院的資料集（取得日期同上），此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。政府資料開放授權條款： https://data.gov.tw/license 。各資料集的顯名聲明見隨安裝檔附上的第三方授權聲明。只取中文名詞，已經篩選整理。國家教育研究院未參與本產品，亦不代表其認可。
  - twngrams（ https://huggingface.co/datasets/taiwan-corpora/twngrams ）的日常詞、使用的網站數與兩個詞前後相連的次數（字彙建議的排序用），以 CC0 1.0 釋出。
- 圖示裡的「字」：思源黑體 TC（SIL Open Font License 1.1）轉出的外框。
- 其他第三方元件的授權聲明隨安裝檔附上。

Apple 與 Apple 標誌是 Apple Inc. 在美國及其他國家和地區註冊的商標，App Store 是 Apple Inc. 的服務標誌。Google Play 和 Google Play 標誌是 Google LLC 的商標。

© 2026 字在開發小組
