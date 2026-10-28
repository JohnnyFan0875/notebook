[Data Science](../README.md) › [R Foundations](README.md) › 文字分析

# 文字分析 (Text Analysis with tidytext)

文字分析的第一步不是選模型，而是把「一欄長字串」轉成「一列一個 token」的 tidy 格式，之後就能用熟悉的 `count()`、`join()`、`group_by()` 做詞頻、詞典情緒、tf-idf 與主題模型。生資情境常見的文字資料是 PubMed 摘要、臨床紀錄的自由文字、GEO / SRA 的樣本描述欄位。需要語意理解（同義詞、否定、上下文）時改用 embedding 或 LLM，見 [文字與序列模型](../deep-learning/nlp-and-transformers/text-and-sequence-models.md) 與 [Embeddings 與語意搜尋](../llm/rag/embeddings-and-semantic-search.md)。

## 流程

```
原始文件（一列一篇，含 doc_id 與其他欄位）
  └─ unnest_tokens()            一列一個 token
       └─ anti_join(stop_words)   移除停用詞（+ 資料集專屬停用詞）
            ├─ count()                     詞頻、分組詞頻
            ├─ inner_join(lexicon)         詞典式情緒
            ├─ bind_tf_idf()               各文件的代表詞
            └─ cast_dtm() → LDA()          主題模型
```

## Tokenization 與詞頻

```r
library(tidyverse)
library(tidytext)

tidy_review <- reviews |>                         # 欄位：id, product, stars, review
  unnest_tokens(word, review)                     # 預設轉小寫、去標點

# 停用詞：通用清單 + 資料集專屬的高頻噪音詞
my_stop <- bind_rows(stop_words, tibble(word = c("product", "tablet", "phone")))
tidy_review <- tidy_review |> anti_join(my_stop, by = "word")

tidy_review |> count(word, sort = TRUE)           # 整體詞頻
tidy_review |> count(product, word, sort = TRUE)  # 分組詞頻
```

| `unnest_tokens(token = )` | 單位 | 用途 |
| --- | --- | --- |
| `"words"`（預設） | 單字 | 詞頻、情緒 |
| `"ngrams", n = 2` | 連續 2 個詞 | 片語（`"not good"`、`"gene expression"`） |
| `"sentences"` / `"paragraphs"` | 句、段 | 句子層級分析 |
| `"regex", pattern = ` | 自訂分隔 | 特殊格式 |

> 停用詞清單是**依資料集決定**的前處理選擇。分析 PubMed 摘要時，`"study"`、`"patients"`、`"results"`、`"cells"` 幾乎每篇都有，不加入停用詞就會霸佔所有排行。

需要詞幹還原時用 `SnowballC::wordStem(word)`（`"genes"`、`"gene"` → `"gene"`）。Word cloud（`wordcloud` 套件）只適合快速瀏覽；要比較群組請用長條圖或 tf-idf。

## tf-idf：每份文件的代表詞

詞頻高的詞往往到處都有；tf-idf 給「在這份文件常見、在其他文件少見」的詞高分。

| 量 | 定義 |
| --- | --- |
| tf (term frequency) | 詞在該文件的次數 / 該文件總詞數 |
| idf (inverse document frequency) | ln(文件總數 / 含該詞的文件數)；所有文件都有的詞 idf = 0 |
| tf-idf | tf × idf |

```r
tidy_review |>
  count(product, word) |>
  bind_tf_idf(word, product, n) |>               # term, document, count
  slice_max(tf_idf, n = 10, by = product)        # 每個產品的前 10 個代表詞
```

tf-idf 不需要先移除停用詞也能壓低它們的分數（idf ≈ 0），但移除後結果較乾淨。

## 詞典式情緒分析

把 token 和情緒詞典 join：只保留詞典裡有的詞，附上情緒標籤。

| 詞典 | 內容 | 取得 |
| --- | --- | --- |
| `bing` | positive / negative | `get_sentiments("bing")` |
| `afinn` | −5 到 +5 分數 | `get_sentiments("afinn")`（需 `textdata` 下載） |
| `nrc` | 8 種情緒 + 正負 | `get_sentiments("nrc")`（需 `textdata` 下載） |

```r
sentiment_by_stars <- tidy_review |>
  inner_join(get_sentiments("bing"), by = "word") |>
  count(stars, sentiment) |>
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) |>
  mutate(net = positive - negative,
         stars = fct_reorder(factor(stars), net))   # 依淨情緒排序，畫圖用
```

| 限制 | 例子 |
| --- | --- |
| 不懂否定 | `"not good"` 被算成 positive → 用 bigram 找出 `not` / `no` 開頭的片語修正 |
| 領域不符 | 一般詞典中 `"positive"`、`"cancer"`、`"tumor"` 有情緒，但在醫學文本是中性描述 |
| 長文件偏差 | 詞越多，正負詞都越多 → 用比例或 `net / 總詞數` |

## 主題模型 (LDA)

Latent Dirichlet Allocation 是非監督式模型：每個 **topic** 是詞的機率分布，每份**文件**是多個 topic 的混合。與 clustering 不同，一份文件可以 70% 屬於 topic A、30% 屬於 topic B。

```r
library(topicmodels)

dtm <- tidy_review |>
  count(id, word) |>
  cast_dtm(id, word, n)                          # tidy → DocumentTermMatrix

lda <- LDA(dtm, k = 4, method = "Gibbs", control = list(seed = 42))

# β：每個 topic 中各詞的機率 → 看高機率詞來命名 topic
tidy(lda, matrix = "beta") |> slice_max(beta, n = 10, by = topic)

# γ：每份文件屬於各 topic 的比例 → 可接回 stars、product 等欄位
tidy(lda, matrix = "gamma")
```

| 選 `k` | 做法 |
| --- | --- |
| 看結果 | 增加 `k` 後若出現新的、可區辨的詞群就合理；若只是重複既有 topic 就太多 |
| 指標 | `ldatuning` 的多種指標、held-out perplexity；`stm` 套件的 `searchK()` |
| 穩定性 | 換不同 seed 重跑，topic 是否大致相同 |

> topic 的名稱是分析者看高機率詞後加上的標籤，不是模型給出的客觀主題。報告時列出每個 topic 的代表詞，讓讀者自己判斷。

需要加入文件的共變數（年份、期刊）時，用 `stm`（structural topic model）。

## 生資應用：文獻探勘

```r
# 取得 PubMed 摘要（NCBI E-utilities）
library(rentrez)
ids <- entrez_search(db = "pubmed", term = "single-cell RNA-seq AND fibrosis", retmax = 200)$ids
xml <- entrez_fetch(db = "pubmed", id = ids, rettype = "xml")
# 解析 XML 取得 PMID、年份、摘要 → tibble，再進入上面的 tidytext 流程
```

| 任務 | 做法 |
| --- | --- |
| 某主題的熱門詞 / 趨勢 | tf-idf 依年份分組 |
| 基因與疾病共同出現 | 以基因符號清單 `inner_join` token，再算共現（`widyr::pairwise_count()`） |
| 文獻分群 | LDA，或 embedding + 分群（語意較準） |
| 抽取實體（基因、藥物、疾病） | 字典比對會漏掉別名與誤判縮寫；改用 PubTator 已標註的結果或生醫 NER 模型 |

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 沒保留文件 ID 就 tokenize | 之後無法分組或接回 metadata；先確保每列有 `id` |
| 停用詞只用通用清單 | 加入資料集專屬高頻詞 |
| 只看 word cloud 下結論 | 用詞頻 / tf-idf 長條圖並分組比較 |
| 詞典式情緒當成語意理解 | 處理否定、確認詞典符合領域，或改用模型 |
| LDA 不設 seed | 每次結果不同；`control = list(seed = )` |
| 把 topic 當成硬分類 | 看 γ 的比例，而不是只取最大值 |
