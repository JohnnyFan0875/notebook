---
name: rewrite-notes
description: 把筆記資料夾改寫成統一的中文筆記風格（中文為主、術語附英文、表格優先、精簡程式碼、麵包屑返回、交叉連結、附檔放 src/），並補充內容、修正錯誤、評估補圖表（uv + matplotlib，圖放 src/）、檢查連結。用於使用者要求「整理 / 改寫 / 優化筆記資料夾」時。
argument-hint: "[資料夾路徑 ...]（省略則為目前工作目錄）"
---

# 筆記改寫 (Rewrite Notes)

依 `data-science/statistics/` 已建立的風格，改寫指定資料夾內的 Markdown 筆記。

## 目標資料夾

- 目標：`$ARGUMENTS`
- 若 `$ARGUMENTS` 為空，使用**目前工作目錄**。
- 可傳入多個路徑（空白分隔），逐一處理；相對路徑以目前工作目錄為基準。
- 處理範圍：目標資料夾底下所有 `.md`（含子資料夾、`src/` 內的附檔 md）。

## 參考範例

動手前先讀以下幾篇成品（路徑相對於 notebook 根目錄），對齊格式與詳略程度。規則與範例衝突時以本文件為準。

| 範例 | 示範重點 |
| --- | --- |
| `data-science/statistics/README.md` | 頂層 README：模組表、建議路線、精簡度 |
| `data-science/statistics/descriptive-statistics/README.md` | 模組 README：麵包屑、順序圖、筆記表 |
| `data-science/statistics/descriptive-statistics/univariate-numerical.md` | 一般筆記：表格化定義、合併程式碼、圖片並排、交叉連結 |
| `data-science/statistics/inferential-statistics/multiple-testing.md` | 新增筆記：針對生資讀者補充的主題寫法 |
| `data-science/statistics/method-selection.md` | 速查頁：以表格為主的查找入口 |
| `data-science/statistics/probability-and-distributions/src/discrete-distributions-binomial-derivation.md` | `src/` 附檔：返回連結與精簡推導 |

只需讀這幾篇，不要掃整個 statistics 資料夾。

## 流程

1. **盤點**：列出所有檔案與大小、圖片 / 附檔位置；讀頂層與各子資料夾的 README，了解結構。
2. **檢查外部連入**：在整個 notebook 中搜尋連到目標資料夾的連結（含 `#anchor`）。**不要改檔名**；若外部連結用了 anchor，改標題後要同步修正。
3. **搬移附檔**：模組內散落的圖片、附檔一律用 `git mv` 移到該模組的 `src/`，並更新引用。
4. **逐模組改寫**：每個模組先完整讀完再寫，避免重複內容。順序：README → 各筆記。
5. **補充與修正**（見下方「內容品質」）。
6. **新增筆記**：若有明顯缺口（對目標讀者重要卻沒有的主題），新增精簡筆記，並從相關 README 與筆記連過去。
7. **補圖表**：評估哪些段落加圖能明顯幫助理解，只加建議加的（見下方「新增圖表」）。
8. **驗證**：執行連結檢查腳本（見「驗證」），修到零錯誤；確認沒有未引用或不在 `src/` 的圖片。
9. **不 commit**，除非使用者要求。最後回報：改了什麼、新增哪些筆記與圖表、修正了哪些錯誤、哪些沒驗證到（例如沒有 Python 環境無法執行程式碼）。

長任務中每完成一個模組就用一句話回報進度。

## 寫作風格

### 語言

- **中文描述為主**，專有名詞第一次出現時附英文：`偏態 (Skewness)`、`偽發現率 (false discovery rate, FDR)`。
- 難以翻譯或業界慣用的詞直接用英文（p-hacking、bootstrap、batch effect、log fold change）。
- 標題格式：`# 中文標題 (English Title)`；小節標題可只有中文或中英並列。
- 移除夾雜的英文長段落、重複的 Key point / Tip / Warning（原檔常有中英重複的同一句話，只留一次）。

### 結構

- 每篇第一行是**麵包屑**（兼返回鍵），之後空一行接標題：
  ```markdown
  [Statistics](../README.md) › [推論統計](README.md) › 假設檢定

  # 假設檢定 (Hypothesis Testing)
  ```
  - 模組 README：`[上層](../README.md) › 模組名`
  - 頂層 README：`[上上層](../README.md) › 本層名`
  - `src/` 內的附檔：標題下放 `[← 回到 xxx](../file.md#anchor)`
- 開頭 1–2 句說明這篇在講什麼、為什麼重要。不寫「This section covers…」式的空話。
- **能用表格就用表格**：定義、比較、選擇指南、判讀規則、優缺點、常見錯誤都做成表。
- 決策流程用 ASCII 樹狀圖（放在 ``` 區塊）。
- 重點、警告用 blockquote：`> **重點**` 或直接 `> 內文`；不要用 `Key point:` / `Tip:` / `Warning:` 前綴。
- 不要每篇結尾都放「Key Takeaways」表；只有內容確實需要總結時才放，且不能重複前文。
- 刪掉面試問答段落，把有價值的內容併入正文表格。

### README

- **保持精簡**：一句簡介 + 建議順序（一行或小流程圖）+ 筆記表（`| 筆記 | 內容 | 回答的問題 |`）。
- 不要「What's Inside Each Section」這類重複細節、不要工具清單長表（必要時 3–4 列小表）。
- 頂層 README 可加「建議路線」表（依讀者類型）與一份速查頁連結。

### 程式碼

- 必須用 ``` 區塊並標語言。
- **同一主題的多段程式碼合併成一個 block**，用 comment 分段說明（`# 1. ...`、行尾 `# 意義`）。
- 輸出結果寫成行尾 comment（`x.mean()   # 5.84`），不要另外貼大段輸出。
- 刪除只為畫圖的冗長程式碼（已有圖片時尤其如此）；保留能說明 API 用法的最小程式碼。
- 移除不必要的 `print(f"...")` 包裝、重複的 import、`np.random.seed` 改用 `np.random.default_rng(seed)`。
- 不必要的公式推導移到 `src/` 附檔或刪除；正文只留理解所需的核心公式。
- R 版本若有價值，用「R 對照」小表或一個短 block 呈現。

### 圖片

- 一律放在模組的 `src/`，檔名維持原樣。
- 多張相關圖片用表格並排：`| 圖 A | 圖 B |` 下一列放 `![...](src/...)`。
- 圖片來源改為一行：`<sub>圖片來源：[網站](url)</sub>`。

### 新增圖表

**判斷是否要加**：圖要能表達表格或文字說不清楚的東西，沒有必要就不加。

| 適合加圖 | 不必加圖 |
| --- | --- |
| 機率面積 / 分配形狀（α、β、power；偏態；Poisson vs NB） | 定義、選擇指南、步驟清單（表格已足夠） |
| 重複抽樣的概念（CI 覆蓋率、CLT） | 已有同內容的圖，或相鄰筆記已有圖可連過去 |
| 判讀型態（殘差圖、交互作用圖、ACF/PACF、軌跡圖、p 值直方圖） | 只是把表格數字畫成長條圖 |
| 比較方法差異（Ridge vs Lasso 路徑、K-Means vs DBSCAN、Pearson vs Spearman） | 需要真實外部資料才有意義、模擬會誤導 |
| 反直覺現象（Simpson's paradox、槓桿 vs 影響力） | |

**產生方式**：

- 用 `uv` 建立暫存環境（放 scratchpad 或短路徑暫存目錄，**不要放在筆記資料夾**）：`uv venv <dir>` → `uv pip install --python <dir> numpy scipy matplotlib pandas scikit-learn statsmodels`。Windows 上路徑過長可能讓 scikit-learn 安裝不完整（`ModuleNotFoundError`），改用短路徑（如 `%TEMP%\sv`）。
- 畫圖腳本寫在 scratchpad，**不保存執行檔**，筆記裡也不貼只為畫圖的程式碼。
- 優先用筆記本身的資料與參數（iris、diabetes、文中的 μ、σ、n、seed），讓圖與正文數字一致；模擬時固定 `default_rng(seed)`。
- 產圖後**逐張開圖檢查**：文字重疊、圖例遮擋、標題是否與正文說法一致（例如 MH 接受率、BH 門檻）。圖中數字與正文衝突時，先查清楚是誰錯，再修正文或圖。

**風格**（與既有圖一致）：

- matplotlib 預設樣式，`dpi=150`、`bbox_inches="tight"`；主色 `steelblue`、對比色 `tomato`、輔助 `gray`。
- 圖內文字用**英文**（避免中文字型缺失），標題直接寫出結論（如 "PACF cuts off after lag 2"）；中文解讀寫在正文。
- 多個情境並排成 1×3 或 2×2 子圖（例：好 / 壞 / 更壞），比拆成多張圖好讀。

**放置與命名**：

- 存到該模組的 `src/`，檔名 `<筆記檔名>-<內容>.png`（如 `hypothesis-testing-errors-power.png`）。
- 插在對應的表格或程式碼之後，必要時補 1–2 句圖的判讀重點，不要重複表格內容。
- 若原文有只為畫該圖的程式碼，改成圖片並刪除程式碼。

### 交叉連結

- 提到其他筆記已深入說明的概念時，**連過去而不是重寫**（例如 SE、CLT、多重檢定、假設檢查）。
- 連結到 notebook 其他領域的相關筆記（如 `../../machine-learning/...`），讓統計與 ML 互相對應。
- 需要 anchor 時，依 GitHub slug 規則計算：小寫、移除標點（含全形「：（）、」與 `×`、`&`、`/`、`'`）、空白換成 `-`，中文保留。例：`## 四分位距與離群值 (IQR & Outliers)` → `#四分位距與離群值-iqr--outliers`。

## 內容品質

- **目標讀者**：一般學生物資訊、具基本 ML 背景的人。補充對他們最有用的內容，例如：
  - 生資：多重檢定 / FDR、計數資料（Poisson / 負二項、過度離散）、批次效應、生物 vs 技術重複、假重複、log 轉換、PCA / 分群在表現資料上的用法、富集分析。
  - ML：MLE ↔ loss function、bias-variance、正則化 ↔ 先驗、bootstrap / 置換檢定、資料洩漏、交叉驗證、評估指標的對應。
- **修正錯誤**：手算核對範例數字、表格輸出、程式碼邏輯（常見：輸出表與程式不符、反例數據其實不成立、函式參數誤用）。能執行就執行驗證；不能執行時手算，並在回報中說明。
- 刪除重複、空洞或與其他筆記重疊的段落；保留原筆記中有價值的細節（不要為了精簡而丟掉知識點）。

## 驗證

改寫完後，在目標資料夾執行同目錄的 [check-links.ps1](check-links.ps1)：

```powershell
powershell -ExecutionPolicy Bypass -File "<notebook>/.claude/skills/rewrite-notes/check-links.ps1" -Path "<目標資料夾>"
```

腳本會檢查：相對連結的檔案是否存在、`#anchor` 是否對應到目標檔的標題、圖片是否都被引用且位於 `src/`。輸出為空（只有 `Checked N files`）才算完成。
