[Data Science](../README.md) › [資料處理與 EDA](README.md) › EDA 流程

# EDA 流程 (EDA Workflow)

探索式資料分析 (Exploratory Data Analysis, EDA) 不是把所有圖畫一遍，而是用最少步驟建立「這份資料可不可信、長什麼樣」的理解，在建模前抓到欄位定義錯誤、偏差與資料洩漏。

## 整體流程

```text
1. 釐清問題      目標變數？觀測單位（一列 = 一個病人？一個樣本？一個 read？）？時間範圍？
2. Profiling     結構、型別、完整性、唯一性、合理性、一致性
3. 單變數        數值：偏態、極端值、是否需 log；類別：不平衡、稀有類別、拼寫分裂
4. 雙變數 / 多變數 數值×數值、類別×數值、時間×數值；PCA 看批次
5. 初步假設      哪些變數可能重要？哪些欄位有 leakage 風險？
6. 記錄行動      要轉型 / 清理 / 排除 / 分層的欄位清單
```

各類品質問題的統計影響（缺失、重複、單位、離群值）見 [Statistics：資料品質](../statistics/descriptive-statistics/data-quality.md)；多變數的工具與 Simpson's paradox 見 [多變量探索](../statistics/multivariate-analysis/multivariate-eda.md)。

## 第一步：資料剖析 (Data Profiling)

每份新資料集都跑一次的固定檢查表：

| 面向 | 要問的問題 | 常見風險訊號 |
| --- | --- | --- |
| 結構 | 幾列幾欄？主鍵是什麼？一列代表什麼？ | 列數比預期少 → 前面 filter / join 掉了資料 |
| 型別 | 數值、類別、日期、文字判斷正確嗎？ | 數值欄變成 `object` / `str`（混入 `""`、`"NA"`、`">100"`）；日期沒轉 datetime 導致排序錯 |
| 完整性 | 缺失比例？集中在特定欄位或群體？ | 缺失集中在某批次 / 某中心 → 不是隨機，見 [缺失機制](missing-data.md) |
| 唯一性 | 主鍵重複嗎？類別值有拼寫分裂嗎？ | 重複匯入造成的重複列；`"NY"` / `"New York"` / `"new york"` |
| 合理性 | 值域、單位、日期順序合理嗎？ | 負的年齡、出院早於入院、mg 與 g 混用 |
| 一致性 | 同一欄是否混多種格式？ | `"2024/01/02"` 與 `"02-01-2024"` 混用 |

```python
import pandas as pd
import seaborn as sns

df = sns.load_dataset("penguins")

# 1. 結構與型別
df.shape
df.info()
df.sample(5, random_state=0)        # 不只看 head()，也看隨機列與 tail()

# 2. 每欄一列的 profile 表
profile = pd.DataFrame({
    "dtype": df.dtypes,
    "missing_ratio": df.isna().mean(),
    "n_unique": df.nunique(dropna=False),
}).sort_values("missing_ratio", ascending=False)

# 3. 數值欄摘要；類別欄看次數（含 NaN）
df.describe().T
for col in df.select_dtypes(exclude="number"):
    print(df[col].value_counts(dropna=False), "\n")

# 4. 重複
df.duplicated().sum()                      # 完全重複的列
df.duplicated(subset=["id"]).sum()         # 主鍵重複（有 id 欄時）
```

> 想要一鍵報表可用 `ydata-profiling`（`ProfileReport(df)`）或 R 的 `skimr::skim()`，但報表只是起點，結論仍要自己寫下來。

做完 profiling 留一份簡短紀錄：哪些欄位要轉型、要清理、暫時排除，哪些可能是 target、feature 或分層變數。

## Python ↔ R 對照

| 任務 | pandas | R (tidyverse) |
| --- | --- | --- |
| 結構 / 型別 | `df.info()` | `glimpse(df)` |
| 摘要統計 | `df.describe(include="all")` | `summary(df)`、`skimr::skim(df)` |
| 缺失比例 | `df.isna().mean()` | `colMeans(is.na(df))`、`naniar::miss_var_summary(df)` |
| 類別次數 | `s.value_counts(dropna=False)` | `count(df, x)` |
| 重複列 | `df.duplicated().sum()` | `sum(duplicated(df))` |

## omics 資料的 EDA

基因表現矩陣（基因 × 樣本）與一般表格的檢查重點不同：

| 檢查 | 做法 | 看什麼 |
| --- | --- | --- |
| 樣本與 metadata 對齊 | `set(counts.columns) == set(meta.index)`，並依 metadata 排序欄位 | 樣本名稱不一致、順序錯位（最常見也最致命的錯） |
| 基因 ID | 檢查重複 ID、版本號（`ENSG00000141510.17`）、Excel 轉成日期的基因名（`SEPT2` → `2-Sep`） | 重複列、無法對應的 ID |
| 文庫大小 (library size) | 每個樣本的 total counts | 某樣本特別低 → 定序失敗或要排除 |
| 偵測基因數 | 每樣本 count > 0 的基因數 | 與文庫大小一起判斷樣本品質 |
| 分布 | 每樣本 `log2(count + 1)` 的箱型圖 / 密度圖 | 原始 count 高度右偏，先 log 再看 |
| 樣本相關 / PCA | log 轉換後的 PCA，依條件、批次、定序日期上色 | 樣本依**批次**而非生物條件分群 → 批次效應 |

```python
import numpy as np

# counts: 基因 × 樣本的 DataFrame；meta: index 為樣本名
assert set(counts.columns) == set(meta.index)
counts = counts[meta.index]                      # 欄位順序對齊 metadata

qc = pd.DataFrame({
    "lib_size": counts.sum(),
    "n_detected": (counts > 0).sum(),
}).join(meta)

logc = np.log2(counts + 1)
logc.boxplot(rot=90)                             # 每樣本分布
```

PCA 的計算與解讀見 [PCA](../statistics/multivariate-analysis/pca.md)；批次效應與混淆見 [混淆與偏誤](../statistics/experimental-design/confounding-bias.md)。

## 判讀與後續動作

| 觀察 | 可能原因 | 下一步 |
| --- | --- | --- |
| 資料量比預期少 | filter 過頭、inner join 掉資料 | 每步驟後印 `shape`，join 前後比對 key |
| 某欄幾乎全空 | 欄位沒用到，或某流程站沒填 | 先問是否重要；重要就調查缺失機制 |
| 類別極不平衡 | 罕見疾病、少數族群 | 建模時用分層切分、適當評估指標，見 [類別不平衡](../machine-learning/evaluation/class-imbalance.md) |
| 時間上有明顯斷點 | 儀器 / 試劑 / 流程改版 | 不要隨機切分；改用時間切分或加批次變數 |
| 某欄與 target 幾乎完全相關 | 資料洩漏（事後才知道的變數、ID 編碼了結果） | 刪除或重新定義，見 [資料洩漏](../machine-learning/foundations/data-leakage.md) |
| 樣本依批次分群 | 批次效應 | 檢查批次與條件是否混淆；設計上無法分開時結論有限 |

## 常見錯誤

| 錯誤 | 為什麼有問題 |
| --- | --- |
| 只看 `head()` | 檔尾常有加總列、註解列；排序過的檔前幾列不具代表性 |
| 只看平均數 | 偏態、雙峰、離群值都看不到；搭配中位數、IQR 與圖，見 [圖表設計原則](visualization/chart-design-principles.md) |
| 看到缺值就補 | 沒先釐清缺失機制，補值可能製造偏誤 |
| 先標準化 / 編碼再切 train/test | 用到測試集資訊 → 洩漏，見 [Train-Test Split](../machine-learning/preprocessing/train-test-split.md) |
| ID 欄位當 feature | 模型學到 ID 與結果的偶然關聯 |
| EDA 看完全部資料才定假設 | 在同一份資料上探索又檢定 → 偽陽性膨脹；探索與確認最好分開資料 |
