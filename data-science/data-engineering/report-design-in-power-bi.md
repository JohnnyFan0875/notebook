# Report Design in Power BI

在 Power BI 裡，report design 不是把圖排漂亮而已。  
它更像是在決定：使用者先看到什麼、什麼資訊應該延後揭露、哪些互動值得保留，以及不同裝置上的閱讀路徑要怎麼成立。

如果 [Power BI Overview](power-bi-overview.md) 偏平台與基本工作流，這篇比較偏報表層的 UX 設計心法。

## Start with Audience, Not Visuals

這份課程一直在提醒同一件事：

- report design 先是 audience design
- 先想使用者要完成什麼，再決定版面與互動

很多報表做不好，不是因為少了一個 fancy visual，而是：

- 不知道主要讀者是誰
- 不知道他們第一眼最需要回答哪個問題
- 沒有根據閱讀情境安排資訊順序

所以設計前先問三件事通常很有幫助：

- 使用者最先要看的 KPI 是什麼
- 他接下來最可能追問哪個細節
- 他是在桌面、簡報，還是手機上閱讀

## Progressive Disclosure

這份課程最值得保留的概念，是 `progressive disclosure`。

可以先把它理解成：

- step-by-step sequencing of information
- 從 abstract 走到 specific
- 只有在使用者需要時才揭露更細節的資訊

這個心法很適合 Power BI，因為互動式報表本來就不是要一次把所有資訊攤平。

## Why It Matters

很多報表之所以難用，不是因為圖表種類錯，而是：

- 首頁就塞太多細節
- 使用者找不到下一步該點哪裡
- 摘要、探索、明細混在同一層

progressive disclosure 的目的，就是讓使用者先掌握整體，再逐步要求更細的資訊，而不是第一眼就被所有視覺化淹沒。

## Reading Patterns and Focal Flow

如果把報表看成閱讀介面，那 layout 不只是排版，而是在安排視線順序。

這份課程整理了幾種常見的閱讀動線：

- `Gutenberg layout`: 視線常從左上往右下移動
- `Z layout`: 適合資訊密度較低、希望用明確起點與終點帶動線的頁面
- `F layout`: 適合文字或清單比較多、使用者會先掃上方再往下找重點的頁面

Power BI 不需要死守某一種版型，但這些 pattern 很適合當作：

- 首屏 KPI 排序的參考
- slicer、標題、重點圖表的位置依據
- mobile layout 的資訊取捨準則

## Focal Points and the Rule of Thirds

課程還補了一個很實用的視覺心法：

- 每一個頁面都應該有明確 focal point
- 關鍵 visual 不應該和次要資訊搶同一層注意力

`rule of thirds` 可以把它當成簡單的構圖提醒：

- 不要把所有重要內容都機械式地塞在正中央
- 讓標題、主要 KPI、核心圖表落在更自然的視線停留區

對 BI 報表來說，這背後真正重要的不是美感，而是：

- 使用者能不能在幾秒內抓到這頁的主角
- 視線會不會被不重要的裝飾或次要圖表打斷

## Bookmarks, Selection Pane, and Buttons

在 Power BI 裡，要把 progressive disclosure 做出來，常見會用到三個元件：

- bookmarks
- selection pane
- buttons

它們可以組成一種「多狀態報表」：

- 用 bookmark 記住某個頁面狀態
- 用 selection pane 控制哪些 visuals 顯示或隱藏
- 用 buttons 讓使用者在不同狀態之間切換

這種做法的重點不是炫技，而是讓同一頁報表可以在摘要與細節之間切換，而不必永遠停留在單一靜態布局。

## What This Pattern Is and Is Not

課程對這點講得很清楚：

- 這不是單純 dashboard
- 也不是 pixel-perfect report

它更像是：

- 給使用者更多控制權
- 用互動切出不同資訊層次
- 讓有限空間承載更多有結構的內容

## Practical Caveat

如果用隱藏 / 顯示 visual 的方式設計狀態切換，要記得一個副作用：

- hiding visuals can reset filters

這代表互動設計不只要看畫面，也要考慮狀態切換後的 filter behavior 是否仍符合預期。

## Themes

報表設計的另一個核心層，是 `themes`。

theme 可以先理解成一組跨整份報表套用的 formatting defaults，包括：

- colors
- icon sets
- visual formats
- fonts
- sizes

它的價值在於讓你不用逐一修改每個 visual，也能維持一致的設計語言。

## Why Themes Matter

如果沒有 theme，報表常會出現：

- 同類視覺化顏色不一致
- 字級到處漂移
- 強調色與次要色沒有規則
- 新加 visual 時容易破壞整體風格

所以 theme 的目的不是裝飾，而是把視覺規則系統化。

## Themes as JSON

Power BI theme file 本質上是 `JSON`。

這很重要，因為它代表：

- theme 可以被版本化
- 可以只改局部設定
- 可以重複匯入不同報表

從 notebook 的角度看，這讓報表風格不只是 GUI 選項，而是某種可攜帶的設計設定檔。

## Editing Themes

常見的編修方式包括：

- 在 Power BI Desktop 用 `Customize current theme`
- 直接修改 JSON
- 用第三方工具協助生成或調整

如果只是微調，Desktop 介面通常夠用。  
如果要更系統化維護品牌色、字級或 visual defaults，直接管理 JSON 往往更穩。

## Importing and Exporting Themes

theme 也可以被匯入與匯出：

- import: `Browse for themes`
- export: `Save current theme`

這使 theme 很適合在多份報表之間共用，避免每一份報表都重新定義一次視覺風格。

## Theme Design Heuristics

這份課程有幾個很實用的設計提醒：

- 字體要夠大且容易讀
- 顏色要容易區分
- 要檢查是否對 color vision deficiency 友善
- 不要用太多顏色
- 第一主題色通常應該是 primary color

還有兩個很實務的取向：

- light themes 比較適合搭配較飽和的顏色
- dark themes 比較適合較亮的色調

一個簡化心法是：theme 不是顏色收藏，而是視覺優先順序系統。

## Accessibility Beyond Theme Colors

無障礙不是只靠挑一組安全配色就結束。  
更完整一點看，至少還包含：

- color usage
- contrast
- typography
- screen reader support
- alternative text

如果把 accessibility 放到報表最後才補，通常會變成局部修修補補。  
比較穩的做法，是一開始就把它當成 layout 與 visual encoding 的限制條件。

## Color Vision Deficiency

這份課程把 `color vision deficiency (CVD)` 當成報表設計的基本現實，而不是邊緣案例。

對 notebook 來說，最值得保留的不是各種類型的細分類表，而是這幾個設計結論：

- 不要假設所有使用者都能可靠分辨紅綠或藍色差異
- 盡量避免只靠顏色傳達狀態
- 同一視覺裡使用的顏色越少，辨識成本通常越低
- 選色時要實際檢查 palette 在 CVD 情境下是否仍可區分

## Better Color Usage

來源裡幾個很實用的提醒，可以直接記成 checklist：

- less is more
- 優先選擇不需要把顏色當唯一訊號的 visual
- 使用 CVD-friendly color palettes
- 除了顏色之外，再提供 shape、label、icon、position 等其他線索
- 可以用像 `Coblis` 這類模擬工具做快速檢查

如果某個圖表只有靠顏色才能知道差異，那通常代表它還不夠穩。

## Contrast, Fonts, and Backgrounds

除了顏色選得對，文字和背景之間也要有足夠對比。

課程提到的實務提醒包括：

- normal text 的 contrast ratio 至少約 `4.5:1`
- large text 可以放寬到約 `3:1`
- 背景圖片常會拉低可讀性與對比

所以在 Power BI 裡，背景不是不能用，而是要很克制。  
若背景開始和數值、標籤、座標軸搶注意力，通常就是該拿掉的訊號。

## Screen Readers and Alt Text

Power BI 的 accessibility 也包含 screen reader 使用情境。

值得保留的幾個重點是：

- 視覺物件要補 `alt text`
- alt text 可以是固定描述，也可以參考欄位值動態生成
- 能夠 `show data as table` 的 visual，對某些讀者更友善

同時也要知道限制：

- keyboard navigation 不是每個內容都很理想
- screen readers 不一定能完整讀出所有互動細節

所以如果某個 insight 很重要，不要只把它藏在複雜互動或純視覺編碼裡。

## Mobile Layout

Power BI 的 mobile design 不應該只是把桌面版縮小。  
手機版其實是一個不同的閱讀場景。

這也是為什麼 mobile layout 值得被單獨設計，而不是被視為桌面報表的副產品。

## What Mobile Layout Can Do

課程提到 mobile layout 常見能做的事情包括：

- 選擇哪些 visuals 要顯示
- 支援 drillthrough 到其他 report page
- 讓 slicers 與 cross-filter 繼續運作

這代表 mobile report 仍然保有互動性，而不是只能看靜態截圖。

## What Mobile Layout Cannot Do

同時也有限制：

- 不能直接在 mobile layout view 裡像桌面版那樣完整編輯
- 不能在那個視圖裡新增新的 visuals 或 shapes
- 桌面版被隱藏的 visuals 不會在 mobile layout 裡自動出現

這提醒我們：mobile layout 更像是挑選與重排既有內容，而不是重新做一份完全獨立的報表。

## Mobile Drillthrough and Bookmark Navigation

在行動裝置上，`drillthrough` 和 `bookmark navigator` 特別有價值。

它們的作用分別比較像：

- drillthrough: 讓使用者從摘要跳到特定情境的細節頁
- bookmark navigator: 用較明確的按鈕式導覽切換不同報表狀態或內容群組

這些能力很適合補足手機螢幕小、同頁可容納資訊少的限制。

## Best Practices for Mobile

課程裡最值得保留的 mobile 準則包括：

- 先放 key metrics
- 避免同一屏塞超過四個主要指標
- display units 要適度摘要
- measure names 需要時可以縮短
- 用清楚的 focal flow 排順序
- 可以用 `Z layout` 去安排閱讀動線
- 要考慮同一 visual 在 web 與 mobile 上的方向是否都合理

這些原則背後的共同邏輯是：

- 空間更少
- 注意力更分散
- 操作更依賴明確的導覽節點

所以 mobile report 通常更需要取捨，而不是更需要把桌面內容原封不動塞進去。

## Practical Heuristics

- 首頁先放摘要，再讓使用者主動要求明細。
- 先定義 audience 與第一個要回答的問題，再決定 visual 和版面。
- 用 `Gutenberg`、`Z`、`F` 這類閱讀動線檢查 focal flow 是否合理。
- 如果資訊有明顯層次，用 bookmarks + buttons + selection pane 做多狀態頁面通常比全部攤平更好。
- theme 要先服務一致性與可讀性，再談品牌感。
- 不要只靠顏色表達語意；至少再給一個 shape、label 或位置線索。
- 若用了背景圖、淡色字或花俏配色，記得回頭檢查 contrast。
- 重要 visual 補 `alt text`，並假設部分使用者會依賴螢幕閱讀輔助。
- 行動版不要只是縮小桌面頁；要重新決定什麼值得留下。
- 若某個 visual 在手機上不好讀，優先改 layout 或改 visual，而不是硬塞。

## Relation to Other Notes

- 如果你想先理解 Power BI 的平台工作流，可以先看 [Power BI Overview](power-bi-overview.md)。
- 如果你想看報表背後的模型層，接著看 [Semantic Models and Power BI](semantic-models-and-power-bi.md)。
- 如果你想看報表互動背後如何被 measures 與 context 驅動，接著看 [DAX in Power BI](dax-in-power-bi.md)。

## Mental Model

一句話總結：

Power BI 的 report design，可以先理解成用 `audience-aware sequencing + focal flow + accessible theming + device-aware layout` 把分析內容變成可使用的互動介面。
