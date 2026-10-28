---
name: rewrite-notes
description: 把 notebook 中任一資料夾的筆記改寫成統一的中文筆記風格（中文為主、術語附英文、表格優先、精簡程式碼、麵包屑返回、交叉連結、附檔放 src/），並依領域補充內容、修正錯誤、評估補圖表（uv + matplotlib，圖放 src/）、檢查連結。適用 biology、computing、data-science、frontend、productivity 各領域。用於使用者要求「整理 / 改寫 / 優化筆記資料夾」時。
argument-hint: "[資料夾路徑 ...]（省略則為目前工作目錄）"
---

# 筆記改寫 (Rewrite Notes)

把 notebook 中指定資料夾的 Markdown 筆記改寫成統一風格。風格以已完成的 `data-science/statistics/` 為範本，適用所有領域。

## 目標與範圍

- 目標：`$ARGUMENTS`；若為空，使用**目前工作目錄**。可傳入多個路徑（空白分隔），逐一處理；相對路徑以目前工作目錄為基準。
- 處理範圍：目標資料夾底下所有 `.md`（含子資料夾、`src/` 內的附檔 md）。
- **範圍太大時先切批**：超過約 30 篇或含多個大型子資料夾時，先列出建議批次（每批一個子資料夾、約 10–30 篇）給使用者確認，再一批一批做；每批完成就驗證並回報，建議使用者 commit 後再做下一批。不要一次改整個領域或整個 notebook。

## 參考範例

動手前先讀以下成品（路徑相對於 notebook 根目錄），對齊格式與詳略程度。規則與範例衝突時以本文件為準。只讀這幾篇，不要掃整個 statistics 資料夾。

| 範例 | 示範重點 |
| --- | --- |
| `data-science/statistics/README.md` | 頂層 README：模組表、建議路線、精簡度 |
| `data-science/statistics/descriptive-statistics/README.md` | 模組 README：麵包屑、順序圖、筆記表 |
| `data-science/statistics/descriptive-statistics/univariate-numerical.md` | 概念型筆記：表格化定義、合併程式碼、圖片並排、交叉連結 |
| `data-science/statistics/inferential-statistics/multiple-testing.md` | 新增筆記：針對目標讀者補充的主題寫法 |
| `data-science/statistics/method-selection.md` | 速查頁：以表格為主的查找入口 |
| `data-science/statistics/probability-and-distributions/src/discrete-distributions-binomial-derivation.md` | `src/` 附檔：返回連結與精簡推導 |

## 流程

1. **盤點**：列出所有檔案與大小、圖片 / 附檔位置；讀目標資料夾與上層的 README，了解結構與每篇筆記的類型（見「筆記類型」）。
2. **檢查外部連入**：在整個 notebook 中搜尋連到目標資料夾的連結（含 `#anchor`）。**不要改檔名、不要搬移或合併筆記**（除非使用者同意）；若外部連結用了 anchor，改標題後要同步修正。
3. **搬移附檔**：散落的圖片、PDF、附檔（包含 `assets/`、`images/`、`img/` 等資料夾）一律用 `git mv` 移到該模組的 `src/`，並更新所有引用。
4. **逐模組改寫**：每個模組先完整讀完再寫，避免重複內容。順序：README → 各筆記。
5. **補充與修正**（見「內容品質」）。
6. **新增筆記**：若有明顯缺口（對目標讀者重要卻沒有的主題），新增精簡筆記，並從相關 README 與筆記連過去。
7. **補圖表**：評估哪些段落加圖能明顯幫助理解，建議加的就加（見「新增圖表」）。
8. **驗證**：執行連結檢查（見「驗證」），修到零錯誤。
9. **不 commit**，除非使用者要求。最後回報：改了什麼、新增哪些筆記與圖表、修正了哪些錯誤、哪些沒驗證到（例如無法執行的程式碼、無法確認的外部資訊）。

長任務中每完成一個模組就用一句話回報進度。

## 筆記類型

先判斷每篇屬於哪一類，套用對應的寫法。

| 類型 | 例子 | 寫法重點 |
| --- | --- | --- |
| 概念型 | 統計方法、ML 演算法、分子生物機制、CS 原理 | 定義表 + 核心公式 / 機制 + 範例 + 常見誤解；適合補圖表 |
| 工具 / 指令型 | git、docker、pandas、R 套件、Excel 功能 | 依**任務**分節（「想做 X → 指令」）；指令速查表；合併成可直接執行的程式碼 block；註明版本差異 |
| 流程 / 工作流型 | RNA-seq pipeline、CI/CD、資料清理流程 | 先給整體流程（ASCII 流程圖或編號步驟），再逐步說明輸入 / 輸出 / 工具 / 檢查點 |
| 資源卡型 | 單一資料庫、網站、軟體的介紹（常只有幾行） | 保持短：標題 + 一句用途 + `| 項目 | 內容 |` 小表（網站、用途、適用情境、替代方案）。不硬加內容；同類資源多時，在 README 用比較表整理 |
| 速查 / 索引頁 | method-selection、指令總表 | 以表格為主，每列連到詳細筆記 |

## 寫作風格

### 語言

- **中文描述為主**，專有名詞第一次出現時附英文：`偏態 (Skewness)`、`容器映像檔 (container image)`。
- 難以翻譯或業界慣用的詞直接用英文（p-hacking、bootstrap、batch effect、commit、pipeline、prompt）。
- 指令、函式名、參數、檔名、欄位名維持原文並用 `inline code`。
- 標題格式：`# 中文標題 (English Title)`；專有名詞本身就是標題時（`# SNOMED CT`、`# Docker`）可只用英文。小節標題可只有中文或中英並列。
- 移除夾雜的英文長段落、重複的 Key point / Tip / Warning（原檔常有中英重複的同一句話，只留一次）。

### 結構

- 每篇第一行是**麵包屑**（兼返回鍵），之後空一行接標題。最多列出**兩層上層 README** + 本篇：
  ```markdown
  [Statistics](../README.md) › [推論統計](README.md) › 假設檢定

  # 假設檢定 (Hypothesis Testing)
  ```
  - 子資料夾 README：`[上層](../README.md) › 本層名`
  - 領域頂層 README（如 `biology/README.md`）：`[Notebook](../README.md) › 本層名`
  - 沒有 README 的層級直接略過，連到最近一層有 README 的上層。
  - `src/` 內的附檔：標題下放 `[← 回到 xxx](../file.md#anchor)`
- 開頭 1–2 句說明這篇在講什麼、為什麼重要。不寫「This section covers…」式的空話。
- **能用表格就用表格**：定義、比較、選擇指南、判讀規則、指令速查、優缺點、常見錯誤都做成表。
- 決策流程、管線流程用 ASCII 樹狀圖 / 流程圖（放在 ``` 區塊）。
- 重點、警告用 blockquote：`> **重點**` 或直接 `> 內文`；不要用 `Key point:` / `Tip:` / `Warning:` 前綴。
- 不要每篇結尾都放「Key Takeaways」表；只有內容確實需要總結時才放，且不能重複前文。
- 刪掉面試問答段落，把有價值的內容併入正文表格。

### README

- **保持精簡**：一句簡介 + 建議順序（一行或小流程圖，若筆記有先後關係）+ 筆記表（`| 筆記 | 內容 | 回答的問題 |`；資源類可改 `| 資源 | 用途 | 何時用 |`）。
- 不要「What's Inside Each Section」這類重複細節、不要把每篇內容再寫一次。
- 領域頂層 README 可加「建議路線」表（依讀者類型）與速查頁連結。

### 程式碼與指令

- 必須用 ``` 區塊並標語言（`python`、`r`、`bash`、`powershell`、`sql`、`yaml`、`dockerfile`…）。
- **同一主題的多段程式碼合併成一個 block**，用 comment 分段說明（`# 1. ...`、行尾 `# 意義`）。
- 輸出結果寫成行尾 comment（`x.mean()   # 5.84`），不要另外貼大段輸出；指令輸出只留關鍵幾行。
- 刪除只為畫圖的冗長程式碼（已有圖片時尤其如此）；保留能說明 API 用法的最小程式碼。
- Python：移除不必要的 `print(f"...")` 包裝與重複 import，`np.random.seed` 改用 `np.random.default_rng(seed)`。
- Shell：區分平台時用小表或分開的 block（bash / PowerShell），不要混在同一個 block。
- 已過時的 API、指令或參數要更新（如 pandas `append`、sklearn 舊參數、`docker-compose` → `docker compose`），不確定時查官方文件，查不到就在回報中列出。
- 不必要的公式推導移到 `src/` 附檔或刪除；正文只留理解所需的核心公式。
- 另一語言版本若有價值（R ↔ Python），用「對照」小表或一個短 block 呈現。

### 圖片

- 一律放在模組的 `src/`，檔名維持原樣。
- 多張相關圖片用表格並排：`| 圖 A | 圖 B |` 下一列放 `![...](src/...)`。
- 圖片來源改為一行：`<sub>圖片來源：[網站](url)</sub>`。

### 新增圖表

**判斷是否要加**：圖要能表達表格或文字說不清楚的東西；建議加的就加，沒有必要就不加。

| 適合加圖 | 不必加圖 |
| --- | --- |
| 分配 / 曲線形狀（α、β、power；偏態；Poisson vs NB；學習率、loss 曲線） | 定義、選擇指南、步驟清單（表格已足夠） |
| 重複抽樣或模擬才看得出的概念（CI 覆蓋率、CLT、bias-variance） | 已有同內容的圖，或相鄰筆記已有圖可連過去 |
| 判讀型態（殘差圖、ACF/PACF、軌跡圖、p 值直方圖、ROC / PR 曲線、學習曲線） | 只是把表格數字畫成長條圖 |
| 比較方法差異（Ridge vs Lasso、K-Means vs DBSCAN、決策邊界、activation functions） | 需要真實外部資料才有意義、模擬會誤導 |
| 反直覺現象（Simpson's paradox、槓桿 vs 影響力、資料洩漏） | 工具操作畫面（截圖易過時，用文字步驟） |

各領域的方向：

| 領域 | 適合用 matplotlib 產生的圖 | 改用 ASCII / 表格 |
| --- | --- | --- |
| data-science | 上表各類；ML 的決策邊界、正則化、學習曲線、評估曲線 | 模型選擇流程 |
| biology | 定量概念：覆蓋度分布、Phred 品質分數、MA / volcano plot 型態、劑量反應、Hardy-Weinberg | 分子機制、實驗流程、遺傳模式 |
| computing | 複雜度成長曲線、快取命中率、排程 / 延遲比較等定量概念 | 架構圖、git 分支圖、指令流程 |
| frontend / productivity | 很少需要 | 元件樹、操作步驟 |

**產生方式**：

- 用 `uv` 建立暫存環境（放 scratchpad 或短路徑暫存目錄，**不要放在筆記資料夾**）：`uv venv <dir>` → `uv pip install --python <dir> numpy scipy matplotlib pandas scikit-learn statsmodels`（依需要增減）。Windows 上路徑過長可能讓 scikit-learn 安裝不完整（`ModuleNotFoundError`），改用短路徑（如 `%TEMP%\sv`）。
- 畫圖腳本寫在 scratchpad，**不保存執行檔**，筆記裡也不貼只為畫圖的程式碼。
- 優先用筆記本身的資料與參數（iris、diabetes、文中的 μ、σ、n、seed），讓圖與正文數字一致；模擬時固定 `default_rng(seed)`。
- 產圖後**逐張開圖檢查**：文字重疊、圖例遮擋、標題是否與正文說法一致。圖中數字與正文衝突時，先查清楚是誰錯，再修正文或圖。

**風格**（與既有圖一致）：

- matplotlib 預設樣式，`dpi=150`、`bbox_inches="tight"`；主色 `steelblue`、對比色 `tomato`、輔助 `gray`。
- 圖內文字用**英文**（避免中文字型缺失），標題直接寫出結論（如 "PACF cuts off after lag 2"）；中文解讀寫在正文。
- 多個情境並排成 1×3 或 2×2 子圖（例：好 / 壞 / 更壞），比拆成多張圖好讀。

**放置與命名**：

- 存到該模組的 `src/`，檔名 `<筆記檔名>-<內容>.png`（如 `hypothesis-testing-errors-power.png`）。
- 插在對應的表格或程式碼之後，必要時補 1–2 句圖的判讀重點，不要重複表格內容。
- 若原文有只為畫該圖的程式碼，改成圖片並刪除程式碼。

### 交叉連結

- 提到其他筆記已深入說明的概念時，**連過去而不是重寫**。
- 主動連結跨領域的對應筆記，例如：統計 ↔ ML（MLE ↔ loss、正則化 ↔ 先驗）、生資流程 ↔ 統計方法（DESeq2 ↔ NB-GLM、多重檢定）、資料工程 ↔ 資料庫、工具筆記 ↔ 使用它的流程筆記。連結前確認目標檔存在。
- 需要 anchor 時，依 GitHub slug 規則計算：小寫、移除標點（含全形「：（）、」與 `×`、`&`、`/`、`'`）、空白換成 `-`，中文保留。例：`## 四分位距與離群值 (IQR & Outliers)` → `#四分位距與離群值-iqr--outliers`。

## 內容品質

**目標讀者**：一般學生物資訊、具基本 ML 與程式背景的人。依領域補充對他們最有用的內容，例如：

| 領域 | 優先補充 |
| --- | --- |
| statistics | 多重檢定 / FDR、計數資料（Poisson / 負二項、過度離散）、批次效應、生物 vs 技術重複、假重複、log 轉換、富集分析 |
| machine-learning / deep-learning | 資料洩漏、交叉驗證設計、評估指標選擇、類別不平衡、bias-variance、與統計觀念的對應；生資應用（高維小樣本、單細胞、蛋白質 / 序列模型） |
| data-manipulation / python / r / databases / data-engineering | 常見陷阱（view vs copy、NA 處理、型別、join 爆量）、效能（向量化、chunk、索引）、可重現性（環境、版本、seed）、Python ↔ R ↔ SQL 對照 |
| llm / ai-strategy | 評估方法、幻覺與驗證、成本 / 延遲取捨、資料隱私；在生資 / 醫療情境的用法與限制 |
| biology | 原理 ↔ 資料特性 ↔ 分析方法的對應（例如定序技術 → 錯誤型態 → QC 指標）；常用資料庫與檔案格式；臨床解讀的限制 |
| computing | 生資常用情境（HPC / 排程器、conda / 容器、大檔案處理、工作流引擎）；Windows / macOS / Linux 差異 |
| frontend / productivity | 依任務整理、保持精簡；不必強行補充 |

- **修正錯誤**：手算核對範例數字、表格輸出、程式碼邏輯、指令參數（常見：輸出表與程式不符、反例數據其實不成立、函式參數誤用、過時的 API）。能執行就執行驗證；不能執行時手算，並在回報中說明。
- **外部事實**：版本號、網址、資料庫收錄範圍、法規等時效性內容，不要憑記憶修改；需要更新時查官方來源，查不到就保留原文並在回報中列出。
- 刪除重複、空洞或與其他筆記重疊的段落；保留原筆記中有價值的細節（不要為了精簡而丟掉知識點）。

## 驗證

改寫完後，用 `uv` 執行同目錄的 [check_links.py](check_links.py)（只用標準函式庫，不需安裝套件）：

```bash
uv run --no-project "<notebook>/.claude/skills/rewrite-notes/check_links.py" "<目標資料夾>"
```

腳本會檢查：相對連結的檔案是否存在、`#anchor` 是否對應到目標檔的標題、圖片是否都被引用且位於 `src/`；略過 `.` 開頭的資料夾。輸出只有 `Checked N files` 才算完成。

外部連入（步驟 2）不在目標資料夾內，改完後再對**整個 notebook** 跑一次，確認沒有因改標題而失效的 anchor。
