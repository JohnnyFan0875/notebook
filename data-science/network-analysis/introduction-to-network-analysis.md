# Introduction to Network Analysis

network analysis 適合處理的，不是單點數值高低，而是關係結構本身。當你真正關心的是「誰和誰有連結」、「資訊或流量怎麼穿越網路」、「哪些節點在中間扮演橋樑」，graph 就會是比普通表格更好的語言。

Key point: 一張 network 的資訊量不只在 nodes 和 edges 的清單，而在它們組成的結構。分析的目標通常是把這個結構轉成可解讀的問題，例如重要性、路徑、群聚與推薦。

## Networks Start With A Modeling Choice

要做 network analysis，第一步不是算 centrality，而是先定義:

- node 代表什麼 entity
- edge 代表什麼 relation
- edge 是否有方向
- edge 是否有權重

例如:

- social network: nodes 是人，edges 是互動或關係
- transportation network: nodes 是站點，edges 是可通行路線
- collaboration network: nodes 是使用者，edges 是共同參與同一個專案或 repo

如果 node 和 edge 的語意沒有先釐清，後面的所有 graph metric 都可能失去意義。

## Why Use Graphs At All

network analysis 常處理幾類典型問題:

- important entities: 例如 social network 中的 influencers
- pathfinding: 例如交通或物流中的最有效路徑
- local structure: 例如朋友群、團隊或合作圈
- recommendation: 例如應該和誰連結、合作或互動

這些問題之所以適合 graph，不是因為 graph 比較炫，而是因為它把「關係」變成一級公民。

## Building Graphs In NetworkX

這份入門材料大量使用 `networkx`。在 Python 裡，最先要熟的通常是:

- 建立 graph 物件
- 加入 nodes 與 edges
- 為 nodes 或 edges 加上 attributes
- 讀取基本結構資訊，例如 `G.nodes()`、`G.edges()`

這些操作看起來簡單，但很重要，因為很多分析其實都建立在「圖是否被正確建起來」。

## Graph Type Changes The Question

不是所有 graph 都一樣。最基本的差異包括:

- undirected graph: 關係雙向，例如 Facebook friendship
- directed graph: 關係有方向，例如 Twitter follow
- multigraph / multidigraph: 同一對節點之間可以有多條邊
- weighted graph: 邊帶有強度、距離、成本或頻率

這個分類會直接改變你能問的問題。

例如:

- 在 directed network 裡，in-degree 和 out-degree 回答不同問題
- 在 weighted network 裡，最短路徑不一定是邊數最少，而可能是成本最低
- 在 multigraph 裡，多次互動不應該被壓成單一無差別連結

## Degree Is The Simplest Importance Signal

degree centrality 可以先當成最直觀的節點重要性。

- undirected graph: 看一個 node 接了多少邊
- directed graph: 可以再拆成 in-degree 與 out-degree

它適合回答:

- 誰和最多人有直接連結？
- 哪些節點最活躍或最受歡迎？

但 degree 只看直接鄰居，不看整體網路結構，所以它很容易高估「熱鬧但不關鍵」的節點。

## Betweenness Captures Bridge Value

betweenness centrality 的核心直覺是:

- 某個 node 會不會經常出現在別人的 shortest path 上

它適合找的是:

- 橋接不同社群的中介節點
- 少數連起兩大團塊的 bottleneck
- degree 不高、但一旦移除就會讓網路斷裂的重要節點

這也是為什麼一個 node 可能:

- degree centrality 不高
- betweenness centrality 卻很高

這種節點未必「朋友很多」，但可能「誰要跨群溝通都得經過它」。

## Paths Answer Reachability Questions

network analysis 很常在問 path 問題。

常見版本包括:

- shortest path between two nodes
- all shortest paths
- 哪些 nodes 最常出現在 shortest paths 上

在交通、供應鏈或資訊傳播語境中，pathfinding 幾乎就是最直接的業務問題翻譯。

提醒: shortest path 的定義一定要和 edge meaning 對齊。若 edge weight 代表距離、成本或阻力，最短路徑不應只看 hops 數量。

## Cliques Capture Tightly Connected Groups

clique 是一組彼此完全連通的 nodes。

最簡單的複雜 clique 可以先想成 triangle。它的重要性在於:

- 它比一般高 degree 更強，因為每個成員彼此都互連
- 它常代表緊密群體、強合作圈或高度重疊的社交結構

network analysis 裡常見的不是只找 clique，而是找 maximal clique，也就是:

- 再多加一個 node 就不再是 clique 的 clique

這種結構常被拿來做:

- community finding 的起點
- 緊密合作團體探索
- 局部高密度區域辨識

## Subgraphs Help You Zoom In

真實 network 很容易太大，直接看全圖通常只會變成一團毛球。

subgraph 的用途就是:

- 聚焦某個 node 周邊的鄰居
- 看某個局部社群的關係
- 從大圖中切出比較可讀的片段

一個很常見的分析節奏是:

1. 先在全圖上找重要 node。
2. 再取該 node 的 neighbors。
3. 建立對應 subgraph。
4. 用局部圖檢查社群、橋接或推薦機會。

這比一開始就試圖解讀整張大圖通常有效得多。

## Graph Visualization Is For Reasoning, Not Decoration

課程裡反覆示範 visualizing networks，原因不是因為圖漂亮，而是因為 visualization 可以幫你快速看出:

- 節點是否分成幾個團塊
- 某些 node 是否明顯扮演橋樑
- clique 或 dense area 是否存在
- local neighborhood 是否合理

但也要記住:

- 視覺 layout 不是數學事實
- layout 改了，圖看起來就可能很不一樣

所以圖像適合拿來探索與溝通，真正的判斷仍要回到 graph metrics。

## A Practical Workflow For Intro Network Analysis

入門 network analysis 可以先固定走這條路:

1. 定義 nodes、edges、direction 與 weights。
2. 建好 graph，先檢查 nodes / edges / attributes 是否合理。
3. 判斷這是 directed、undirected、weighted 還是 multigraph 問題。
4. 先算 degree、再看 betweenness 與 shortest paths。
5. 若圖太大，切 subgraphs 做局部檢查。
6. 若懷疑有緊密群體，再看 cliques 或 clique-like structure。
7. 最後回到真實任務，例如 influence、routing、community 或 recommendation。

這個順序很重要，因為很多人會太早跳去複雜 metric，卻還沒確認 graph 是否被正確表示。

## Example Use Case: Collaboration Network

這份課程最後用 GitHub collaboration network 當案例，很適合入門。

設定方式很直覺:

- nodes: users
- edges: 共同參與同一個 repository 的合作關係

這樣的 network 可以回答:

- 哪些使用者在 collaboration graph 中最核心？
- 哪些人橫跨多個合作圈？
- 哪些使用者之間可能值得推薦建立合作？

這也提醒我們: recommendation system 不一定只能從 user-item matrix 出發，也可以從 graph structure 出發。

## Common Failure Modes

- 把任何關聯資料都硬畫成 graph，卻沒有清楚 edge meaning
- 忽略 directed vs undirected 的差異
- 把高 degree 誤解成所有形式的重要性
- 只看 visualization，不看 metric
- 把全圖擠在一起，卻不切 subgraph 做局部理解
- 把 clique 或 community 當成絕對真實群體，而不是依賴建模定義的結構

如果 graph representation 錯了，後面的 centrality、path 與 recommendation 幾乎都會一起失真。
