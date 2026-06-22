# Bipartite and Evolving Networks

很多真實 network 不是一開始就以「人和人相連」的形式存在，而是以 two-mode data 出現，例如 customer-product、student-forum、author-paper。這時直接把資料當一般 graph 來看，常會漏掉 partition 結構本身的意義。

Key point: bipartite network 的重點不是多一種 graph 類型而已，而是它強迫你區分兩類不同角色的 nodes。projection、centrality 與 filtering 都必須尊重這個分工。

## Bipartite Graphs Start From Two Partitions

bipartite graph 由兩組不同型態的 nodes 組成，edges 只跨 partition，不在同一組內直接相連。

常見例子:

- customers <-> products
- students <-> forums
- users <-> repositories
- authors <-> papers

這個結構很重要，因為它代表關係不是「同類之間直接相連」，而是透過另一組實體間接產生。

## Projection Is A Modeling Step, Not Just A Function Call

projection 的核心想法是:

- 保留某一側的 nodes
- 根據它們是否共同連到另一側的 nodes，建立 unipartite graph

也就是說，projection 是把 bipartite connectivity 轉成單一 partition 上的關係圖。

例如:

- customer projection: 兩位 customers 因為買過同一產品而相連
- product projection: 兩個 products 因為被同一批 customers 買過而相連

這個步驟非常有用，但也很危險，因為每一次 projection 都在重新定義 edge meaning。

## Always Ask What An Edge Means After Projection

在 projection 前後，edge 的語意不一樣。

- bipartite edge: customer interacted with product
- projected edge: two customers share at least one product interaction

如果沒有把這個 distinction 說清楚，很容易把「共同購買」誤解成「彼此直接有關係」。

所以做 projection 時，最好先問:

- 我想保留哪一側？
- 共同連到另一側代表什麼樣的關係？
- 這個 projected relation 對我的分析任務真的有意義嗎？

## Build Graphs From DataFrames Deliberately

這份課程很實用的一點，是它直接示範從 pandas DataFrame 建 graph。

一個典型流程通常是:

1. 從欄位中加入兩側 nodes。
2. 用 node attributes 標記 partition，例如 `bipartite='customers'`。
3. 再從每一列觀察建立 edges。

這個流程的關鍵不在語法，而在 schema discipline:

- 哪些欄位代表 node identities？
- 哪些欄位是 metadata？
- 每一列到底代表一筆 interaction、一次 posting，還是一次 co-occurrence？

如果 row meaning 不清楚，graph 很容易從第一步就建錯。

## Flat Edge Lists Are Often The Most Portable Network Format

network data 在實務上常不是存在 graph database，而是存在:

- nodelist + metadata
- edgelist + metadata

這種 flat file representation 很常見，因為它:

- 容易儲存成 CSV
- 容易和 pandas workflow 串接
- 容易跨工具交換

但也因此更需要你明確定義:

- source / target 欄位
- edge attributes
- node attributes
- directedness 與 partition labeling

否則 `read_edgelist()` 讀得進去，不代表語意就完整保留下來。

## Bipartite Centrality Needs The Right Denominator

在 bipartite graph 裡，degree centrality 不能總是照一般 graph 的方式直覺解讀。

原因是:

- 一側 node 的最大可能連結數
- 其實來自另一側 partition 的大小

這也是為什麼 bipartite centrality 最好用對應的 bipartite-aware 方法來算，而不是直接套一般 `degree_centrality()` 後就開始比較。

提醒: 如果直接把 bipartite graph 當普通 graph 算 centrality，結果未必錯到不能看，但詮釋通常會偏掉。

## Filtering Is Often The Real Analysis Step

真實 interaction network 常常非常密。這時真正有價值的不是把所有 edges 都畫出來，而是先做 filtering。

常見過濾方式包括:

- 只保留 edge weight 或 interaction count 高於某個門檻
- 只保留特定時間範圍
- 只保留某群 nodes 或某個 partition 的局部圖

例如如果 edge attribute 是 `sale_count` 或 `post_count`，只保留高頻 edges 往往能把雜訊網路變成更可解讀的結構圖。

Key point: filtering 不是資料作弊，而是把分析焦點放回真正強的關係。

## Visualization Should Respect Partition Structure

bipartite graph 的視覺化如果直接用一般 layout，常常很難讀。

這也是為什麼這份課程提到像 `CircosPlot` 這類視覺化工具，它們的價值在於:

- 保留 partition grouping
- 讓 node 類型可以用 grouping 或 color 看出來
- 幫助辨識高度共享的 nodes 或 dense interaction pattern

但和一般 graph 一樣，圖只是 reasoning aid，不是 metric 本身。

## Evolving Graphs Add Time Back Into The Network

intermediate 課程另一個重要主題，是 evolving graphs。

很多 network 不是靜態的，例如:

- communication networks
- forum posting networks
- collaboration networks

這時你關心的不只是某個時間點的結構，而是:

- graph statistics 如何隨時間改變
- edges 是否持續增加或減少
- 某些 periods 是否出現結構斷裂或快速擴張

這就把 network analysis 拉向 time-series thinking。

## Time Slicing Creates Comparable Snapshots

當 graph 會隨時間變化時，一個很常見的方法是:

- 先依時間切片
- 對每個 time window 建一張 graph
- 再比較每張 graph 的 summary statistics

這樣可以回答:

- network density 是否上升？
- connectedness 是否變強？
- 某些 nodes 是否逐漸變得更 central？

這種做法的好處是保留 network structure，同時又能回到可比較的時間序列。

## Analyze Statistics, Not Just Visual Drift

evolving graph analysis 很容易停在「圖看起來變密了」。更成熟的做法是對每個 snapshot 算固定的一組指標，例如:

- number of nodes
- number of edges
- density
- connected components
- partition-specific centrality

然後再把這些指標放回時間軸上看趨勢。

換句話說，evolving graph 不只是畫很多張圖，而是把 graph statistic 變成 time series。

## A Practical Case: Student-Forum Posting Network

課程案例用的是 college forum posting dataset，這很適合展示完整 workflow。

設定方式通常是:

- nodes: students, forums
- edges: 某位 student 在某個 forum 發文或互動

接著可以做:

1. 從 DataFrame 建 bipartite graph。
2. 投影成 student-student 或 forum-forum graph。
3. 依互動次數過濾 edges。
4. 視覺化局部或整體結構。
5. 按月份或其他 window 比較 evolving graph statistics。

這個流程很像真實分析工作，因為它把資料整理、建模、投影、過濾與時間分析放在同一條線上。

## Common Failure Modes

- 忘記標記 partition，後面無法正確投影或算 bipartite metrics
- projection 後直接沿用原始 edge 的語意
- 把弱連結與強連結混在一起，不做 edge filtering
- 只用單一全期間 graph，忽略網路結構會隨時間改變
- 對 evolving graph 只看圖，不看可比較的 summary statistics
- 用一般 centrality 直接比較 bipartite nodes，卻沒注意 normalization 邏輯

如果你不先搞清楚 graph 是 two-mode 還是 one-mode，後面很多「看起來合理」的結論都可能只是 representation artifact。
