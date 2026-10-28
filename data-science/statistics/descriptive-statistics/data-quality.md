[Statistics](../README.md) › [敘述統計](README.md) › 資料品質

# 資料品質 (Data Quality)

在算任何摘要統計、做檢定或建模之前，先確認資料是「可分析的」(analysis-ready)。缺失值、重複列、錯誤單位都可能嚴重扭曲平均數、p 值與迴歸係數。

> 組織層級的資料品質治理（責任歸屬、監控）見 [Data Engineering: Data Quality Checks](../../data-engineering/data-quality-checks.md)。

## 快速檢查表

| 問題 | 怎麼查 | 常見處理 |
| --- | --- | --- |
| 缺失值 (missing values) | `df.isna().sum()`、`df.isna().mean()` | 刪除、插補 (impute)、標記為 unknown |
| 重複 (duplicates) | `df.duplicated()`、ID 是否唯一 | 移除真正的重複 |
| 離群值 (outliers) | Boxplot、IQR、z-score | 先查證，再決定保留 / 截尾 / 轉換 |
| 不可能的值 (invalid values) | 範圍檢查（年齡 < 0、比例 > 1） | 修正來源或設為缺失 |
| 類別標籤不一致 | `df[col].unique()` | 統一標籤（`male` / `Male` / `M`） |
| 單位混用 (unit mismatch) | 摘要統計看量級 | 分析前統一單位（cm vs inch） |
| 偽裝的缺失值 | 找 `999`、`-1`、`"unknown"`、空字串 | 轉成 `NaN` |
| 日期格式不一 | `2024/01/02` vs `02-01-2024` | 統一用 `pd.to_datetime` 解析 |

```python
import numpy as np

# 缺失值：數量與比例
df.isna().sum().sort_values(ascending=False)
df.isna().mean().sort_values(ascending=False)

# 偽裝的缺失值 → NaN
df = df.replace([999, -1, "unknown", ""], np.nan)

# 重複列 / 重複 ID
df.duplicated().sum()
df["sample_id"].is_unique
```

## 缺失值 (Missing Data)

不要直接 `dropna()`。先看：

- 哪些欄缺最多？缺多少比例？
- 缺失是否集中在某些群組、時間、批次 (batch)？→ 若是，代表缺失可能不是隨機的

缺失機制 MCAR / MAR / MNAR 與對應處理見 [Missing Data Mechanisms](../../data-manipulation-and-eda/missing-data.md)；ML 前處理的插補見 [Imputation](../../machine-learning/preprocessing/imputation.md)。

## 離群值 (Outliers)

偵測方法（IQR fence、boxplot）見 [單變數：數值型](univariate-numerical.md#四分位距與離群值-iqr--outliers)。

| 離群值類型 | 處理方式 |
| --- | --- |
| 輸入錯誤 (data entry error) | 修正或移除 |
| 真實但極端的值 | 保留，並報告敏感度分析 (sensitivity analysis) |
| 量測假影 (measurement artifact) | 有正當理由才移除 |
| 對模型影響大的點 (influential point) | 查 leverage 與殘差，見 [迴歸診斷](../regression-analysis/multiple-linear-regression.md) |

> 很多「離群值」其實是單位或輸入錯誤。先理解意義，再決定刪不刪。

## 建議的檢查順序

1. 每一列 (row) 代表什麼？ID 與重複
2. 缺失模式
3. 不可能的值、單位不一致
4. 理解脈絡後再看離群值

如果還答不出「每列代表什麼、每欄的意義與單位、缺失集中在哪」，建模通常還太早。

## 生物資料常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 基因名稱被 Excel 轉成日期 | `SEPT2` → `2-Sep`、`MARCH1` → `1-Mar` |
| 批次效應 (batch effect) | 不同實驗批次 / 定序機台造成系統性差異，常被誤認為生物訊號，見 [干擾與偏誤](../experimental-design/confounding-bias.md) |
| 低於偵測下限 (below detection limit) | 0 或缺失可能代表「沒測到」而不是「不存在」 |
| 樣本標籤錯置 (sample swap) | 用性別基因、genotype 等交叉驗證樣本身分 |
