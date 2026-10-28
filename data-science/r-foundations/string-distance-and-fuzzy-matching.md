[Data Science](../README.md) › [R Foundations](README.md) › 字串距離與模糊比對

# 字串距離與模糊比對 (String Distance and Fuzzy Matching)

regex 回答「符不符合某個模式」；字串距離回答「兩個字串**有多接近**」。用在人工輸入的拼錯、同一實體的多種寫法（醫院名、組織部位、藥名）、兩份樣本表的 ID 不完全一致等情境。工具是 `stringdist`（計算距離）與 `fuzzyjoin`（近似 join）。Python 版（rapidfuzz）見 [文字清理與正規表示式](../python-foundations/text-cleaning-and-regex.md#模糊比對-fuzzy-matching)。

> **生物 ID 不要用模糊比對**：`CD4` 與 `CD8`、`IL6` 與 `IL6R` 的編輯距離只有 1，卻是完全不同的基因。基因別名要用對照表：`HGNChelper::checkGeneSymbols()`、`AnnotationDbi::mapIds(org.Hs.eg.db, keys, "SYMBOL", "ALIAS")`，見 [匯入資料](importing-data.md)。

## 距離方法

| 方法 | `method =` | 計算什麼 | 適合 |
| --- | --- | --- | --- |
| Levenshtein | `"lv"` | 插入、刪除、替換的最少次數 | 一般打字錯誤 |
| Optimal String Alignment | `"osa"`（預設） | 同上 + 相鄰字元交換，每段子字串只能編輯一次 | 打字時常見的 `teh` → `the` |
| Damerau-Levenshtein | `"dl"` | 同上，無限制 | 同上，數學上正確的距離 |
| Hamming | `"hamming"` | 等長字串中不同位置的數目 | 等長條碼、UMI、index 序列 |
| q-gram | `"qgram"` | 長度 q 片段的出現次數差異總和 | 較長字串、詞序變動 |
| Jaccard | `"jaccard"` | 1 − 片段集合交集 / 聯集 | 同上，結果在 0–1 |
| Cosine | `"cosine"` | 片段次數向量的 1 − cosine 相似度 | 同上 |
| Jaro-Winkler | `"jw"`（`p = 0.1`） | 共同字元與順序，前綴相同加分 | 人名、短字串；結果在 0–1 |

```r
library(stringdist)

stringdist("saturday", "sunday", method = "lv")    # 3
stringdist("ab", "ba", method = c("lv"))            # 2：兩次替換
stringdist("ab", "ba", method = "osa")              # 1：一次交換
stringdist("ca", "abc", method = "osa")             # 3
stringdist("ca", "abc", method = "dl")              # 2：dl 允許交換後再插入

qgrams("Honolulu", "Hanolulu", q = 2)               # 列出每個 bigram 的次數
stringdist("Honolulu", "Hanolulu", method = "qgram", q = 2)    # 4
stringdist("Honolulu", "Hanolulu", method = "jaccard", q = 2)  # 0.5：交集 4 / 聯集 8

stringdistmatrix(c("liver", "livr"), c("liver", "lung"))       # 全部兩兩距離矩陣
stringsim("liver", "livr", method = "jw")           # 相似度（1 − 正規化距離），0–1
```

| 選擇原則 | |
| --- | --- |
| 短字串、單字母錯字 | `osa` / `dl` |
| 長字串、片段相似、詞序可能不同 | `qgram` / `jaccard` / `cosine` |
| 人名 | `jw` |
| 不同長度的字串要比較 | 用 `stringsim()` 或除以長度，絕對距離對長字串不公平 |

> 沒有「最好」的距離：選方法等於定義「什麼叫相似」，先看資料裡實際出現的是哪種錯誤。

## 找最接近的候選：`amatch()`

```r
canonical <- c("liver", "lung", "kidney", "heart")

amatch("livr", canonical)                       # NA！預設 maxDist = 0.1，任何錯字都不接受
amatch("livr", canonical, maxDist = 1)          # 1：對應到 "liver"
canonical[amatch(c("Lung ", "kidny", "brain"), canonical, maxDist = 1)]
# NA "kidney" NA：大小寫與空白也算差異 → 先標準化；brain 沒有候選 → 保持 NA
```

**對唯一值比對**而不是每一列：先 `unique(x)` 建出「原值 → 標準值」對照表，人工檢查後再 join 回去。

## 模糊 join：fuzzyjoin

```r
library(fuzzyjoin)

# 單欄字串距離
stringdist_left_join(lab_samples, registry, by = "sample_name",
                     method = "osa", max_dist = 1, distance_col = "dist")

# 多條件：名稱相近 且 日期差 ≤ 3 天
fuzzy_left_join(
  visits, records,
  by = c("patient" = "patient", "date" = "date"),
  match_fun = list(
    \(a, b) stringdist(a, b, method = "jw") < 0.1,
    \(a, b) abs(as.numeric(a - b)) <= 3
  )
)
```

| fuzzyjoin 函式 | 比對方式 |
| --- | --- |
| `stringdist_*_join()` | 字串距離 |
| `regex_*_join()` | 一邊是 regex pattern |
| `difference_*_join()` | 數值差 ≤ `max_dist` |
| `interval_*_join()` | 區間重疊（基因組座標通常改用 `GenomicRanges::findOverlaps()`） |
| `fuzzy_*_join()` | 每欄自訂 `match_fun` |

> fuzzy join 會產生**一對多**：一筆可能同時符合多個候選。join 後檢查列數，對每筆只保留距離最小者，並人工審核距離 > 0 的配對。

## 工作流程

```
原始字串
  └─ 1. 標準化：str_to_lower()、str_squish()、移除標點與固定前後綴（regex）
     2. 完全相符的直接配對
     3. 剩下的唯一值 → 算距離、取最近候選、設定閾值
     4. 輸出「原值 → 建議值 → 距離」表，人工確認高風險配對
     5. 把確認後的對照表存檔，之後的資料直接 join（可重現、可審查）
```

標準化步驟見 [正規表示式](regular-expressions.md)。

## 常見錯誤

| 錯誤 | 後果 / 修正 |
| --- | --- |
| 跳過標準化直接算距離 | `"Liver "` 和 `"liver"` 距離 2；先清理 |
| `amatch()` 沒設 `maxDist` | 預設 0.1 → 幾乎全部 `NA` |
| 閾值太寬 | 錯誤配對（`lung` ↔ `lungs`？`CD4` ↔ `CD8`！） |
| 長短字串用同一個絕對閾值 | 用正規化相似度或依長度調整 |
| 只靠名稱相似 | 加上日期、數值、地區等條件共同判斷 |
| 每次分析都重新模糊比對 | 結果可能隨候選清單改變；把確認過的對照表存下來 |
