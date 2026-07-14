# Scalable Processing and Out-of-Core Workflows

## Why This Topic Exists

很多資料流程的第一個瓶頸，不是演算法太複雜，而是資料根本放不進記憶體。

當資料大到超過單機 RAM 可舒服處理的範圍時，團隊就不能再假設：

- 全部資料一次讀進來
- 直接用 in-memory objects 做完所有運算
- 只靠更大的 swap 或虛擬記憶體就能撐過去

scalable processing 的核心目標，是在有限記憶體下，仍然能穩定載入、轉換、彙總與保留結果。

## RAM, Disk, and Why Swapping Hurts

像 R 這類以記憶體物件為中心的環境，會讓這個問題特別明顯：物件主要存在 RAM 中。

一旦超出 RAM，系統可能把資料移到 disk。問題在於：

- disk 比 RAM 慢得多
- execution time 會大幅上升
- 有時不只是變慢，還可能直接失敗或 crash

所以真正的 scalable strategy，通常不是硬撐到 swap，而是重新設計資料如何被讀與算。

## Two Common Strategies

面對大資料時，常見有兩條路：

1. 使用 disk-backed / out-of-core structure
2. 使用 chunk-wise processing

這兩條路都不是語言限定概念。R 的 `bigmemory` 和 `iotools` 只是具體例子，背後的想法可以轉移到 Python、Spark 或其他資料系統。

## Out-of-Core Data Structures

out-of-core 的核心概念是：

- 資料主要存在 disk
- 只在需要時把部分資料搬進 RAM
- 盡量保留 random access 或接近原生物件的操作體驗

這類方式特別適合：

- 資料形狀固定
- 需要反覆存取不同區塊
- 單機仍然可處理，只是記憶體不夠大

課程裡 `big.matrix` 的例子，正是這種 disk-backed random-access structure。

## What Disk-Backed Matrix Workflows Trade Off

這類資料結構通常有明顯優點：

- 能處理大於 RAM 的 dense matrix
- 仍可做 subset、summaries、部分更新
- 對使用者來說看起來接近一般 matrix

但限制也很重要：

- 常要求資料以 matrix 形式表示
- 不一定能動態增減 rows / columns
- 仍然需要足夠 disk space
- 如果資料型態不規則，matrix abstraction 可能不自然

所以它不是「任何大資料都適合」，而是適合特定資料形狀與 access pattern。

## Chunk-Wise Processing

另一條非常常見的路，是不要維持完整資料可隨機存取，而改成分批處理。

chunk-wise processing 的基本節奏通常是：

1. 載入一小塊資料
2. 轉成原生物件
3. 對這塊資料做運算
4. 保留必要結果
5. 丟掉這塊資料，讀下一塊

這個模式的價值在於：

- 透過 chunk size 控制記憶體壓力
- 讓資料量可以超過 RAM
- 可以把部分結果累積起來

## Loading and Parsing Are Different Steps

課程有一個很值得保留的觀點：匯入資料常包含兩個不同成本來源。

1. 從 disk 取資料
2. 把 raw bytes 解析成原生資料物件

這兩件事分開思考很重要，因為：

- I/O 常常比真正運算還慢
- parsing strategy 會直接影響記憶體與效能
- 如果先把 raw loading 和 object conversion 拆開，通常更有彈性

這也是為什麼很多高效資料系統都會把 scan、parse、decode、materialize 分成不同層。

## Split-Apply-Combine as a Scaling Pattern

當資料能被切成互相獨立的 partitions 時，常見做法是 split-apply-combine：

- `split`: 先把資料切成 partitions
- `apply`: 對每個 partition 做相同運算
- `combine`: 把各 partition 的結果彙總

這種模式特別適合：

- group-wise summary
- per-partition counting
- chunk-based partial aggregation
- 很多可分解的 regression / linear algebra 子問題

實務上，這個思維不只出現在 R 的 `split()`、`Map()`、`Reduce()`，也會出現在：

- map-reduce 類系統
- Spark transformations + actions
- chunked Pandas / SQL aggregation workflow

## Designing the Combine Step

split-apply-combine 真正的關鍵，不只是會切，而是 combine 能不能正確且有效率。

好的 partial result 通常要：

- 足以保留後續所需資訊
- 能被多個 chunk 結果安全合併
- 最好具備 associative / additive 性質

例如平均數常可以拆成：

- partial sum
- partial count

最後再把 sums 和 counts 合併，重新得到 global mean。

這種設計很常見，因為它比保留全部原始值更省資源。

## What Does Not Fit This Pattern

不是所有統計量都能自然地 split-apply-combine。

課程明確提醒的一類情況是：

- 需要同時看到全部資料的運算

典型例子像 exact median，就不像 sum 或 count 那麼容易靠簡單 partial aggregation 得到。

這提醒我們：在設計 scalable workflow 前，要先問演算法本身是否可分解，而不是先假設所有任務都能平行化。

## Sequential vs. Parallel Chunk Processing

chunk processing 可以 sequential，也可以 parallel。

### Sequential Chunking

適合：

- 資源有限
- combine state 需要逐步攜帶
- I/O 已經是主要瓶頸

### Parallel Chunking

適合：

- 各 chunk 彼此獨立
- apply 階段可以完全平行
- combine 成本相對可控

但更多 processors 不一定就一定更快，因為：

- 單機 I/O 可能先成為瓶頸
- worker coordination 有成本
- chunk 太小時，調度 overhead 可能超過收益

## Benchmarking and Performance Thinking

scalable code 不只是能跑大資料，也要知道慢在哪裡。

課程強調的幾個實務觀點包括：

- 計算複雜度會影響速度
- disk operations 需要被特別小心設計
- benchmarking 能幫你分辨 bottleneck 是 compute 還是 I/O

這個 mindset 很重要，因為很多「大資料問題」其實不是資料大，而是：

- 不必要地反覆讀寫 disk
- 過早 materialize 大物件
- combine 設計不佳

## When to Choose Which Approach

可以用這個粗略判斷：

- 如果資料形狀固定、需要 random access、且單機 disk 足夠，disk-backed structure 可能比較自然
- 如果資料比較像表格流、以掃描和彙總為主，chunk-wise processing 通常更直接
- 如果需要跨多機或天然平行，split-apply-combine 會比單機 matrix 更有延展性

## Practical Reminders

- 真正的 scalable workflow，不是讓全部資料勉強塞進 RAM，而是減少對完整 in-memory materialization 的依賴。
- loading、parsing、computing 最好分開思考，因為瓶頸不一定在同一層。
- chunk size 是重要調參點，太大會爆記憶體，太小會讓 overhead 變重。
- 想做平行化前，先確認你的運算能不能被安全拆解與合併。
- `bigmemory` 和 `iotools` 是具體工具，但更重要的是背後的 out-of-core 與 chunk-wise 心智模型。

[Back to Data Engineering](README.md)
