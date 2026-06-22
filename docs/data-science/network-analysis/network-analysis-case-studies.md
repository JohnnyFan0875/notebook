# Network Analysis Case Studies

真正做 network analysis 時，資料通常不是一開始就長成乾淨的 node-edge 表。你更常拿到的是事件紀錄、文字欄位、交易資料或移動軌跡，然後必須自己決定怎麼把它轉成 graph。

Key point: case study 的價值不只是多看幾張圖，而是學會把 messy event data 轉成可分析的 network，並知道不同建模選擇會產生不同 edge meaning。

## Start From Events, Not From A Finished Graph

這組案例最有價值的地方，是它們都從原始資料表出發，而不是從已經整理好的 adjacency matrix 開始。

常見原始來源包括:

- 商品之間的共同購買或推薦紀錄
- 推文文本與使用者互動
- 單車站點之間的騎乘紀錄

這提醒我們，network workflow 的前半段通常是:

1. 先定義一筆 row 代表什麼事件。
2. 再決定 event 會不會生成 edge。
3. 最後才建立 graph 並計算指標。

## Amazon Product Network: One Date Can Be One Snapshot

Amazon 案例把商品互動資料過濾到單一日期，再建立 directed graph。這種做法很值得保留，因為它其實就是 time slicing。

建模方式可以理解成:

- nodes: products
- edges: 某產品連向另一產品的推薦或共同購買方向
- time unit: 某一天的 snapshot

這樣的好處是:

- 可以先看單一時間點的結構
- 也可以把多個日期串起來看變化

如果資料本身有時間欄位，先決定 graph 要不要是 snapshot，而不是急著把全部期間壓成同一張圖，通常會比較安全。

## Importance Can Change Over Time

這個案例裡一個很好的問題是: 某些看起來重要的 products，是否在其他日期也一樣重要？

這背後其實是兩個判斷:

- 重要性是怎麼定義的
- 重要性是否穩定

案例用的是簡單規則，例如:

- out-degree 高
- in-degree 低

這種定義未必普遍，但很值得學，因為它說明一件事: important node 不一定是抽象 centrality 排名，也可以是任務導向的結合條件。

更重要的是，當你把這些 nodes 放回多個日期的 graphs 觀察時，會發現重要性可能是暫時現象，而不是固定身分。

## Large Graphs Usually Need Local Views

Amazon graph 很大時，案例不是直接畫整張圖，而是:

- 先取 induced subgraph
- 再刪掉 degree 為 0 的 nodes
- 最後只看局部結構

這是很實用的工作習慣，因為真實網路常常太密。與其硬畫全圖，不如先:

- 抽某個時間點
- 抽某群重要節點
- 抽某個局部子圖

讓 visualization 回到可讀範圍。

## Twitter Interaction Graphs Need Text Parsing First

Twitter 案例很清楚地展示了一個重點: edge 常常不是直接存在欄位裡，而是藏在文字中。

例如你可能要先從 tweet text 抽出:

- retweet 對象
- mentions 對象
- reply 對象

這表示 network construction 的核心不只是 `graph_from_data_frame()`，而是先把文本事件轉成 sender-target pairs。

## Retweet And Mention Graphs Are Different Networks

同一份 tweet 資料，至少可以建兩種 graph:

- retweet graph
- mention graph

它們看起來都像使用者之間的 directed graph，但 edge meaning 其實不同。

- retweet edge 比較接近傳播、轉發、放大
- mention edge 比較接近對話、引用、呼叫、社交接觸

這很重要，因為如果把它們混成同一張圖，後面的 centrality、community 與 influence interpretation 就會變得模糊。

## Vertex Creation Sometimes Happens On The Fly

Twitter 案例還有一個很實用的工程細節: 被提及或被 retweet 的帳號，不一定先出現在作者清單裡。

所以建圖流程常會變成:

1. 先用已知作者建立部分 vertices。
2. 逐列掃描文本抽出互動對象。
3. 如果目標帳號不在現有 vertices 中，就補加進去。
4. 再把 edge 加上去。

這個模式在很多 event log 上都會出現，尤其是 target entity 來自半結構化文字時。

## Cleaning The Graph Is Part Of Construction

案例在建完 retweet / mention graph 後，會做幾個很實際的清理動作:

- `simplify()` 去掉重複或不必要的結構
- 刪除 degree 為 0 的 vertices

這提醒我們:

- graph 建出來不代表 graph 已經可分析
- construction 和 cleaning 通常是一個連續流程

如果你不先清掉孤立點、重複邊或明顯噪音，後面的社群與視覺化結果很容易被干擾。

## Community Detection Is Better As A Comparison Than A Single Answer

Twitter mentions 案例沒有只跑一種 community detection，而是比較了:

- edge betweenness
- leading eigenvector
- label propagation

這個做法很值得保留，因為不同方法切出來的群組數與群大小本來就可能不同。

所以比較成熟的態度不是問:

- 哪個方法給我唯一正確社群？

而是問:

- 哪些群組在不同方法下都穩定存在？
- 哪些邊界非常依賴演算法？
- 我的結論是否對分群方法敏感？

Key point: community detection 比較像是結構假說產生器，不是最後仲裁者。

## Bike Sharing Data Naturally Becomes A Weighted Mobility Graph

單車案例展示了另一種常見情境: 原始資料是一筆筆 trips，而不是已存在的 edges。

這時合理的做法通常是:

1. 用 `from_station_id` 和 `to_station_id` 分組。
2. 計算每組出現次數。
3. 把次數當成 edge weight。

於是 graph 變成:

- nodes: stations
- directed edges: 從起點站到終點站的流動
- weight: 該路徑出現頻率

這是一個非常典型的 mobility network 建模方式。

## Edge Weight Often Comes From Aggregation

這個案例最值得記住的是，weight 不一定是原始欄位直接給你的數字，它也可以是你彙總事件後得到的結果。

像這裡的 `weights = n()` 代表的是:

- 同一對站點之間被騎過多少次

這樣的 weight 很適合用來:

- 控制 edge thickness
- 定義強連結與弱連結
- 之後做過濾或 routing 分析

## Graph Distance And Geographic Distance Are Not The Same Thing

單車案例做了一個很好的對照:

- graph distance: 在 network 中要經過幾站才能到
- geographic distance: 現實世界中的地理距離

這兩者不一定一致。

一對站點可能:

- 地理上很遠，但 network 上連得不差
- 地理上很近，但因為路徑結構或流量模式，graph distance 反而不短

這個對照很重要，因為它提醒我們 network shortest path 測的是結構可達性，不是物理空間距離本身。

## Connectivity Describes Robustness, Not Just Reachability

案例後面還引入了 connectivity 的角度，例如:

- vertex connectivity
- edge connectivity

它們回答的不是「能不能到」，而是:

- 要移除多少 nodes 或 edges，網路才會斷開

這讓 network analysis 從 navigation 問題往 robustness 問題延伸。對交通、通訊、供應鏈類資料來說，這往往比單純 shortest path 更接近真實風險。

## Visualization Tools Depend On The Task

最後一部分案例展示了多種畫圖方式與套件。對 notebook 來說，真正要保留的不是某個特定 R 套件名稱，而是選圖工具的原則:

- 靜態探索圖: 適合快速檢查局部結構
- 屬性映射圖: 適合把中心性、社群或權重映射到顏色與大小
- 互動式圖: 適合展示較大的網路與滑動探索

換句話說，visualization tool 應該根據分析目的選，而不是因為某個套件比較炫就固定使用。

## A Practical Workflow For Messy Network Data

如果你面對的是事件流或半結構化資料，可以優先照這個順序走:

1. 先定義一筆資料會不會產生 edge。
2. 釐清 edge direction 與 edge meaning。
3. 必要時從文字中抽 sender-target 關係。
4. 若互動可重複發生，決定是否先聚合成 weighted edges。
5. 建圖後立刻清理孤立點與重複邊。
6. 大圖先切 subgraph 或抽 snapshot，不要直接解讀全圖。
7. 若資料有時間欄位，優先考慮 snapshot 或 evolving graph。
8. 若要做社群，至少比較兩種方法，避免把單一演算法輸出當定論。

## Common Failure Modes

- 把原始事件列直接當 edge，卻沒有先確認 row meaning
- 把 retweet、mention、reply 混成同一種互動
- 忘記為新增出現的目標帳號補 vertex
- 不聚合同一對 entities 的重複互動，導致 weight information 流失
- 只看地理距離，忽略 graph distance 回答的是另一個問題
- 只跑一種 community detection 就直接下定論

如果前面幾篇是 network analysis 的概念地圖，這篇 case study 更像是提醒你: 真正困難的地方，往往不是算指標，而是把資料正確地變成值得分析的 graph。
