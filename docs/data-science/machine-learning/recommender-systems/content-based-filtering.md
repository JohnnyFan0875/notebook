# Content-Based Filtering

content-based filtering 的核心想法是：如果使用者喜歡某些 item，就推薦在內容特徵上和它們相近的其他 items。

它不像 collaborative filtering 先看「誰和誰像」，而是先看「item 本身長什麼樣」。

## 什麼資料適合做 Content-Based

最常見的是 item metadata 足夠完整的場景，例如：

- 書籍：genre、作者、摘要、關鍵字
- 電影：類型、演員、導演、劇情介紹
- 商品：品牌、品類、價格帶、規格
- 文章：標籤、主題、內文摘要

Key point: 如果 item 幾乎沒有結構化或文字特徵，content-based 方法就很難發揮。

## 把 Item 變成向量

最基本的做法是先把 item 表示成 feature vector。

### 結構化屬性

如果是明確欄位，可以直接 one-hot 或 multi-hot：

```python
item_features = pd.DataFrame(
    {
        "adventure": [1, 0, 0],
        "fantasy": [1, 0, 1],
        "tragedy": [0, 1, 0],
    },
    index=["The Hobbit", "Macbeth", "The Two Towers"],
)
```

### 文字欄位

如果特徵主要來自摘要、描述或標籤文本，常見起點是 `TfidfVectorizer`。

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(min_df=2, max_df=0.7)
X = tfidf.fit_transform(book_summary_df["description"])

tfidf_df = pd.DataFrame(
    X.toarray(),
    index=book_summary_df["title"],
    columns=tfidf.get_feature_names_out(),
)
```

`min_df` 和 `max_df` 的直覺是：

- `min_df`: 太罕見的詞先忽略，降低噪音
- `max_df`: 太常見的詞先忽略，降低低資訊量字詞的主導性

## Item-to-Item Similarity

一旦每個 item 都成了向量，就可以直接算 item similarity。

最常見的相似度是 cosine similarity。

```python
from sklearn.metrics.pairwise import cosine_similarity

sim = cosine_similarity(tfidf_df)
sim_df = pd.DataFrame(sim, index=tfidf_df.index, columns=tfidf_df.index)
```

查某一本書最像哪些書：

```python
similar_books = sim_df.loc["The Hobbit"].sort_values(ascending=False)
```

Key point: cosine similarity 看的是向量方向是否接近，不太受向量長度本身影響，因此很適合稀疏文字特徵。

## 從 User History 建 User Profile

content-based recommendation 很實用的一步是把 user 已經喜歡或看過的 items 聚合成一個 profile vector。

```python
books_read = ["The Hobbit", "Foundation", "Nudge"]
user_books = tfidf_df.reindex(books_read)

user_profile = user_books.mean(axis=0)
```

這個 `user_profile` 可以被理解成：

- 這個使用者在哪些主題詞上偏高
- 他已讀項目在 feature space 裡的大致中心

如果有評分或互動強度，也可以做加權平均，而不是單純平均：

```python
weights = pd.Series([5, 4, 2], index=books_read)
user_profile = user_books.mul(weights, axis=0).sum(axis=0) / weights.sum()
```

這通常比「每本書一票」更合理。

## 給單一使用者找推薦

建好 user profile 之後，就可以對還沒看過的 items 算 similarity。

```python
non_user_books = tfidf_df.drop(books_read, axis=0)

scores = cosine_similarity(
    user_profile.values.reshape(1, -1),
    non_user_books,
)

score_df = pd.DataFrame(
    scores.T,
    index=non_user_books.index,
    columns=["similarity_score"],
).sort_values("similarity_score", ascending=False)
```

這就是最常見的 content-based top-N recommendation pattern。

## Content-Based 的優點

- 不需要其他使用者資料就能運作
- 新 item 只要 metadata 完整，就能立刻進入推薦
- 推薦理由通常比較容易解釋

這使它特別適合 cold-start item 場景。

## Content-Based 的限制

- 容易把人困在已知偏好附近
- 非常依賴 metadata 品質
- 很難只靠內容特徵學到「意外但有趣」的跨類推薦

Key point: content-based 很會回答「和你以前喜歡的東西相似的還有什麼」，但不一定擅長回答「你可能會意外喜歡什麼」。

## Practical Reminders

- 特徵工程比模型本身更影響結果。
- 先確認 item features 是否穩定、可解釋、能持續更新。
- 有 rating 時，user profile 最好考慮權重，不要只做簡單平均。

[Back to Recommender Systems](README.md)
