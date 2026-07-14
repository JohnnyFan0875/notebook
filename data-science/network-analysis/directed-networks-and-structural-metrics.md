# Directed Networks and Structural Metrics

當 graph 有方向時，很多原本看起來熟悉的 network 指標都會換一個意思。這也是為什麼 network analysis 不能只停在「有沒有連到」，還要進一步問 edge 是否有方向、整體結構是否比隨機圖更聚集、以及 nodes 是否傾向和相似的對象互連。

Key point: directed network 讓 edge meaning 更精細，而 structural metrics 則讓你從整體層級判斷這張圖到底是鬆散、集中、互惠、同質，還是存在清楚社群。

## Adjacency Matrix And Edge List Are Different Working Views

同一張 graph，常見的兩種資料表示方式是:

- adjacency matrix
- edge list

adjacency matrix 適合強調:

- 哪些 node pairs 之間有沒有連結
- 關係是否對稱
- 以矩陣角度做運算

edge list 則更適合:

- 從 tabular data 建 graph
- 加入 edge-level metadata
- 和 pandas 或 tidy data workflow 串接

實務上 edge list 通常更方便，但 adjacency matrix 很適合幫助你看出 directedness 與 sparsity。

## Directedness Changes The Question

在 undirected graph 裡，`A -- B` 和 `B -- A` 沒有差別；但在 directed graph 裡，`A -> B` 和 `B -> A` 是不同事件。

這會立刻改變分析問題:

- 誰主動指向很多人？
- 誰被很多人指向？
- 哪些路徑可走，哪些其實走不通？

所以 directedness 不是技術細節，而是 network semantics 的一部分。

## In-Degree And Out-Degree Answer Different Things

一旦 graph 有方向，degree 最好拆開來看:

- in-degree: 有多少 edges 指向這個 node
- out-degree: 這個 node 指向多少其他 nodes

兩者通常代表不同角色。

例如在社交或引用 network 裡:

- 高 in-degree 可能代表受關注、被提及或被依賴
- 高 out-degree 可能代表活躍、擴散或主動接觸很多對象

如果只報一個總 degree，很容易把這兩種角色混在一起。

## Directed Queries Need Local Inspection Too

directed network 很常需要做局部檢查，例如:

- `A` 是否真的指向 `E`
- 哪些 edges 和某個 node incident
- 一條 edge 的起點與終點各是誰

這些問題看起來很基礎，但很重要，因為很多後續 centrality 或 path 結論都建立在 edge direction 沒有被建錯的前提上。

## Network-Level Metrics Describe The Whole Graph

除了 node-level centrality，也需要一些 graph-level summary 來描述整體結構。這份材料特別適合補上的，是下面幾個指標:

- density
- average path length
- transitivity

它們不是在問「誰重要」，而是在問「這張網路整體長什麼樣」。

## Density Tells You How Full The Network Is

density 可以先理解成:

- 實際存在的 edges
- 占理論上可能 edges 的比例

它很適合回答:

- 這張圖是稀疏還是稠密？
- 同樣規模的圖之間，哪一張更容易形成連結？

但 density 單獨看不夠，因為高 density 不代表一定有清楚群聚，也不代表資訊一定能快速傳播。

## Average Path Length Captures Reachability At Scale

average path length 關心的是:

- 任兩點之間平均要經過多少步才走得到

它幫你從全圖層級理解 reachability。

直覺上:

- 平均路徑短，代表網路比較容易穿越
- 平均路徑長，代表不同區塊之間可能更疏遠

這個指標特別適合和 density 一起看，因為兩張密度相近的網路，平均路徑長仍可能差很多。

## Transitivity Measures Local Closure

transitivity 可以先把它想成 triangle closure 的比例，也就是:

- 你的朋友的朋友，是否也常回頭連到你或彼此

這份課程同時區分了:

- global transitivity: 從全圖角度看 closed triplets 的比例
- local transitivity: 從單一 node 周邊看鄰居之間是否互相連接

這個指標很有用，因為它比單純 degree 更能反映「局部圈子有沒有真的形成團塊」。

## Compare To Random Graphs Before Telling A Story

這份課程最值得保留的一個觀念，是不要只看原始 network 的數值，而要和 random baseline 比較。

一個常見流程是:

1. 建立多張和原圖擁有相同節點數、近似 density 的 random graphs。
2. 對每張 random graph 計算某個指標，例如 average path length。
3. 把原始網路的數值放進這個隨機分佈中比較。

這樣你才知道:

- 原圖的結構只是隨機也會出現
- 還是真的比較短、比較聚集、比較特殊

Key point: 單一 graph metric 幾乎永遠不該脫離 baseline 單獨解讀。

## Assortativity Asks Whether Similar Nodes Prefer Each Other

assortativity 描述的是:

- nodes 是否傾向和「相似」的 nodes 相連

這個相似可以是:

- categorical attribute
- numerical attribute
- degree 本身

因此 assortativity 適合回答的不是「有沒有群體」，而是:

- 相同類型的人是否更常互連
- 高 degree nodes 是否傾向連到其他高 degree nodes

這能幫你分辨網路是偏同質連結，還是更混合、異質的結構。

## Reciprocity Matters Only When Direction Matters

reciprocity 是 directed graph 很重要的補充指標。它關心的是:

- 若 `A -> B` 存在，`B -> A` 是否也常存在

這個指標常見於:

- communication network
- social following network
- trade or exchange network

它能區分:

- 單向關注或單向依賴
- 雙向互動或互惠關係

如果你的 network 本質上有方向，卻不檢查 reciprocity，就很容易漏掉關係是否真正對等。

## Community Detection Turns Dense Structure Into Groups

當網路開始出現多個緊密區塊時，community detection 可以幫助你把整體結構切成較可解讀的 groups。

這份課程用 edge betweenness 的想法來做社群偵測，核心直覺是:

- 跨群的橋接 edges
- 通常更常出現在不同群之間的 shortest paths 上

所以如果逐步移除高 edge-betweenness 的 edges，原本的大圖就可能分裂成較自然的 communities。

這種方法的價值不只是輸出群組編號，而是讓你更清楚:

- 哪些 edges 在撐住不同社群之間的連接
- 社群邊界大致落在哪裡

## A Practical Reading Order For Structural Analysis

如果你已經會基本 centrality，接下來可以用這個順序判讀更完整的 network structure:

1. 先確認 graph 是 directed 還是 undirected。
2. 對 directed graph 分開看 in-degree 與 out-degree。
3. 用 density 與 average path length 看整體連通程度。
4. 用 global / local transitivity 看局部閉合與群聚。
5. 再和 random graph baseline 比較，避免過度解讀。
6. 若懷疑有同質連結，看 assortativity。
7. 若關係有互惠可能，看 reciprocity。
8. 若圖呈現多團塊，再做 community detection。

## Common Failure Modes

- 把 directed graph 當 undirected graph 解讀，忽略關係方向
- 只報 degree，卻不區分 in-degree 與 out-degree
- 看到高 transitivity 就直接說存在穩定社群，卻沒和其他指標一起看
- 用 density 或 average path length 單獨講故事，沒有 random baseline
- 在 directed network 裡忽略 reciprocity，誤把單向連結當雙向互動
- 把 community detection 輸出的群組當成絕對真實邊界，而不是方法依賴的結構切分

如果你想從「圖上有哪些 node」走到「這張網路整體怎麼運作」，directedness 與 structural metrics 幾乎就是中間最重要的一層。
