[Python Foundations](../README.md) › [pandas](README.md) › Reshape 與 Merge

# Reshape 與 Merge

Reshape 改變表的形狀（寬 ↔ 長），merge / concat 把多張表合在一起。merge 最常見的 bug 不是語法錯，而是 **key 不唯一造成列數暴增**，或 **key 對不到造成資料靜靜消失**；每次 merge 前後都要檢查列數。

## 寬表與長表

```text
寬表 (wide)：一列一個基因、一欄一個樣本          長表 (long / tidy)：一列一個觀測
gene  S1  S2                                        gene  sample  expr
TP53   5   7      ── melt ──▶                       TP53  S1      5
EGFR   3   4      ◀── pivot ──                      TP53  S2      7
                                                    EGFR  S1      3
                                                    EGFR  S2      4
```

| 格式 | 適合 |
| --- | --- |
| 寬表 | 矩陣運算（PCA、相關、聚類）、人看、DESeq2 等的 count matrix |
| 長表 | `groupby`、seaborn / ggplot2 作圖、統計模型、資料庫 |

### melt：寬 → 長

```python
import pandas as pd

wide = pd.DataFrame({"gene": ["TP53", "EGFR"], "S1": [5, 3], "S2": [7, 4]})
long = wide.melt(id_vars="gene", var_name="sample", value_name="expr")   # 4 列

# 只攤開部分欄
iris.melt(id_vars="species", value_vars=["sepal_length", "petal_length"],
          var_name="measurement", value_name="value")

# 欄名有規律（sales_2022、sales_2023）：wide_to_long 直接把後綴變成一欄
w = pd.DataFrame({"id": [1, 2], "sales_2022": [1, 2], "sales_2023": [3, 4]})
pd.wide_to_long(w, stubnames="sales", i="id", j="year", sep="_").reset_index()
#    id  year  sales
# 0   1  2022      1  ...
```

### pivot 與 pivot_table

長表 → 寬表。

```python
long.pivot(index="gene", columns="sample", values="expr")    # 不彙總；key 組合重複就 ValueError

# key 組合可能重複（例如技術重複）→ pivot_table 先彙總再攤開
long.pivot_table(index="gene", columns="sample", values="expr", aggfunc="mean", fill_value=0)
iris.pivot_table(index="species", values=["sepal_length", "petal_width"],
                 aggfunc={"sepal_length": "mean", "petal_width": "sum"})
iris.pivot_table(index="species", columns=iris["sepal_width"] > 3,
                 values="sepal_length", aggfunc="mean", margins=True)   # 加總列 / 欄
```

| | `pivot` | `pivot_table` |
| --- | --- | --- |
| 彙總 | 不做 | 做（預設 mean） |
| 重複 key | `ValueError: Index contains duplicate entries` | 依 `aggfunc` 合併 |
| 用途 | 已確定一對一的長表 | 樞紐分析表 |

`pivot` 報重複錯誤時，先用 `long.duplicated(["gene", "sample"]).sum()` 找出重複，確認原因再決定用哪種彙總，不要直接換成 `pivot_table` 把問題蓋掉。資料已在 index 時用 `stack` / `unstack`，見 [Index 與 MultiIndex](index-multiindex.md#stack-與-unstack)。

### explode：一格多值 → 多列

```python
cities = pd.DataFrame({"city": ["Taipei", "Kaohsiung"], "zip": ["100,103", "800"]})
cities.assign(zip=cities["zip"].str.split(",")).explode("zip", ignore_index=True)   # 3 列
```

常見於一個變異對到多個基因、一篇文獻有多個標籤、GO 註解欄位以分號分隔。

## Concat：上下或左右接

```python
pd.concat([df_jan, df_feb, df_mar], ignore_index=True)                  # 上下接，重新編 index
pd.concat([df_jan, df_feb], keys=["jan", "feb"])                        # 外層 index 標記來源
pd.concat([df_jan, df_feb], keys=["jan", "feb"], names=["month", None]).reset_index(level=0)  # 來源變成欄
pd.concat([left, right], join="inner")                                  # 只留共同欄
pd.concat([df_a, df_b], axis=1)                                         # 左右接：依 index 對齊
pd.concat([df_feb, df_mar], verify_integrity=True)                      # index 重複就報錯

# 多個檔案：讀成 list 再一次 concat（不要在迴圈裡反覆 concat）
from pathlib import Path
frames = [pd.read_csv(p).assign(source=p.stem) for p in Path("data").glob("*.csv")]
df = pd.concat(frames, ignore_index=True)
```

上下接時欄名不同會產生 NaN 欄；先確認 `set(a.columns) ^ set(b.columns)` 是空集合。

## Merge：依 key 合併

```python
expr = pd.DataFrame({"gene": ["TP53", "TP53", "EGFR"], "sample": ["S1", "S2", "S1"], "expr": [5, 7, 3]})
ann = pd.DataFrame({"gene": ["TP53", "EGFR", "MYC"], "chrom": ["chr17", "chr7", "chr8"]})

expr.merge(ann, on="gene", how="left")                          # 保留 expr 全部列
expr.merge(ann, left_on="gene", right_on="symbol")              # key 欄名不同
expr.merge(ann, on=["gene", "sample"])                          # 複合 key
expr.merge(ann, on="gene", suffixes=("_expr", "_ann"))          # 同名非 key 欄，取代預設 _x / _y
expr.merge(ann_indexed, left_on="gene", right_index=True)       # 右表的 key 在 index
expr.set_index("gene").join(ann.set_index("gene"))              # index 對 index 的捷徑
```

| `how=` | 保留 | 試算表 / SQL / dplyr |
| --- | --- | --- |
| `"inner"`（預設） | 兩邊都有的 key | `INNER JOIN` / `inner_join` |
| `"left"` | 左表全部 | `VLOOKUP` 補欄位 / `LEFT JOIN` / `left_join` |
| `"right"` | 右表全部 | `RIGHT JOIN` |
| `"outer"` | 兩邊全部 | `FULL OUTER JOIN` / `full_join` |
| `"cross"` | 所有組合 | `CROSS JOIN` |

SQL 的 join 語意見 [SQL Joins](../../databases/sql-joins-and-set-operations.md)。

### 合併前檢查 key

```python
# 1. key 是否唯一（單欄與複合 key 分開檢查）
ann["gene"].duplicated().sum()                   # 0 才是唯一
expr.duplicated(["gene", "sample"]).sum()

# 2. key 的 dtype 與格式是否一致
expr["gene"].dtype, ann["gene"].dtype            # int vs str 會完全對不到
expr["gene"] = expr["gene"].str.strip().str.upper()

# 3. 讓 pandas 驗證關聯型態
expr.merge(ann, on="gene", how="left", validate="many_to_one")   # 右表 key 不唯一就 MergeError

# 4. 合併後檢查列數與沒對到的 key
out = expr.merge(ann, on="gene", how="left", indicator=True)
assert len(out) == len(expr)
out["_merge"].value_counts()                     # both / left_only / right_only
out.loc[out["_merge"] == "left_only", "gene"].unique()   # 註解表中找不到的基因
```

| `validate=` | 假設 |
| --- | --- |
| `"one_to_one"` / `"1:1"` | 兩邊 key 都唯一 |
| `"one_to_many"` / `"1:m"` | 左表 key 唯一 |
| `"many_to_one"` / `"m:1"` | 右表 key 唯一（最常見：補註解欄位） |
| `"many_to_many"` | 不檢查 |

> 列數暴增：若註解表中 TP53 有 2 個 transcript，`expr`（TP53 兩列）merge 後 TP53 會變 2 × 2 = 4 列，加上 EGFR 共 5 列，之後的平均、加總全都錯。left join 的結果列數應等於左表；多出來就是右表 key 不唯一。

### Anti join 與 semi join

```python
# anti join：左表中「沒有」對到右表的列
out = expr.merge(ann[["gene"]], on="gene", how="left", indicator=True)
expr_unannotated = out.loc[out["_merge"] == "left_only"].drop(columns="_merge")

# semi join：左表中「有」對到的列（不加右表欄位，也不會因右表重複而變多列）
expr[expr["gene"].isin(ann["gene"])]
expr[~expr["gene"].isin(ann["gene"])]            # anti join 的簡潔寫法
```

## 有順序的合併

| 函式 | 配對方式 | 用途 |
| --- | --- | --- |
| `merge` | key 完全相等 | 一般合併 |
| `merge_ordered` | 依 key 排序的 outer merge，可前值填補 | 對齊兩條時間序列 |
| `merge_asof` | 找「之前最近」（或最近）的 key | 事件對齊最近一次量測、交易對齊最近報價 |

```python
pd.merge_ordered(aapl, mcd, on="date", suffixes=("_aapl", "_mcd"), fill_method="ffill")

# merge_asof：兩邊都必須依 on 欄排序
pd.merge_asof(events, measurements, on="time")                        # 預設 direction="backward"：之前最近的
pd.merge_asof(events, measurements, on="time", direction="nearest")   # 前後最近
pd.merge_asof(events, measurements, on="time", by="patient_id",       # 在同一位病人內配對
              tolerance=pd.Timedelta("2h"))                            # 超過 2 小時就不配（NaN）
```

`merge_asof` 類似試算表的 `VLOOKUP(..., TRUE)`（近似比對），但能指定方向、分組與容許差距。基因體座標的區間重疊（例如變異落在哪個基因內）不適合用 merge，改用 `pyranges` / `bedtools`。
