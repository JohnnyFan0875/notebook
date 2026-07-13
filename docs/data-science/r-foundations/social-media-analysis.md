# Social Media Analysis in R

R 做社群資料分析時，真正的難點通常不是畫圖，而是先把 tweet metadata、文字內容、互動關係與地理欄位整理成可分析的形式。這類 workflow 很適合用 `rtweet` 抓資料，再依問題拆成過濾、文字處理、network、sentiment 與 geolocation 幾條支線。

## Core Data Source: `rtweet`

最常見的起點是 `rtweet::search_tweets()`：

```r
library(rtweet)

tweets <- search_tweets(
  "#google",
  n = 18000,
  include_rts = FALSE
)
```

常用參數包括：

- `n`：想抓多少筆 tweet
- `include_rts`：是否保留 retweets
- `lang`：限制語言，例如 `lang = "en"`

```r
tweets_en <- search_tweets(
  "brand marketing",
  lang = "es"
)
```

Key point: 抓 tweet 前先決定你要研究的是原創內容、擴散內容、還是整個話題流。這會直接影響後面的結果。

## Query Design Matters

Twitter 查詢本身就帶有資料清理效果。若只想看原創 tweet，可以在 query 或結果上過濾：

- `-filter:retweets`
- `-filter:quote`
- `-filter:replies`

若想抓高互動內容，也可以在 query 加條件：

- `min_faves:100`
- `min_retweets:50`

這些條件不是分析後的小修飾，而是定義資料集邊界的一部分。

## Original Tweets vs Amplified Content

社群分析常要先區分：

- original tweets：原創貼文
- retweets：轉發擴散
- quotes：帶評論的轉貼
- replies：回覆互動

如果研究的是內容主題或品牌訊息，先排除 retweet / quote / reply 通常比較容易避免重複訊號；如果研究的是傳播結構，反而應該保留 retweet。

在 `rtweet` 輸出裡，這些欄位與旗標很值得先檢查：

- `is_retweet`
- `is_quote`
- `reply_to_status_id`
- `retweet_count`
- `favorite_count`
- `screen_name`
- `followers_count`
- `friends_count`

## Simple User-Level Diagnostics

即使還沒進到 network analysis，tweet metadata 本身也能提供一些初步判讀。

例如：

- `retweet_count` / `favorite_count`：內容互動熱度
- `followers_count`：潛在觸及規模
- `friends_count`：追蹤他人的規模

一些資料會進一步把使用者彙總成帳號層級，再比較 followers 與 friends：

```r
tweet_fit %>%
  group_by(screen_name) %>%
  summarize(
    follower = mean(followers_count),
    friend = mean(friends_count)
  )
```

這類比值只能當粗略線索，不能直接等同 influence。很多品牌號、媒體號與新帳號的追蹤結構很不一樣。

## Text Cleaning Workflow

tweet text 很 noisy，常混有：

- URL
- hashtags
- mentions
- HTML artifacts，例如 `amp`
- 表情符號
- 多餘空白
- stop words

這門課採用的是傳統 `tm` 流程，核心步驟很值得記住：

```r
tweets_df <- search_tweets("Obesity", n = 1000, include_rts = FALSE, lang = "en")
twt_txt <- tweets_df$text

twt_corpus <- Corpus(VectorSource(twt_txt))
twt_corpus_lwr <- tm_map(twt_corpus, tolower)
twt_corpus_stpwd <- tm_map(twt_corpus_lwr, removeWords, stopwords("english"))
twt_corpus_final <- tm_map(twt_corpus_stpwd, stripWhitespace)
```

實務上這個順序通常還會補上：

- 移除 URL
- 移除標點符號
- 移除數字
- 移除 topic-specific 無意義高頻字

例如：

```r
custom_stop <- c("obesity", "can", "amp", "one", "like", "will", "just")
twt_corpus_refined <- tm_map(twt_corpus_final, removeWords, custom_stop)
```

Key point: 社群文字的 stop words 不只是一份通用英文字表，還常包含 query 本身、平台噪音字與事件特有高頻詞。

## Corpus to DTM

文字清理後，下一步通常是建立 document-term matrix：

```r
dtm <- DocumentTermMatrix(twt_corpus_refined)
rowTotals <- apply(dtm, 1, sum)
tweet_dtm_new <- dtm[rowTotals > 0, ]
```

這一步很重要，因為：

- 空文件要先移掉
- 後續 topic modeling 要吃 DTM
- 很多文字摘要都建立在 term frequency 上

## Quick Visual Summaries

最簡單的視覺摘要是 word cloud：

```r
library(wordcloud)

wordcloud(
  twt_corpus_refined,
  min.freq = 20,
  max.words = 100,
  colors = "red"
)
```

word cloud 適合快速看高頻詞，但不適合做精確比較。若要判讀主題差異、時間差異或群組差異，最好回到結構化的 term counts。

## Topic Modeling with LDA

清理後的 tweet corpus 可以直接進 `topicmodels::LDA()`：

```r
library(topicmodels)

lda_5 <- LDA(tweet_dtm_new, k = 5)
terms(lda_5, 10)
```

這類模型適合：

- 從大量 tweet 摘出幾個主題簇
- 看事件討論是否集中在少數幾個方向
- 做探索式主題摘要

但要小心：

- tweet 很短，topic 通常比長文章更不穩
- 清理規則會大幅影響 topic quality
- `k` 的選擇沒有唯一正解

## Sentiment Analysis

社群情緒分析在 R 裡很常直接用詞典法起步，例如 `syuzhet` 的 NRC lexicon：

```r
twts_galxy <- search_tweets(
  "galaxy fold",
  n = 5000,
  lang = "en",
  include_rts = FALSE
)

library(syuzhet)
sa_value <- get_nrc_sentiment(twts_galxy$text)
score <- colSums(sa_value)
score_df <- data.frame(score)
sa_score <- cbind(sentiment = row.names(score_df), score_df, row.names = NULL)
```

常見輸出包含：

- `anger`
- `anticipation`
- `fear`
- `joy`
- `sadness`
- `trust`
- `negative`
- `positive`

接著可以直接用長條圖呈現：

```r
ggplot(sa_score, aes(x = sentiment, y = score, fill = sentiment)) +
  geom_bar(stat = "identity") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

詞典法的優點是快、容易解釋；缺點是容易忽略反諷、語境、縮寫與平台俚語。

## Retweet Networks

如果研究的是擴散結構，而不是文字內容，可以把 retweet 關係轉成 edge list：

```r
twts_OOTD <- search_tweets("#OOTD", n = 18000, include_rts = TRUE)

rt_df <- twts_OOTD[, c("screen_name", "retweet_screen_name")]
rt_df_new <- rt_df[complete.cases(rt_df), ]
matrx <- as.matrix(rt_df_new)

library(igraph)
nw_rtweet <- graph_from_edgelist(el = matrx, directed = TRUE)
```

這裡的直覺可以理解成：

- source：轉發者
- target：被轉發的帳號
- edge direction：資訊或注意力流向

之後才考慮 degree centrality、betweenness、followers 等節點屬性。

## Geolocation Is Sparse and Messy

tweet 地理資訊來源可能包括：

- tweet text
- user profile
- Twitter Place
- precise coordinates

但這些來源可靠度不同。課程裡特別提醒兩件事：

- `Place` 常是使用者從預定清單中選的區域，通常帶 bounding box，不一定是發文精確位置
- 精確 GPS 座標只佔少數 tweet，常見說法大約只有 `1-2%`

在 `rtweet` 裡可先用：

```r
pol <- search_tweets("#politics", n = 18000)
pol_coord <- lat_lng(pol)
pol_geo <- na.omit(pol_coord[, c("lat", "lng")])
```

再簡單疊到地圖上：

```r
map(database = "state", fill = TRUE, col = "light yellow")
with(pol_geo, points(lng, lat, pch = 20, cex = 1, col = "blue"))
```

Key point: 地圖上看到的是可取得座標的 tweet，不是整個話題的完整地理分布。

## A Practical Workflow

實務上可以把社群資料分析拆成這個順序：

1. 先決定研究問題是內容、情緒、擴散、還是地理分布。
2. 用 `search_tweets()` 設計合理 query，先定義資料集邊界。
3. 用 metadata 過濾 retweet / quote / reply 與語言。
4. 若做文字分析，先清理 text，再建 corpus / DTM。
5. 若做擴散分析，把使用者互動整理成 edge list。
6. 若做 geospatial 分析，先確認座標來源與缺值比例。
7. 最後才畫圖與解釋。

## Common Mistakes

- 把 search query 當成小事，結果資料集一開始就混入不該進來的 tweet。
- 同時分析 original tweet 和 retweet，卻沒有區分兩者的商業意義。
- 直接看 word cloud 就下結論，沒有回到 token / frequency 結構。
- 把詞典式 sentiment score 當成真實情緒強度。
- 看見地圖點位就以為那是精確發文位置。
- 用 follower 數直接代表影響力，忽略 retweet 結構與互動型態。
