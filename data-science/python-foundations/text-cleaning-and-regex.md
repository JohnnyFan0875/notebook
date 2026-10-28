[Data Science](../README.md) › [Python Foundations](README.md) › 文字清理與正規表示式

# 文字清理、正規表示式與模糊比對 (Text Cleaning, Regex & Fuzzy Matching)

文字欄位有固定但不完全規則的格式時（樣本名稱、基因座、檔名、問卷自由填答），用 regex 擷取、驗證、取代與切分；拼字不一致時用模糊比對 (fuzzy matching)。Shell 的 glob / `grep` regex 對照見 [Regex and Wildcard](../../computing/operating-system/regex-wildcard.md)；pandas 的 `.str` 向量化字串操作見 [dtype、類別與字串](pandas/dtypes-categorical-strings.md)。

## 先選對工具

| 需求 | 用 | 不必用 regex |
| --- | --- | --- |
| 固定字串取代 | `s.replace("a", "b")` | ✓ |
| 前後綴檢查 | `startswith()` / `endswith()` | ✓ |
| 是否包含 | `"x" in s` | ✓ |
| 依固定分隔符切 | `s.split("\t")` | ✓ |
| 有模式的擷取 / 驗證 / 取代 | `re` | |
| 已有結構化格式（URL、JSON、HTML、VCF） | 專用 parser（`urllib.parse`、`json`、BeautifulSoup、`pysam`） | ✓ |
| 拼字不一致、錯字 | `rapidfuzz` / `thefuzz` | |

## `re` 主要函式

```python
import re

re.search(r"\d+", "Order number: 48291").group()   # '48291'：任意位置第一個符合
re.match(r"\d+", "123abc").group()                 # '123'：只從開頭比
re.match(r"\d+", "abc123")                         # None
re.fullmatch(r"S\d{3}", "S012")                    # 整個字串都要符合（驗證格式用這個）
re.findall(r"\d+", "3 cats and 14 dogs")           # ['3', '14']
re.sub(r"\d", "X", "02-123-4567")                  # 'XX-XXX-XXXX'
re.split(r"[,;\s]+", "a, b;c  d")                  # ['a', 'b', 'c', 'd']
[m.span() for m in re.finditer(r"ATG", "ATGCATG")] # [(0, 3), (4, 7)]：需要位置時

pat = re.compile(r"chr(\d+|[XYM]):(\d+)-(\d+)")    # 同一 pattern 重複使用時先 compile
pat.findall("chr1:100-200 chrX:5-9")               # [('1', '100', '200'), ('X', '5', '9')]
```

> regex 一律寫成 raw string `r"..."`：`\` 在 Python 字串與 regex 都有特殊意義，raw string 免去雙重跳脫。

## 語法速查

| 類別 | 符號 | 意義 |
| --- | --- | --- |
| 字元類別 | `\d` / `\w` / `\s` | 數字 / 英數字與底線 / 空白；大寫 `\D` `\W` `\S` 為反集合 |
| | `.` | 任意字元（換行除外） |
| | `[A-Za-z]`、`[ACGT]` | 自訂集合 |
| | `[^0-9]` | 排除集合 |
| 次數 | `+` / `*` / `?` | 1 次以上 / 0 次以上 / 0 或 1 次 |
| | `{m}` / `{m,n}` / `{m,}` | 剛好 m / m 到 n / 至少 m 次 |
| | `+?`、`*?` | non-greedy：盡量少吃 |
| 位置 | `^` / `$` | 開頭 / 結尾 |
| | `\b` | 單字邊界 |
| 群組 | `(...)` | 分組並擷取 |
| | `(?:...)` | 只分組不擷取 |
| | `(?P<name>...)` | 具名群組 |
| | `\1`、`(?P=name)` | 反向參照 (backreference) |
| | `a\|b` | 或 (alternation) |
| 環視 | `(?=...)` / `(?!...)` | 後面是 / 不是…（不消耗字元） |
| | `(?<=...)` / `(?<!...)` | 前面是 / 不是… |

| 旗標 | 作用 |
| --- | --- |
| `re.IGNORECASE` / `re.I` | 不分大小寫 |
| `re.MULTILINE` / `re.M` | `^` `$` 對每一行生效 |
| `re.DOTALL` / `re.S` | `.` 也匹配換行 |
| `re.VERBOSE` / `re.X` | 允許在 pattern 內換行加註解 |

```python
re.findall(r"colou?r", "color colour")             # ['color', 'colour']
re.findall(r"www[^0-9]+com", "www.example.com www3example.com")   # ['www.example.com']
re.findall(r"^the\s\d+s", "the 3s are here")       # ['the 3s']：錨定開頭
re.findall(r"\bgene\b", "gene genes subgene")      # ['gene']：只要完整單字
```

## 群組與擷取

```python
text = "Clary has 2 friends, Susan has 3 brothers"
re.findall(r"([A-Za-z]+)\s\w+\s(\d+)\s(\w+)", text)
# [('Clary', '2', 'friends'), ('Susan', '3', 'brothers')]：多個群組 → tuple

m = re.search(r"(\d{1,2})-(\d{2})-(\d{4})", "The date is 12-05-2024.")
m.group(0), m.group(3)                             # '12-05-2024', '2024'

re.findall(r"(\d+)(?:st|nd|rd|th)", "21st and 22nd")   # ['21', '22']：(?:) 不產生多餘群組
re.findall(r"\d+\s(cat|dog)", "1 cat 2 dog")       # ['cat', 'dog']：| 要用括號限定範圍

m = re.search(r"(?P<sample>S\d+)_(?P<rep>R\d)", "run3_S012_R2.fastq.gz")
m.group("sample"), m.groupdict()                   # 'S012', {'sample': 'S012', 'rep': 'R2'}

re.sub(r"(\w+)\s\1", r"\1", "go go stop")          # 'go stop'：反向參照抓重複字
re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", "2024-03-15")   # '15/03/2024'：取代時重排
re.findall(r"\d+(?=\s?mg)", "dose 50 mg, 20mg")    # ['50', '20']：lookahead 只取數字
```

pandas 對應：`s.str.extract(r"(?P<sample>S\d+)_(?P<rep>R\d)")` 直接把具名群組展開成欄位。

### Greedy vs Non-greedy

```python
s = "www.example.com and www.test.com"
re.findall(r"www.+com", s)       # ['www.example.com and www.test.com']：greedy 吃到最後一個 com
re.findall(r"www.+?com", s)      # ['www.example.com', 'www.test.com']
```

> 很多 regex bug 來自 greedy：`.*` 會吃到最遠的符合處。抓括號、引號、標籤內容時用 `.*?` 或排除集合 `[^"]*`。

## 實務範例

```python
# 解析 FASTQ 檔名（Illumina 慣例）
fname = "Tumor01_S3_L001_R1_001.fastq.gz"
m = re.fullmatch(r"(?P<sample>.+)_S(?P<num>\d+)_L(?P<lane>\d{3})_R(?P<read>[12])_001\.fastq\.gz", fname)
m.groupdict()          # {'sample': 'Tumor01', 'num': '3', 'lane': '001', 'read': '1'}

# 清理樣本標籤：統一大小寫、空白、分隔符
def clean_label(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[\s\-\.]+", "_", s)    # 空白、-、. → _
    return re.sub(r"_+", "_", s)        # 連續底線合併

clean_label("  Tumor - 01 ")            # 'tumor_01'

# 驗證 Ensembl gene ID（含可選的版本號）
re.fullmatch(r"ENSG\d{11}(\.\d+)?", "ENSG00000141510.17") is not None   # True
re.sub(r"\.\d+$", "", "ENSG00000141510.17")                              # 去版本號再 join

# 找 DNA motif：重疊的符合要用 lookahead
re.findall(r"(?=(ATA))", "ATATA")       # ['ATA', 'ATA']；re.findall(r"ATA", ...) 只會找到 1 個
```

> 合併不同來源的基因表時，ID 版本號（`.17`）、大小寫、別名（gene symbol 會改名）是最常見的 join 失敗原因；symbol 對應建議用 HGNC / Ensembl 的對照表，不要靠 regex 或模糊比對猜。

## 模糊比對 (Fuzzy Matching)

用字串相似度處理錯字與拼法差異（問卷填答、手動輸入的類別）。分數 0–100，100 為完全相同。

| 函式 | 特性 | 適用 |
| --- | --- | --- |
| `fuzz.ratio` | Levenshtein 編輯距離比例 | 長度相近的錯字 |
| `fuzz.partial_ratio` | 最佳子字串比對 | 一邊是另一邊的子字串 |
| `fuzz.token_sort_ratio` | 先把字詞排序 | 字詞順序不同（"New York" vs "York New"） |
| `fuzz.token_set_ratio` | 忽略重複字詞 | 一邊多了額外字詞 |
| `fuzz.WRatio` | 綜合上述的加權分數 | 不確定時的預設 |

```python
# rapidfuzz：C++ 實作、比 thefuzz（舊名 fuzzywuzzy）快很多，API 幾乎相同
from rapidfuzz import fuzz, process

fuzz.ratio("Reeding", "Reading")                  # ≈ 85.7
process.extract("Bobo", ["Alice", "Bob", "Eve"], scorer=fuzz.WRatio, limit=2)
# [('Bob', 85.7..., 1), ...]：(候選, 分數, 索引)

# 把錯字對應回標準類別：先列出標準值，逐一比對「唯一值」而不是每一列
canonical = ["setosa", "versicolor", "virginica"]
observed = df["species"].str.strip().str.lower().unique()

mapping = {}
for value in observed:
    best, score, _ = process.extractOne(value, canonical, scorer=fuzz.WRatio)
    mapping[value] = best if score >= 90 else None  # 低於門檻設 None，留給人工檢查

mapping                                            # {'setosa': 'setosa', 'setossa': 'setosa', ...}
df["species_clean"] = df["species"].str.strip().str.lower().map(mapping)
df.loc[df["species_clean"].isna(), "species"].unique()   # 需要人工確認的值
```

| 原則 | 原因 |
| --- | --- |
| 比對前先標準化（`lower()`、`strip()`、統一分隔符） | 很多「錯字」其實只是大小寫或空白 |
| 對**標準清單**比對，不要彼此互比 | 避免把兩個錯字合併成新類別 |
| 門檻後人工檢視替換表 | 相似度高不代表同義（`BRCA1` vs `BRCA2` 分數很高） |
| 已知的常見錯誤寫成 dict 對照表 | 可重現、可審查，比每次跑模糊比對可靠 |
