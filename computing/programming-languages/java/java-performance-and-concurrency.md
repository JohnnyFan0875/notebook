[程式語言](../README.md) › [Java](README.md) › 效能與並行

# Java 效能與並行 (Performance and Concurrency)

效能工作的第一原則：**最佳化真正的瓶頸，而不是看起來可疑的程式碼**。本篇是 Java 特有的部分：選對集合、JVM 記憶體與 GC、量測方法、執行緒與平行。複雜度 (Big-O) 的概念見 [演算法與複雜度](../../computer-science-foundations/algorithms-and-complexity.md)。

## 選對資料結構

| 操作 | 慢 | 快 |
| --- | --- | --- |
| 成員檢查 | `List.contains`，`O(n)` | `HashSet.contains`，`O(1)` 平均 |
| 依 key 查值 | 走訪 `List` 比對 | `HashMap.get`，`O(1)` 平均 |
| 依索引存取 | `LinkedList.get(i)`，`O(n)` | `ArrayList.get(i)`，`O(1)` |
| 兩端進出 | `ArrayList.remove(0)`，`O(n)` | `ArrayDeque` |
| 反覆取最小值 | 每次排序 | `PriorityQueue` |

雜湊結構的 `O(1)` 是**平均**情況，依賴良好的 `hashCode()` 分布；自訂類別當 key 時要正確實作 `equals` 與 `hashCode`。

## 瓶頸與量測

| 瓶頸類型 | 例子 | 方向 |
| --- | --- | --- |
| CPU-bound | 大量計算 | 更好的演算法、平行 |
| I/O-bound | 資料庫、網路、檔案 | 緩衝、批次、非同步、快取 |
| Memory-bound | 大量物件、GC 壓力 | 減少配置、基本型別陣列、串流處理 |

```
找出慢的路徑 → 量測 → 改設計 → 再量測
```

```java
long start = System.nanoTime();          // 量經過時間用 nanoTime，不用 currentTimeMillis（會受系統時鐘調整影響）
doWork();
long ms = (System.nanoTime() - start) / 1_000_000;
```

| 單次計時不可靠的原因 | 說明 |
| --- | --- |
| JVM 暖機 (warm-up) | JIT 要執行一陣子才會把熱點編譯成機器碼，前幾次特別慢 |
| GC 暫停 | 量測中途發生 GC |
| 死碼消除 | 結果沒被使用時 JIT 可能直接刪掉整段計算 |

> 嚴肅的微基準測試用 **JMH**（Java Microbenchmark Harness）。找熱點用 profiler：JDK Flight Recorder + JDK Mission Control、VisualVM、async-profiler。

## JVM 記憶體與 GC

| 區域 | 存放 |
| --- | --- |
| 堆疊 (stack) | 每個執行緒一個：呼叫框架、區域的基本型別值、參考 |
| 堆積 (heap) | 所有物件與陣列；由 GC 管理 |

```java
Runtime rt = Runtime.getRuntime();
rt.maxMemory();      // JVM 最多會用到的 heap（-Xmx）
rt.totalMemory();    // 目前已配置
rt.freeMemory();     // 已配置中尚未使用
```

```bash
java -Xms2g -Xmx8g -jar tool.jar          # 初始 / 最大 heap
java -XX:+UseG1GC -Xmx16g -jar tool.jar   # 指定 GC（G1 為 Java 9+ 預設）
```

> 跑 GATK、Picard 等 JVM 工具時最常調的就是 `-Xmx`：設太小丟 `OutOfMemoryError: Java heap space`；在 HPC 上要小於 [Slurm](../../workflow-engines/slurm.md) 申請的記憶體（留給 JVM 本身與原生記憶體的空間）。

GC 自動回收不再被參考的物件，但不代表記憶體不重要：不必要的物件配置會增加 GC 次數與暫停。

```java
StringBuilder sb = new StringBuilder();   // 迴圈中串接字串：避免每次產生新的 String
for (String part : parts) {
    sb.append(part).append('\t');
}
String row = sb.toString();
```

| 減少配置 | 說明 |
| --- | --- |
| `StringBuilder` 取代迴圈中的 `+` | 字串不可變，每次 `+` 都產生新物件 |
| 基本型別陣列 / `IntStream` | `List<Integer>` 每個元素都是物件，`int[]` 省很多記憶體 |
| 逐行串流處理 | 不要把整個大檔讀進記憶體 |

## 並行與平行 (Concurrency and Parallelism)

| 方式 | 用途 |
| --- | --- |
| `Thread` | 最底層；直接建立執行緒，實務少用 |
| `ExecutorService`（執行緒池） | 重用固定數量的 worker 執行緒，提交任務取得 `Future` |
| 虛擬執行緒 (virtual threads, Java 21+) | 極輕量，適合大量 I/O 等待的任務（每個請求一個執行緒） |
| 平行 stream | 資料平行：對大集合的獨立運算 |
| `CompletableFuture` | 非同步任務的組合 |

```java
import java.util.*;
import java.util.concurrent.*;

// 執行緒池：CPU-bound 任務通常設為核心數
ExecutorService pool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
List<Future<Integer>> results = new ArrayList<>();
for (Path f : files) {
    results.add(pool.submit(() -> countLines(f)));    // 提交任務，立即回傳 Future
}
int total = 0;
for (Future<Integer> r : results) total += r.get();   // 等待結果
pool.shutdown();

// Java 21+：虛擬執行緒，I/O-bound 任務
try (ExecutorService vt = Executors.newVirtualThreadPerTaskExecutor()) {
    for (String url : urls) vt.submit(() -> fetch(url));
}
```

### 平行 stream

```java
List<Integer> doubled = numbers.parallelStream().map(n -> n * 2).toList();
```

| 有幫助 | 沒幫助甚至更慢 |
| --- | --- |
| 每個元素的工作量大 | 每個元素工作量很小（切分與協調成本主導） |
| 資料量大 | 資料量小 |
| 運算彼此獨立、無共享狀態 | 有順序要求、會修改共享變數（還會產生錯誤結果） |

### 執行緒安全

多個執行緒同時修改同一個物件會產生競態條件 (race condition)：

| 問題 | 解法 |
| --- | --- |
| 共享的 `HashMap` / `ArrayList` | `ConcurrentHashMap`、`Collections.synchronizedList`，或讓每個執行緒各自累積再合併 |
| 共享計數器 `count++` | `AtomicInteger`、`LongAdder` |
| 多步驟操作需要原子性 | `synchronized` 區塊、`ReentrantLock` |

## 快取

用記憶體換速度：把昂貴的結果存起來重用。

```java
private final Map<String, Profile> cache = new ConcurrentHashMap<>();
Profile get(String id) {
    return cache.computeIfAbsent(id, this::loadFromDb);   // 不存在才計算並存入
}
```

需要考慮：多久過期、記憶體滿了淘汰誰（LRU）、能容忍多舊的資料。正式環境用 Caffeine 這類有淘汰與過期政策的快取函式庫，不要讓 `HashMap` 無限成長。

## 最佳化順序

| 優先 | 做法 |
| --- | --- |
| 1 | 修演算法與資料結構（`O(n²)` → `O(n)`） |
| 2 | 量測確認瓶頸 |
| 3 | 減少熱點迴圈中的物件配置與 I/O |
| 4 | 只在問題適合平行時才加並行 |
| 5 | 重算成本明顯高於記憶體成本時才加快取 |
