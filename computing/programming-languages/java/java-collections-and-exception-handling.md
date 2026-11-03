[程式語言](../README.md) › [Java](README.md) › 集合與例外處理

# Java 集合與例外處理 (Collections and Exception Handling)

一般 Java 程式很快就會遇到兩個問題：怎麼管理一群物件（集合框架），以及出錯時怎麼不失去控制（例外處理）。資料結構的原理與複雜度見 [線性資料結構](../../computer-science-foundations/linear-data-structures.md)、[非線性資料結構](../../computer-science-foundations/non-linear-data-structures.md)。

## 集合框架 (Collections Framework)

`java.util` 內建的資料結構，分兩大家族：`Collection`（一群物件：`List`、`Set`、`Queue`）與 `Map`（key → value）。

| 介面 | 特性 | 常用實作 | 對應 Python |
| --- | --- | --- | --- |
| `List` | 有序、可重複、依索引存取 | `ArrayList`（預設）、`LinkedList` | `list` |
| `Set` | 不重複 | `HashSet`（無序）、`LinkedHashSet`（保留插入順序）、`TreeSet`（排序） | `set` |
| `Queue` / `Deque` | FIFO / 雙端 | `ArrayDeque`（預設）、`PriorityQueue`（堆積） | `collections.deque`、`heapq` |
| `Map` | key → value | `HashMap`、`LinkedHashMap`、`TreeMap`（依 key 排序） | `dict` |

| 陣列 | 集合 |
| --- | --- |
| 長度固定 | 大小可變 |
| 可直接放基本型別 | 只放物件（`Integer` 而非 `int`，自動裝箱） |
| 幾乎沒有內建操作 | 豐富的方法 |

### 泛型 (Generics)

```java
List<String> animals = new ArrayList<>();       // <String>：只能放 String；右邊 <> 自動推斷
animals.add("horse");
animals.add(42);                                // 編譯錯誤：型別安全
```

沒有泛型的「原始型別」(`List animals`) 什麼都能放，取出時要強制轉型，錯誤延到執行時才發現。

### 常用操作

```java
import java.util.*;

// List
List<String> animals = new ArrayList<>(List.of("horse", "cow"));
animals.add("chicken");
animals.get(0);                  // "horse"
animals.set(1, "goat");
animals.remove("horse");
animals.contains("goat");        // true（O(n)）
animals.size();

List<String> fixed = List.of("a", "b");          // Java 9+：不可變；add 會丟 UnsupportedOperationException
List<String> view = Arrays.asList(arr);          // 固定長度，與原陣列共用資料

// Set
Set<String> words = new HashSet<>();
words.add("java"); words.add("java");            // 重複的被忽略
words.contains("jvm");                           // O(1) 平均

// Map
Map<String, Integer> counts = new HashMap<>();
counts.put("A", 1);
counts.get("A");                                 // 1；不存在回傳 null
counts.getOrDefault("C", 0);                     // 0
counts.merge("A", 1, Integer::sum);              // 計數：A → 2
for (Map.Entry<String, Integer> e : counts.entrySet()) {
    System.out.println(e.getKey() + "=" + e.getValue());
}

// Queue / Deque
Deque<String> q = new ArrayDeque<>();
q.offer("A"); q.offer("B");                      // 尾端加入
q.poll();                                        // "A"：前端取出；空時回傳 null
Deque<String> stack = new ArrayDeque<>();
stack.push("x"); stack.pop();                    // 當堆疊用

// 工具類別
Collections.sort(animals);
Collections.reverse(animals);
animals.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));
```

| 方法成對 | 失敗時丟例外 | 失敗時回傳特殊值 |
| --- | --- | --- |
| 加入 | `add()` | `offer()` → `false` |
| 取出 | `remove()` | `poll()` → `null` |
| 查看 | `element()` | `peek()` → `null` |

| 選擇 | 理由 |
| --- | --- |
| `ArrayList` 而非 `LinkedList` | 隨機存取 `O(1)`、快取友善；`LinkedList` 只有在頻繁於已知位置插入刪除時才有優勢 |
| `ArrayDeque` 而非 `Stack` / `LinkedList` 當佇列 | 較快；`Stack` 是舊類別 |
| `HashSet` / `HashMap` 做成員檢查與查找 | `O(1)` 平均；`List.contains` 是 `O(n)` |
| 多執行緒共用 | `ConcurrentHashMap`、`ArrayBlockingQueue`（見 [效能與並行](java-performance-and-concurrency.md)） |

## 例外處理 (Exception Handling)

例外 (exception) 表示正常流程無法照寫的方式繼續：輸入錯誤、程式錯誤、外部資源出問題。

```java
try {
    int n = Integer.parseInt(text);
    String x = list.get(n);
} catch (NumberFormatException e) {             // 依序比對，第一個符合的 catch 執行
    System.out.println("Bad number: " + e.getMessage());
} catch (IndexOutOfBoundsException | NullPointerException e) {   // 多個型別共用處理
    System.out.println("Bad index");
} finally {
    System.out.println("Always runs");          // 不論是否發生例外都執行：清理
}
```

### 例外的種類

```
Throwable
├── Error                    嚴重問題，通常不處理：OutOfMemoryError、StackOverflowError
└── Exception
    ├── RuntimeException     unchecked：通常是程式錯誤
    │   NullPointerException、IndexOutOfBoundsException、IllegalArgumentException、
    │   NumberFormatException、ArithmeticException（除以 0）
    └── 其他                 checked：外部因素，必須處理或宣告
        IOException、FileNotFoundException、SQLException
```

| | Checked | Unchecked |
| --- | --- | --- |
| 父類別 | `Exception`（非 `RuntimeException`） | `RuntimeException` |
| 編譯器要求 | 必須 `catch` 或在方法簽章用 `throws` 宣告 | 可不處理 |
| 代表 | 不在程式控制內的狀況（檔案不存在、網路斷） | 錯誤的假設或 bug |

```java
// throws：交給呼叫者處理
public static List<String> readIds(Path p) throws IOException {
    return Files.readAllLines(p);
}

// 丟出例外：驗證輸入
if (reads < 0) throw new IllegalArgumentException("reads must be >= 0, got " + reads);

// 重新拋出並保留原因：加上脈絡，讓上層決定怎麼處理
try {
    loadConfig(path);
} catch (IOException e) {
    throw new IllegalStateException("cannot load config " + path, e);   // e 成為 cause
}
```

> 需要關閉的資源（檔案、連線）用 try-with-resources，見 [檔案 I/O](java-file-io-and-streams.md)；比 `finally` 手動關閉安全。

## Logging

`System.out.println` 適合練習；正式程式用 logging，可分級、可設定輸出位置與格式。

```java
import java.util.logging.Level;
import java.util.logging.Logger;

private static final Logger LOG = Logger.getLogger(MyClass.class.getName());
LOG.info("Loaded " + n + " samples");
LOG.log(Level.SEVERE, "Failed to parse " + file, e);    // 附上例外，會印出 stack trace
```

| 等級（`java.util.logging`） | 用途 |
| --- | --- |
| `SEVERE` / `WARNING` | 錯誤 / 可能有問題 |
| `INFO` | 重要的正常事件 |
| `CONFIG` / `FINE` | 設定 / 除錯細節 |

> 實務專案多用 SLF4J + Logback（等級 `ERROR`、`WARN`、`INFO`、`DEBUG`、`TRACE`）。

## 常見錯誤

| 錯誤 | 說明 |
| --- | --- |
| 使用原始型別集合 | 失去型別檢查 |
| 對 `List.of` / `Arrays.asList` 結果呼叫 `add` | `UnsupportedOperationException` |
| for-each 迴圈中刪除元素 | `ConcurrentModificationException`；用 `removeIf` 或 `Iterator.remove()` |
| `catch (Exception e) {}` 吞掉例外 | 錯誤消失無蹤；至少要記錄 |
| 太早 catch 太廣的 `Exception` | 隱藏了有用的細節 |
| 重新拋出時沒帶原例外 | 失去根本原因的 stack trace |
