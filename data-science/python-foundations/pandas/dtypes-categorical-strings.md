[Python Foundations](../README.md) › [pandas](README.md) › dtype、類別與字串

# dtype、類別與字串 (Dtypes, Categorical & Strings)

欄位型別錯了，後面的 groupby、merge、統計都會靜靜出錯：數字被讀成字串就無法相加、ID 被讀成數字就掉了前導 0、類別順序錯了圖就亂排。讀檔後第一件事是 `df.dtypes`。

## pandas 的 dtype

| 資料 | 預設 dtype | 可缺值的 dtype（nullable） | 備註 |
| --- | --- | --- | --- |
| 整數 | `int64` | `Int64`（大寫 I） | `int64` 欄只要有一個缺值就變 `float64` |
| 浮點 | `float64` | `Float64` | |
| 布林 | `bool` | `boolean` | `bool` 欄有缺值會變 `object` |
| 字串 | `str`（pandas 3 起） | `string` | 3.0 以前是 `object` |
| 類別 | `category` | 本身可缺值 | 重複值多的欄位 |
| 日期 | `datetime64[ns]` | 本身可缺值（`NaT`） | 見 [日期與時間](../datetime.md#pandas-datetime-欄位) |
| 其他 | `object` | | 混合型別、Python 物件；慢，盡量避免 |

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"a": [1, None], "b": ["x", None], "c": [True, None]})
df.dtypes                     # a: float64、b: str、c: object
df.convert_dtypes().dtypes    # a: Int64、b: string、c: boolean → 統一用 pd.NA 表示缺值
df.info()                     # dtype + 非缺值數 + 記憶體

pd.Series([1, None], dtype="Int64")          # [1, <NA>]：整數保持整數
```

> **pandas 3 的字串**：字串欄預設是 `str` dtype（有裝 pyarrow 時以 Arrow 儲存），不再是 `object`。舊程式碼中 `df["x"].dtype == object` 的判斷要改成 `pd.api.types.is_string_dtype(df["x"])`。

## 轉型

```python
df["x"] = df["x"].astype(float)
df = df.astype({"id": "str", "count": "int64", "group": "category"})

# 1. 有髒值的數字欄：to_numeric 把無法轉的變 NaN
s = pd.Series(["1", "2", "x", None])
pd.to_numeric(s, errors="coerce")            # [1.0, 2.0, nan, nan]
s[pd.to_numeric(s, errors="coerce").isna() & s.notna()]   # 找出是哪些值轉不了 → "x"

# 2. 有缺值的欄轉 int
pd.Series([1.0, np.nan]).astype(int)         # IntCastingNaNError
pd.Series([1.0, np.nan]).astype("Int64")     # [1, <NA>]

# 3. 日期
pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")

# 4. 讀檔時就指定，避免猜錯
pd.read_csv("samples.csv", dtype={"sample_id": "str", "chrom": "category"})
```

| 常見型別陷阱 | 症狀 | 解法 |
| --- | --- | --- |
| ID / 郵遞區號被讀成數字 | `00123` → `123` | 讀檔時 `dtype={"id": str}` |
| 數字欄被讀成字串 | `sum()` 變字串串接、`mean()` 報錯 | `pd.to_numeric(errors="coerce")`，再查哪些值轉不了 |
| 整數欄出現 `.0` | 有缺值，被轉成 float | 用 `Int64` |
| 染色體 `chr10` 排在 `chr2` 前面 | 字串字典序 | 有序 `category` 指定順序 |
| 基因名被 Excel 改成日期 | `SEPT2` → `2-Sep` | 不要用 Excel 開原始檔；見 [匯入資料](../importing-data.md#excel) |
| merge 對不到 | 一邊 `int64` 一邊 `str` | merge 前統一 key 的 dtype |

## 類別 (Categorical)

`category` 用「一份類別清單 + 每列一個整數 code」儲存，適合**重複值多、唯一值少**的欄位（樣本組別、染色體、批次、物種）。好處是省記憶體、可指定順序；ID、自由文字等高基數 (high cardinality) 欄位轉了沒好處。

```python
import seaborn as sns
iris = sns.load_dataset("iris")

iris["species"] = iris["species"].astype("category")
iris["species"].cat.categories               # Index(['setosa', 'versicolor', 'virginica'])
iris["species"].cat.codes                    # 0, 1, 2 的整數 code

# 1. 先把雜亂標籤對應成乾淨標籤，再轉類別
mapping = {"0-15 Min": "short", "16-30 Min": "medium", "30+ Min": "long"}
df["stop_length"] = df["stop_duration"].map(mapping)       # 沒對到的變 NaN：可藉此抓出漏網標籤

# 2. 有序類別：排序、比較、groupby、作圖都依此順序
likert = ["never", "rarely", "sometimes", "often", "always"]
df["freq"] = pd.Categorical(df["freq"], categories=likert, ordered=True)
df.sort_values("freq")
df[df["freq"] >= "often"]                    # 只有 ordered=True 才能比大小
df["freq"].value_counts().sort_index()       # 依類別順序，而非字母

chroms = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY", "chrM"]
df["chrom"] = pd.Categorical(df["chrom"], categories=chroms, ordered=True)

# 3. 管理類別清單
s = s.cat.rename_categories({"setosa": "SETOSA"})
s = s.cat.reorder_categories(["c", "b", "a"], ordered=True)   # 必須列出全部現有類別
s = s.cat.set_categories(["a", "b", "z"])    # 不在新清單的值 → NaN（小心）
s = s.cat.add_categories(["unknown"])
s = s.cat.remove_unused_categories()         # 只修剪清單，不動資料
```

| 方法 | 改動類別清單 | 會把值變 NaN？ |
| --- | --- | --- |
| `rename_categories` | 改名 | 否 |
| `reorder_categories` | 改順序（必須是同一組類別） | 否 |
| `set_categories` | 任意替換 | **會**：不在新清單的值 |
| `remove_unused_categories` | 刪掉沒出現的類別 | 否 |

> 篩掉某類別的列後，它仍留在 `cat.categories` 中。pandas 3 的 `groupby` 預設 `observed=True`（只顯示有出現的類別）；要列出所有類別（含 0 筆）時用 `groupby(..., observed=False)`，作圖或報表才不會漏組。

### 編碼 (Encoding)

```python
iris["species_code"] = iris["species"].cat.codes            # label encoding（0, 1, 2）
pd.get_dummies(iris["species"], dtype=int)                  # one-hot：預設回傳 bool，dtype=int 改成 0/1
pd.get_dummies(iris, columns=["species"], drop_first=True)  # 線性模型避免共線性

# train / test 要有相同的 dummy 欄：先固定類別清單
cats = ["Bella", "Lucy", "Max"]
pd.get_dummies(pd.Categorical(test["name"], categories=cats), dummy_na=True)
```

在建模流程中，編碼要放進 pipeline、只在訓練資料 fit；`get_dummies` 適合探索，建模用 `OneHotEncoder(handle_unknown="ignore")`，見 [類別編碼](../../machine-learning/preprocessing/categorical-encoding.md)。

### 找出不一致的類別

```python
known = {"setosa", "versicolor", "virginica"}
bad = ~iris["species"].isin(known)
iris.loc[bad, "species"].unique()            # 拼錯的值，例如 "setossa"

# 常見清理：大小寫、空白
iris["species"] = iris["species"].str.strip().str.lower()
```

拼字相近但不同的值用模糊比對處理，見 [文字清理與 Regex](../text-cleaning-and-regex.md)。

## 字串操作 (`.str`)

`.str` 對整欄做向量化字串操作，缺值會保留為缺值。

```python
s = pd.Series(["  TP53 ", "brca1", None])

s.str.strip().str.upper()                    # ['TP53', 'BRCA1', nan]
s.str.len()                                  # [7.0, 5.0, nan]
s.str.replace("1", "-1", regex=False)        # 字面取代；regex=True 時用 pattern
s.str.contains("tp", case=False)             # 不分大小寫比對
s.str.startswith("b"), s.str.endswith("3")
s.str[:3]                                    # 前 3 個字元
s.str.pad(8, fillchar="0")                   # 補到固定長度

# 切分與擷取
loc = pd.Series(["chr1:100-200", "chr2:5-9"])
loc.str.split(":", expand=True)              # 兩欄：chr1 | 100-200
loc.str.extract(r"(?P<chrom>chr\w+):(?P<start>\d+)-(?P<end>\d+)")   # 具名群組 → 欄名
pd.Series(["a;b", "c"]).str.split(";").explode()   # 一格多值 → 多列

# 多欄文字一起搜尋：先對每欄建遮罩，再用 | 合併
cols = ["text", "retweeted_text", "quoted_text"]
mask = pd.concat([df[c].str.contains("apple", case=False, na=False) for c in cols], axis=1).any(axis=1)
df[mask]
```

| 想做的事 | 方法 |
| --- | --- |
| 清空白、大小寫 | `strip`、`lower` / `upper` / `title` |
| 取代 | `replace(pat, repl, regex=False)` |
| 判斷 | `contains`、`startswith`、`endswith`、`fullmatch`、`isnumeric` |
| 擷取 | `extract`（第一個符合）、`extractall`（全部） |
| 切分 | `split(expand=True)`、`rsplit(n=1)`、`partition` |
| 長度 / 切片 | `len`、`str[a:b]`、`slice` |
| 串接 | `s1 + "_" + s2`、`s.str.cat(sep=",")` |

> `contains` 預設把 pattern 當 regex：`"v."` 會比對 `v` 後接任意字元。純文字比對加 `regex=False`。缺值在 `str` dtype 下比對結果為 `False`；在 `object` 欄則是 NaN，當遮罩前加 `na=False`。

regex 語法與文字清理流程見 [文字清理與 Regex](../text-cleaning-and-regex.md)。
