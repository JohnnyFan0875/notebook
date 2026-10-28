[Machine Learning](../README.md) › [推薦系統](README.md) › 內容式過濾

# 內容式過濾 (Content-Based Filtering)

使用者喜歡某些項目，就推薦**內容特徵**相近的其他項目。它不看「誰和誰像」，而是看「項目本身長什麼樣」，所以只要項目有足夠的結構化或文字特徵就能運作。

| 適合的資料 | 特徵例子 |
| --- | --- |
| 書籍 | 類型、作者、摘要、關鍵字 |
| 電影 | 類型、演員、導演、劇情介紹 |
| 商品 | 品牌、品類、價格帶、規格 |
| 文章 | 標籤、主題、內文 |

## 流程

```
項目 → 特徵向量（one-hot / TF-IDF / embedding）→ 項目間相似度（cosine）
使用者歷史 → 加權平均成 user profile → 對沒看過的項目算相似度 → 排序取 top-N
```

## 用法

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

books = pd.DataFrame({
    "title": ["The Hobbit", "The Two Towers", "Macbeth", "Foundation",
              "Nudge", "Dune", "Hamlet", "Thinking Fast and Slow"],
    "description": ["fantasy adventure hobbit dragon quest", "fantasy adventure ring war quest",
                    "tragedy king murder ambition play", "science fiction empire galaxy future",
                    "behavioral economics choice decision", "science fiction desert empire future",
                    "tragedy prince revenge play", "behavioral psychology decision bias"],
})

# 1. 項目 → TF-IDF 向量（真實資料常加 min_df / max_df 去掉太罕見與太常見的詞）
tfidf = TfidfVectorizer(stop_words="english")
X = tfidf.fit_transform(books["description"])
item_vec = pd.DataFrame(X.toarray(), index=books["title"], columns=tfidf.get_feature_names_out())

# 2. 項目與項目的相似度
sim = pd.DataFrame(cosine_similarity(item_vec), index=item_vec.index, columns=item_vec.index)
sim.loc["The Hobbit"].drop("The Hobbit").sort_values(ascending=False).head(2)
# The Two Towers 0.51，其他都是 0（沒有共同詞）

# 3. 使用者 profile：依評分加權平均讀過的書
read = pd.Series({"The Hobbit": 5, "Foundation": 3})           # 書名 → 評分
profile = item_vec.loc[read.index].mul(read, axis=0).sum() / read.sum()

# 4. 對沒讀過的書評分排序
candidates = item_vec.drop(read.index)
scores = pd.Series(cosine_similarity(profile.to_numpy().reshape(1, -1), candidates)[0],
                   index=candidates.index).sort_values(ascending=False)
# The Two Towers 0.44、Dune 0.38 → 奇幻與科幻各推一本，比例跟著評分權重
```

| 結構化特徵 | 做法 |
| --- | --- |
| 單選類別 | One-hot |
| 多選（一本書有多個類型） | Multi-hot（`MultiLabelBinarizer`） |
| 數值（價格、年份） | 分箱或標準化後併入 |
| 文字 | TF-IDF；或預訓練的句子 embedding（語意相似而非字面重疊） |

> Cosine 相似度只看向量**方向**，不受長度影響，適合長短不一的稀疏文字特徵。上例中 The Hobbit 與 Macbeth 沒有任何共同詞，相似度剛好為 0：TF-IDF 只抓字面重疊，抓不到「同義但用字不同」。

## 優缺點

| 優點 | 缺點 |
| --- | --- |
| 不需要其他使用者的資料 | 容易困在已知偏好附近（過度專門化） |
| **新項目**只要有特徵就能立刻被推薦 | 非常依賴特徵品質 |
| 推薦理由好解釋（「因為你喜歡奇幻小說」） | 很難推出「意外但有趣」的跨類項目 |
| — | 新**使用者**仍有冷啟動問題 |

> 內容式方法很會回答「和你以前喜歡的相似的還有什麼」，但不擅長回答「你可能會意外喜歡什麼」，後者是 [協同過濾](memory-based-collaborative-filtering.md) 的強項。實務上常兩者混合。
