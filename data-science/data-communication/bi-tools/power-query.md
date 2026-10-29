[Data Communication](../README.md) › [BI 工具](README.md) › Power Query

# Power Query

Power Query 是 Power BI（以及 Excel、Fabric Dataflows）的資料擷取與清理層：連接資料來源、選擇儲存模式，並把每一步轉換記成可重跑的 Applied Steps（底層是 M 語言）。很多看起來像視覺化或 DAX 的問題，根源其實在這一層：來源選錯、儲存模式不合適、重新整理不穩、gateway 或認證沒設好。模型與計算見 [Power BI 模型與 DAX](power-bi-modeling-and-dax.md)。

## Desktop 與 Service 的分工

| | Power BI Desktop | Power BI Service |
| --- | --- | --- |
| 角色 | 作者端：載入、轉換、建模、做報表 | 雲端：發布、分享、排程重新整理、gateway、權限 |
| 連線設定 | 本機能開就好 | 還要設定認證、gateway、重新整理排程才能穩定運作 |

## 資料來源與儲存模式

來源包括資料庫、CSV / Excel、web service、data lake，也可分成內部資料（營運與交易的事實）與外部資料（市場、人口、地理等比較脈絡）。

| 儲存模式 | 行為 | 優點 | 代價 | 適合 |
| --- | --- | --- | --- | --- |
| Import | 把資料載入 Power BI 模型 | 完整的轉換與 DAX 功能、查詢快 | 新鮮度依賴重新整理；資料大時模型與重新整理成本高 | 多數情境的預設 |
| DirectQuery | 不載入資料，每次互動時向來源查詢 | 資料不必匯入、較即時 | 效能取決於來源資料庫；部分轉換與 DAX 受限 | 資料量很大、需要近即時、來源支援 |
| Live connection | 連到已發布的 semantic model 或 Analysis Services | 多份報表共用同一個集中模型 | 本地幾乎無法改模型 | 組織已有集中管理的模型 |
| Composite / Dual | 同一模型混用 Import 與 DirectQuery | 熱資料即時、歷史資料匯入 | 設計較複雜 | 大型模型最佳化 |

Microsoft Fabric 另有 Direct Lake 模式，直接讀 OneLake 中的 Delta 表。選擇順序：需要完整轉換與建模彈性 → 先想 Import；資料量很大且來源撐得住 → DirectQuery；已有集中模型 → Live。DirectQuery 不是「比較進階」，而是用更高的上游耦合換取更少的匯入負擔。

## 參數與增量重新整理

Parameter（有名稱、值、型別）把伺服器、資料庫、日期範圍等會變的值抽出來，用於篩選、自訂函式輸入、切換資料來源（dev / prod）。

增量重新整理 (incremental refresh) 只重新整理新增或變動的部分，舊資料保留或封存，適合大型歷史資料、變動集中在近期的情境，可縮短重新整理時間、減少資料庫負擔。它需要：

| 依賴 | 說明 |
| --- | --- |
| `RangeStart` / `RangeEnd` 參數 | 名稱固定、型別為 date/time，用來篩選日期欄 |
| 可摺疊的查詢 (query folding) | 篩選要能推回來源執行，否則每次仍讀全部資料 |
| Service 端設定 | 重新整理政策、授權等級 |
| Gateway | 來源在地端時，Service 要透過 on-premises data gateway 存取 |

重新整理問題通常不是單純模型問題，而是 Desktop、Service、來源系統與 gateway 一起組成的部署問題。

## 效能

| 做法 | 理由 |
| --- | --- |
| 匯入前移除不需要的列與欄 | 模型越小，重新整理越快、DAX 越快 |
| 選對型別（整數 key、date 而非 datetime） | 壓縮率高 |
| 先 group / summarize 到需要的 grain | 不要背著不會用到的明細 |
| 保持 query folding | 轉換推回來源資料庫執行；可在步驟上按右鍵看「檢視原生查詢」 |
| DirectQuery：限制平行查詢、寫有效率的 SQL、建索引、只取需要的欄列 | 瓶頸常在上游資料庫 |

近即時需求可用自動頁面重新整理 (automatic page refresh，只適用 DirectQuery 來源) 或變更偵測 (change detection，追蹤某個 measure 有變化時才重新查詢)。間隔要配合資料實際到達的頻率：上游每 15 分鐘才更新，頁面每秒查一次只會增加負擔。每個開著報表的使用者都可能各自觸發查詢；可用頻率也受 capacity 與授權限制。用 Performance Analyzer 檢查每次查詢成本。

## 資料準備

```
連接資料 → 開啟 Power Query → 確認型別與欄名 → 用預覽功能檢查品質 → 文字 / 數值 / 日期轉換 → Close & Apply
```

Applied Steps 的價值在於：每次重新整理都重新套用同樣的步驟，清理流程可以檢查、調整與重跑，比在 Excel 手動改值更接近可重現的 pipeline。

| 乾淨資料的條件 | 不乾淨時的後果 |
| --- | --- |
| 型別正確（數值、日期 / 時間、文字、邏輯） | 日期被當文字 → 排序與日期函式失效；數值被當文字 → 無法聚合；類別代碼被當數值 → 被誤算平均 |
| 缺值已辨識、錯字與輸入錯誤已修正 | 篩選與分組分散 |
| 重複資料已處理 | 指標被放大 |
| 無關資料已排除、離群值已檢查 | 模型變大、結果偏移 |
| 欄名與表名簡短可讀 | DAX 與 Q&A 難用 |
| 一欄只放一種資訊 | 「City, State」「First Last」混在一欄，難以分群與建立關聯 |

### 預覽功能（View 頁籤）

| 功能 | 顯示 |
| --- | --- |
| Column quality | 有效 / 錯誤 / 空值比例 |
| Column distribution | distinct 與 unique 數、分布 |
| Column profile | 選取欄的統計與值分布 |

預設只根據前 1000 列計算，可在狀態列改成「根據整個資料集」；快速診斷可以，但不代表完整分布。

### 常用轉換

| 欄位類型 | 轉換 |
| --- | --- |
| 文字 | 大小寫、**Trim**（去前後空白）、**Clean**（去換行等控制字元）、分割欄、合併欄、取代值 |
| 數值 | 絕對值、對數、乘 / 加常數（單位換算）、四捨五入 |
| 日期 | 取出年 / 季 / 月 / 週 / 日、年 / 月初與月底、計算年齡 |

多來源的文字欄位，Trim + Clean 幾乎可以當作預設的第一輪處理。日期欄要盡早轉成真正的 date / time 型別，後面建階層與日期邏輯才順。

## 資料重塑

| 操作 | 方向 | 用途 |
| --- | --- | --- |
| Unpivot | wide → long | Excel 來源以月份當欄名、多個量值分散成多欄；模型通常偏好 long 格式 |
| Pivot | long → wide | 給人閱讀的表格 |
| Group By | 依 key 彙總 | 先把明細壓到客戶 / 產品 / 日期層級 |
| Append | 縱向堆疊（加列） | 多個月份、多個門市的同結構檔案；**先確認欄名、欄數、型別一致**，否則會默默補出 null |
| Merge | 橫向補欄（依 key） | 把 lookup 表接回明細表；key 型別、拼寫、cardinality 不一致會產生缺值、重複列或錯配 |

Merge 可以把多表壓成較平的表，但不代表所有表都該壓成一張：該維持 star schema 多表結構的，留給 semantic model 表達。long / wide 與 merge 的概念與 pandas / tidyr 相同，見 [pandas 重塑與合併](../../python-foundations/pandas/reshape-merge.md)。

## M 語言與自訂欄

每個 Power Query 步驟都會被翻譯成 M 程式碼；Advanced Editor 是 GUI 與程式碼之間的橋：可以檢視、直接編輯整段查詢。M **區分大小寫**，有標準函式庫。

```m
let
    Source   = Csv.Document(File.Contents("C:\data\samples.csv"), [Delimiter = ",", Encoding = 65001]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed    = Table.TransformColumnTypes(Promoted, {{"sample_id", type text}, {"age", Int64.Type}, {"date", type date}}),
    Trimmed  = Table.TransformColumns(Typed, {{"tissue", each Text.Clean(Text.Trim(_)), type text}}),
    AgeGroup = Table.AddColumn(Trimmed, "age_group",
                 each if [age] = null then "unknown" else if [age] < 40 then "<40" else "40+", type text)
in
    AgeGroup
```

| 自訂欄運算 | 語法 |
| --- | --- |
| 數值 | `+ - * /`；次方用 `Number.Power(x, 2)`（M 沒有 `^` 運算子） |
| 文字串接 | `&` |
| 比較 | `< > <> <= >= =` |
| 條件 | `if ... then ... else ...` |
| 布林 | `and or not` |

自訂欄最常見的問題不是語法，而是型別：文字當數字算、日期未轉型就比較、null 沒處理，可能報錯，更糟的是產生看似合理的錯誤結果。

## M vs DAX

| | M（Power Query） | DAX（模型） |
| --- | --- | --- |
| 目的 | 載入與轉換資料 | 在模型上做分析計算 |
| 典型動作 | 改名、篩選、pivot、group、自訂欄 | measure、計算欄、filter context |
| 執行時機 | 重新整理時 | 查詢時（measure） |
| 大小寫 | 區分 | 不區分 |

要改資料本身的形狀或內容 → M；要做隨篩選變化的分析計算 → DAX。
