# Text Analysis in R

R 做文字分析時，真正的重點通常不是先選模型，而是先把文字整理成可以計數、連接詞典、再進一步建模的結構。`tidytext` 的價值就在這裡：它把文字拆成 tidy data，讓文字分析變成一條和一般 `dplyr` workflow 相容的資料整理流程。

## The Core Mental Model

最常見的文字分析起手式不是直接做 NLP 模型，而是先走這條路：

1. 原始文件或評論
2. tokenization
3. remove stop words
4. count terms
5. 視需求做 sentiment、tf-idf、topic modeling 或 visualization

Key point: 很多文字分析的第一步，其實是把「一欄長字串」轉成「一列一個 token」。

## Text as Tidy Data

在 `tidytext` 的思路裡，最自然的資料形狀通常是：

- 一列代表一個 token
- 保留文件 ID 或群組欄位
- 後續再做 `count()`, `join()`, `group_by()`

如果還停留在整段文字放在單一欄位，你能做的分析會很有限。

## Tokenization with `unnest_tokens()`

`unnest_tokens()` 是最常見的入口。

```r
library(tidytext)

tidy_review <- reviews %>%
  unnest_tokens(word, review)
```

這一步的意思是：

- 把 `review` 欄位拆成單字
- 新增一個叫 `word` 的 token 欄位
- 每個詞的每次出現都各自佔一列

常見直覺：

- token 是「一次出現」
- bag-of-words 是先不管詞序，只保留詞項和次數

## Counting Words

tokenization 之後，最基本的摘要通常就是詞頻。

```r
tidy_review %>%
  count(word, sort = TRUE)
```

如果有分組欄位，也常會一起算：

```r
tidy_review %>%
  count(word, product, sort = TRUE)
```

這類計數是後面很多分析的基礎，因為：

- word cloud 要吃 frequency
- tf-idf 要先有 term count
- sentiment join 後也常要再 count

## Stop Words and `anti_join()`

分析高頻詞前，通常先移掉 stop words。

```r
tidy_review_nostop <- reviews %>%
  unnest_tokens(word, review) %>%
  anti_join(stop_words, by = "word")
```

`anti_join()` 在這裡很好用，因為語意很直接：

- 保留 review tokens
- 移掉出現在 stop word 字典裡的詞

## Custom Stop Words

通用 stop words 往往不夠，因為很多資料集會有自己的高頻噪音詞。

```r
custom_stop_words <- tibble::tribble(
  ~word,
  "tablet",
  "phone",
  "product"
)

stop_words2 <- stop_words %>%
  bind_rows(custom_stop_words)
```

這很重要，因為在特定語境下：

- query 本身
- 品牌名
- 平台術語
- 評論模板詞

都可能變成沒有分析價值但出現很多次的詞。

Key point: stop-word 清單通常不是固定資產，而是資料集特定的建模前處理決策。

## Word Frequency Visualization

完成清理後，最常見的快速視覺化之一是 word cloud。

```r
library(wordcloud)

tidy_review_nostop %>%
  count(word) %>%
  with(
    wordcloud(word, n)
  )
```

Word cloud 適合：

- 快速看高頻詞
- exploratory communication

但不適合：

- 精確比較群組
- 推論重要性
- 替代統計摘要

Warning: 不要只看 word cloud 就下結論。它比較像 exploration，不是完整分析。

## Sentiment Analysis with Lexicons

R 裡最容易上手的 sentiment workflow 是詞典法。

例如 `bing` lexicon：

```r
get_sentiments("bing")
```

它把詞分成：

- positive
- negative

接著可以把 token table 和 sentiment lexicon 連起來：

```r
sentiment_review <- tidy_review_nostop %>%
  inner_join(get_sentiments("bing"), by = "word")
```

這一步的意思不是「模型懂情緒」，而是：

- 只保留出現在情緒詞典裡的詞
- 每個詞附上一個情緒標籤

## Summarizing Sentiment

最常見的下一步是計數與彙總：

```r
sentiment_review %>%
  count(word, sentiment, sort = TRUE)
```

如果有評分、產品或群組欄位，也可以往群組層級聚合：

```r
sentiment_by_rating <- tidy_review %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(stars, sentiment) %>%
  tidyr::pivot_wider(names_from = sentiment, values_from = n) %>%
  mutate(overall_sentiment = positive - negative)
```

這裡的 `overall_sentiment = positive - negative` 是一個很實用的簡單指標：

- 正值代表整體偏正面
- 負值代表整體偏負面

但它仍然只是詞典式近似，不是語意理解。

## Visualizing Sentiment by Group

當文字資料帶有群組欄位，例如評分、產品或來源時，最值得做的不是只看總情緒，而是看不同群組的變化。

```r
sentiment_stars <- tidy_review %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(stars, sentiment) %>%
  tidyr::pivot_wider(names_from = sentiment, values_from = n) %>%
  mutate(
    overall_sentiment = positive - negative,
    stars = forcats::fct_reorder(stars, overall_sentiment)
  )
```

這種做法的好處是，你可以把文字特徵和原本的結構化欄位重新接回來，而不是把文字分析孤立成另一條流程。

## Topic Modeling with `LDA`

如果目標不是判斷正負面，而是找出文件群內部常一起出現的詞組模式，可以走 topic modeling。

### Core Idea

LDA 是一種常見的 topic model。

幾個關鍵直覺：

- corpus: 一組文件
- bag-of-words: 先不看詞序，只看詞項與次數
- topic: 一組常一起出現的詞
- document: 可以是多個 topic 的混合

Key point: topic modeling 是 unsupervised learning。它找的是詞彙共現結構，不是在預測標籤。

## Topic Modeling vs Clustering

這兩者容易被混在一起，但邏輯不太一樣：

- clustering 常把每個物件分到單一群
- topic modeling 允許每份文件同時混合多個 topic

所以 topic modeling 比較像是在說：

- 這份文件有多少比例像 topic A
- 又有多少比例像 topic B

而不是只給一個單一 cluster label。

## From Tidy Tokens to `DocumentTermMatrix`

LDA 前常需要把 tidy token counts 轉成 document-term matrix。

```r
dtm_review <- tidy_review_nostop %>%
  count(id, word) %>%
  cast_dtm(id, word, n)
```

這一步很重要，因為它把 tidy format 重新轉回 topic model 常吃的矩陣格式。

## Running `LDA()`

```r
library(topicmodels)

lda_out <- LDA(
  dtm_review,
  k = 2,
  method = "Gibbs"
)
```

這裡最重要的設定之一是 `k`，也就是 topic 數量。

實務上可以先這樣理解：

- topic 太少：不同主題會被混在一起
- topic 太多：開始出現重複 topic 或過度碎裂

一個很實用的判斷原則是：

- 新增 topic 如果帶來新的、有區辨力的詞群，通常合理
- 如果只是重複既有 topic，通常已經太多

## Interpreting Topics

跑完模型後，通常會看每個 topic 的高機率詞。

```r
lda_topics <- tidy(lda_out, matrix = "beta")
```

接著常會取每個 topic 機率最高的幾個詞來命名：

```r
word_probs <- lda_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 10)
```

命名 topic 本質上是人工解讀工作，不是模型直接給你的真理。

Warning: topic 的名字是 analyst 加上去的。它應該被當成方便理解的標籤，而不是客觀存在的唯一主題。

## Common Mistakes

- 還沒 tokenization 就急著做模型。
- 把 stop words 當固定清單，不隨資料集調整。
- 只看 word cloud 就直接解讀文本主題。
- 把詞典式 sentiment 當成真正的語意理解。
- 把 topic model 的輸出當成明確分類，而不是機率混合。
- `k` 只憑感覺亂設，沒有檢查是否開始重複 topic。

## Practical Workflow

一條很穩的 R 文字分析入門路徑通常是：

1. 用 `unnest_tokens()` 把文字拆成 tidy tokens
2. 用 `anti_join(stop_words)` 移掉通用 stop words
3. 視資料集加入 custom stop words
4. 用 `count()` 先看詞頻與群組差異
5. 如果要做情緒分析，`inner_join(get_sentiments("bing"))`
6. 如果要做主題分析，`count(id, word)` 後 `cast_dtm()` 再跑 `LDA()`
7. 最後才做視覺化與解讀
