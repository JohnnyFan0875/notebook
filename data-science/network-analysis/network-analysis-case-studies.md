[Data Science](../README.md) › [Network Analysis](README.md) › 網路分析案例

# 網路分析案例 (Network Analysis Case Studies)

真正做網路分析時，資料很少一開始就是乾淨的 node–edge 表：拿到的是事件紀錄、文字、交易、移動軌跡或表現量矩陣，要自己決定怎麼轉成 graph。不同的建模選擇會產生不同的 edge 意義。指標的定義與解讀見 [入門](introduction-to-network-analysis.md) 與 [結構指標](directed-networks-and-structural-metrics.md)。

```
定義一列代表什麼事件 → 決定事件會不會產生 edge（方向、意義）→ 必要時從文字抽出關係
  → 重複互動聚合成權重 → 建圖後清理 → 大圖切子圖或時間切片 → 計算指標、比較方法
```

## 商品網路：一天一張快照

把商品推薦 / 共同購買資料過濾到單一日期，建成有向圖（node：商品；edge：某商品連向另一商品）。這就是時間切片：先看單一時間點的結構，再把多個日期串起來看變化。

「重要」可以是任務導向的組合條件，例如 out-degree 高且 in-degree 低（常推薦別人、少被推薦）。把這些節點放回其他日期的圖中檢查，會發現重要性可能只是暫時現象。

大圖的處理：取重要節點的 induced subgraph → 刪掉 degree 為 0 的節點 → 只看局部結構。

## Twitter：關係藏在文字裡

edge 常不在欄位中，而要從貼文文字抽出：轉推 (retweet)、提及 (mention)、回覆 (reply)、引用 (quote) 的對象。

| 互動 | 意義 | 方向 |
| --- | --- | --- |
| Retweet | 擴散、放大 | 轉推者 → 原作者 |
| Quote | 帶評論的引用 | 引用者 → 原作者 |
| Reply | 對話、互動回應 | 回覆者 → 被回覆者 |
| Mention | 呼叫、社交接觸 | 發文者 → 被提及者 |

它們都能表示成 `source → target`，但社會意義不同；研究問題和 edge 意義有關時，要分開建圖，不要合併。

```python
import networkx as nx
import pandas as pd

# 1. 從文字抽 mention（被提及的帳號不一定在作者清單中，建圖時自動補節點）
mentions = (tweets.assign(target=tweets["text"].str.findall(r"@(\w+)"))
                  .explode("target").dropna(subset=["target"]))

# 2. 不同互動各建一張有向圖；重複互動聚合成權重
def build(df, target_col):
    w = df.groupby(["user", target_col]).size().reset_index(name="weight")
    G = nx.from_pandas_edgelist(w, "user", target_col, edge_attr="weight", create_using=nx.DiGraph)
    G.remove_edges_from(nx.selfloop_edges(G))          # 清理：自我迴圈
    G.remove_nodes_from(list(nx.isolates(G)))          # 清理：孤立點
    return G

G_rt = build(tweets.dropna(subset=["retweeted_user"]), "retweeted_user")
G_mention = build(mentions, "target")

# 3. 比較同一批帳號在不同互動中的角色
deg = (pd.Series(dict(G_rt.in_degree()), name="rt")
         .to_frame().join(pd.Series(dict(G_mention.in_degree()), name="mention"), how="inner"))
deg["ratio"] = deg["mention"] / deg["rt"]              # 常被提及（對話型）vs 常被轉推（擴散型）
```

社群偵測不要只跑一種方法：比較 edge betweenness、Louvain / Leiden、label propagation 的結果，問哪些群在不同方法下都穩定、哪些邊界依賴演算法、結論對方法是否敏感，見 [社群偵測](directed-networks-and-structural-metrics.md#社群偵測-community-detection)。

## 單車共享：流動網路與權重

原始資料是一筆筆騎乘紀錄，不是現成的邊：

```python
flows = trips.groupby(["from_station_id", "to_station_id"]).size().reset_index(name="weight")
G = nx.from_pandas_edgelist(flows, "from_station_id", "to_station_id",
                            edge_attr="weight", create_using=nx.DiGraph)
```

| 概念 | 說明 |
| --- | --- |
| 權重來自聚合 | 同一對站點被騎過幾次；可控制線寬、區分強弱連結、做過濾 |
| 網路距離 ≠ 地理距離 | 網路距離是要經過幾站，衡量結構可達性；兩站可能地理遠但網路近，反之亦然 |
| 連通度 (connectivity) | `nx.node_connectivity`、`nx.edge_connectivity`：要移除多少節點或邊網路才會斷開，衡量韌性 (robustness) |

## 生資案例

### PPI 網路（STRING）

[STRING](https://string-db.org/) 整合實驗、共表現、文獻探勘、基因鄰近等證據，給每對蛋白質一個信心分數（下載檔案中 `combined_score` 為 0–1000）。

```python
import requests, io

genes = ["TP53", "MDM2", "CDKN1A", "ATM", "CHEK2", "BRCA1"]
r = requests.get("https://string-db.org/api/tsv/network",
                 params={"identifiers": "\r".join(genes), "species": 9606, "required_score": 700})
ppi = pd.read_csv(io.StringIO(r.text), sep="\t")
G = nx.from_pandas_edgelist(ppi, "preferredName_A", "preferredName_B", edge_attr="score")
```

| 注意 | 說明 |
| --- | --- |
| 分數門檻 | 400 中等、700 高、900 最高信心；結論要對門檻做敏感度分析 |
| 證據類型 | 只用實驗證據 vs 包含文獻探勘，網路差很多 |
| 研究偏差 | 熱門基因的已知交互作用多，hub 不一定是生物上最核心 |
| ID 對應 | 用 STRING ID 或 Ensembl protein ID，symbol 有歧義 |

常見分析：從差異表現基因建子網路、找模組（MCODE、Louvain）、看 hub 與橋樑節點、對模組做富集分析。

### 基因共表現網路（WGCNA）

node 是基因，edge 是表現量的相似度。WGCNA 把相關係數取冪次（soft thresholding）讓網路接近無尺度 (scale-free)，再用 topological overlap 分出模組，每個模組以第一主成分（eigengene）摘要，與臨床特徵相關。

```r
library(WGCNA)
# datExpr：樣本 × 基因（已過濾低表現、已做變異穩定轉換）
sft <- pickSoftThreshold(datExpr, powerVector = 1:20, networkType = "signed")
net <- blockwiseModules(datExpr, power = 12, networkType = "signed", TOMType = "signed",
                        minModuleSize = 30, mergeCutHeight = 0.25)
MEs <- net$MEs                                   # 每個模組的 eigengene
cor(MEs, traits, use = "p")                      # 模組 ↔ 表型
```

| 注意 | 說明 |
| --- | --- |
| 樣本數 | 一般建議至少約 15–20 個樣本，否則相關係數雜訊太大 |
| 批次效應 | 先校正，否則模組反映的是批次而非生物 |
| 相關 ≠ 調控 | 共表現網路無方向、不代表因果；推論調控關係需要其他證據 |

### 單細胞 kNN 圖 + Leiden

單細胞分群本身就是網路分析：node 是細胞，edge 連到表現量空間（PCA 後）中最近的 k 個鄰居，再用 Leiden 社群偵測切出細胞群。

```python
import scanpy as sc

sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)        # 建 kNN 圖：adata.obsp["connectivities"]
sc.tl.leiden(adata, resolution=1.0, flavor="igraph", n_iterations=2, key_added="leiden_r1")
sc.tl.umap(adata)                                       # UMAP 也建立在同一張 kNN 圖上
```

| 參數 | 影響 |
| --- | --- |
| `n_neighbors` | 小：保留細緻局部結構、易破碎；大：較平滑、小群可能被吞掉 |
| `n_pcs` | 太少丟失訊號，太多加入雜訊 |
| `resolution` | 社群偵測的 resolution 參數：越大群越多；沒有唯一正確值，要用 marker 基因與生物知識判斷 |

UMAP 上看起來分開不代表是不同細胞類型，看起來相連也不代表是連續的分化：判斷要回到 kNN 圖與 marker。批次整合（Harmony、scVI）要在建圖之前，見 [單細胞深度學習](../deep-learning/bio-applications/single-cell-deep-learning.md)。

## 常見錯誤

| 錯誤 | 後果 |
| --- | --- |
| 把原始事件列直接當 edge，沒確認每列的意義 | 圖建錯 |
| 把 retweet、mention、reply 混成同一種互動 | centrality 與社群的解讀變模糊 |
| 沒有聚合重複互動 | 權重資訊流失（或變成多重邊） |
| 只看地理距離，或把相似度當距離算最短路徑 | 回答錯的問題 |
| 只跑一種社群偵測、一個 resolution 就下結論 | 結果依賴方法與參數 |
| 共表現網路沒校正批次 | 模組反映技術變異 |
