[Data Science](../README.md) › [Network Analysis](README.md) › 二分網路與時間演變

# 二分網路與時間演變 (Bipartite and Evolving Networks)

很多真實網路一開始是兩類實體的關係（客戶–商品、學生–論壇、作者–論文、基因–疾病、細胞–基因、藥物–標靶），直接當一般網路看會漏掉分組結構的意義。網路也會隨時間改變，需要把時間切片後比較。

## 二分網路 (Bipartite Graph)

兩組不同類型的節點，邊只跨組、不在同組內直接相連。關係是透過另一組實體間接產生的，所以 projection、centrality 與過濾都必須尊重這個分工。

| 例子 | 組 U | 組 V | 邊 |
| --- | --- | --- | --- |
| 電商 | 客戶 | 商品 | 購買 |
| 論壇 | 學生 | 論壇 | 發文 |
| 生醫 | 基因 | 疾病 | 已知關聯（DisGeNET） |
| 藥理 | 藥物 | 蛋白質標靶 | 結合（DrugBank、ChEMBL） |
| 文獻 | 作者 | 論文 | 共同署名 |

```python
import networkx as nx
from networkx.algorithms import bipartite

B = nx.Graph()
B.add_nodes_from(df["gene"].unique(), bipartite="gene")      # 用 node attribute 標記分組
B.add_nodes_from(df["disease"].unique(), bipartite="disease")
B.add_edges_from(df[["gene", "disease"]].itertuples(index=False, name=None))

genes = {n for n, d in B.nodes(data=True) if d["bipartite"] == "gene"}
bipartite.is_bipartite(B)                                     # True
bipartite.degree_centrality(B, genes)                         # 分母用對面組的大小
```

從 DataFrame 建圖的關鍵是 schema：哪些欄是節點身分、哪些是 metadata、每一列代表一次互動、一篇貼文還是一次共同出現。列的意義不清楚，圖從第一步就會建錯。注意兩組節點名稱若可能重複（基因與疾病都有 `"ALS"`），要加前綴區分。

> 二分網路中一側節點的最大可能連結數是**另一側**的節點數。直接用一般的 `nx.degree_centrality()` 會用錯分母，比較時要用 `bipartite.degree_centrality`。

## Projection：重新定義 edge

projection 保留一側節點，兩個節點只要共同連到另一側的某個節點就相連。

| | 二分網路的邊 | projection 後的邊 |
| --- | --- | --- |
| 客戶–商品 | 客戶買過商品 | 兩位客戶買過至少一個相同商品 |
| 基因–疾病 | 基因與疾病有關 | 兩個基因共享至少一個疾病 |

```python
G_genes = bipartite.projected_graph(B, genes)                 # 無權重
G_w = bipartite.weighted_projected_graph(B, genes)            # weight = 共享鄰居數
G_j = bipartite.overlap_weighted_projected_graph(B, genes)    # Jaccard 權重
```

| 風險 | 做法 |
| --- | --- |
| 「共同購買」被誤解為「彼此直接有關係」 | 在報告中明確寫出 projected edge 的意義 |
| 熱門的另一側節點（暢銷商品、被研究最多的疾病）讓大量節點彼此相連，形成假 hub | 用共享數或 Jaccard 加權，再過濾；或改用統計顯著性（超幾何檢定）定義邊 |
| projection 丟失資訊（共享 1 個 vs 共享 50 個） | 用加權 projection |

## 過濾 (Filtering)

真實互動網路常非常稠密。過濾不是資料作弊，而是把焦點放回真正強的關係：

| 過濾 | 例子 |
| --- | --- |
| 依 edge 權重 / 互動次數門檻 | `sale_count >= 5`、STRING `combined_score >= 700` |
| 依時間範圍 | 只看某季 |
| 依節點屬性或子集 | 某個分組、某個 pathway |

```python
strong = nx.Graph((u, v, d) for u, v, d in G_w.edges(data=True) if d["weight"] >= 3)
```

門檻是分析決策，要報告；換幾個門檻看結論是否穩定。

## 存成檔案

網路資料在實務上多以 node list + edge list（各含 metadata）存成 CSV，容易交換、與 pandas 串接。要明確定義 source / target 欄、edge 與 node 屬性、是否有向、分組標記，否則 `read_edgelist()` 讀得進去不代表語意也保留了。需要保留屬性與型別時用 GraphML（`nx.write_graphml`）。

視覺化二分網路時，用一般 layout 常很難讀；保留分組的版面（`nx.bipartite_layout`、Circos plot、兩欄排列）較能看出共享模式。

## 時間演變 (Evolving Graphs)

溝通、論壇、合作、交易網路都會隨時間改變。常見做法是時間切片：

```
依時間窗切資料 → 每個窗建一張圖 → 對每張圖算同一組指標 → 把指標當時間序列看
```

```python
import pandas as pd

rows = []
for period, chunk in events.groupby(pd.Grouper(key="timestamp", freq="MS")):   # 每月
    Gt = nx.from_pandas_edgelist(chunk, "student", "forum")
    rows.append({"period": period, "n_nodes": Gt.number_of_nodes(), "n_edges": Gt.number_of_edges(),
                 "density": nx.density(Gt), "n_components": nx.number_connected_components(Gt)})
stats = pd.DataFrame(rows).set_index("period")
stats.plot(subplots=True)
```

| 指標 | 回答 |
| --- | --- |
| 節點數、邊數 | 網路在擴張還是縮小？ |
| density | 連結是否變密？ |
| 連通分量數、最大分量比例 | 是否整合成一體？ |
| 特定節點的 centrality 隨時間 | 誰逐漸變得核心？ |

| 選擇 | 取捨 |
| --- | --- |
| 窗口大小 | 太小：每張圖太稀疏、雜訊大；太大：看不到變化 |
| 不重疊 vs 滑動窗口 | 滑動窗口較平滑，但相鄰點不獨立 |
| 累積圖 vs 窗內圖 | 累積圖的指標只會單調變化，不適合看活躍度 |

不要只看「圖看起來變密了」，要把固定的一組指標畫成時間序列。

## 案例：學生–論壇發文網路

1. 從 DataFrame 建二分圖（學生、論壇；邊 = 發文）
2. projection 成學生–學生或論壇–論壇圖
3. 依發文次數過濾邊
4. 視覺化局部或整體結構
5. 按月比較各時間切片的指標

| 常見錯誤 | |
| --- | --- |
| 忘記標記分組 | 後面無法正確 projection 或算二分指標 |
| projection 後沿用原始邊的意義 | 「共享」被當成「直接關係」 |
| 強弱連結混在一起、不過濾 | 結構被雜訊淹沒 |
| 只用整段期間的單一圖 | 忽略結構隨時間改變 |
| 用一般 centrality 比較二分節點 | 分母錯誤 |
