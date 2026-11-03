[程式語言](../README.md) › [Java](README.md) › 檔案 I/O 與 Stream

# Java 檔案 I/O 與 Stream API (File I/O and Streams)

兩個名稱相近但不同的主題：**檔案 I/O** 處理檔案系統與持久化（`java.nio.file`、`java.io`）；**Stream API** 是對記憶體中集合做篩選、轉換、彙總的管線，和 I/O 的「串流」無關。

## 檔案 I/O

新程式用 `java.nio.file`（`Path` + `Files`）；舊的 `java.io.File` 仍常見於舊程式碼。

| 任務 | `java.nio.file`（建議） | `java.io`（舊） |
| --- | --- | --- |
| 表示路徑 | `Path p = Path.of("data", "a.txt")` | `new File("data/a.txt")` |
| 是否存在 | `Files.exists(p)` | `file.exists()` |
| 建立檔案 / 目錄 | `Files.createFile(p)`、`Files.createDirectories(dir)` | `createNewFile()`、`mkdir()` / `mkdirs()` |
| 刪除 | `Files.delete(p)`（失敗丟例外）、`Files.deleteIfExists(p)` | `delete()`（只回傳 `false`，不說原因） |
| 讀整個小檔 | `Files.readString(p)`、`Files.readAllLines(p)` | — |
| 寫整個小檔 | `Files.writeString(p, text)` | `FileWriter` |
| 列出目錄 | `Files.list(dir)`、遞迴 `Files.walk(dir)` | `listFiles()`（目錄不存在回傳 `null`） |
| 複製 / 移動 | `Files.copy`、`Files.move` | — |
| 絕對路徑 | `p.toAbsolutePath()` | `getAbsolutePath()` |

> `new File(...)` / `Path.of(...)` 只是指向一個位置，不會建立檔案。相對路徑以**目前工作目錄**為基準，從 IDE 與命令列執行時可能不同。

### 讀寫文字檔

```java
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.stream.Stream;
import java.util.zip.GZIPInputStream;

Path in = Path.of("samples.tsv");

// 1. 逐行讀大檔：try-with-resources 自動關閉，即使發生例外
try (BufferedReader br = Files.newBufferedReader(in, StandardCharsets.UTF_8)) {
    String line;
    while ((line = br.readLine()) != null) {      // null = 檔案結尾
        String[] cols = line.split("\t");
    }
} catch (IOException e) {
    System.err.println("Cannot read " + in + ": " + e.getMessage());
}

// 2. 以 Stream 逐行處理（惰性讀取，也要關閉）
try (Stream<String> lines = Files.lines(in)) {
    long n = lines.filter(l -> !l.startsWith("#")).count();
}

// 3. 寫檔：預設覆寫；附加用 StandardOpenOption.APPEND
Path out = Path.of("out.txt");
try (BufferedWriter bw = Files.newBufferedWriter(out)) {
    bw.write("Hello");
    bw.newLine();
}
Files.writeString(out, "More\n", StandardOpenOption.APPEND);

// 4. 讀 .gz（如 FASTQ.gz、VCF.gz）
try (BufferedReader br = new BufferedReader(new InputStreamReader(
        new GZIPInputStream(Files.newInputStream(Path.of("reads.fastq.gz"))), StandardCharsets.UTF_8))) {
    String header = br.readLine();
}
```

| 舊寫法 | 問題 |
| --- | --- |
| `FileReader.read()` 一次一個字元 | 慢；回傳 `int`，`-1` 表示結尾，要轉型成 `char` |
| 手動 `close()` | 中途丟例外就不會關閉，造成檔案控制代碼洩漏 |
| `new FileWriter("a.txt")` | 預設覆寫；附加要 `new FileWriter("a.txt", true)` |
| 未指定編碼 | Java 18 起預設 UTF-8，之前依作業系統（Windows 常是 Big5 / CP950） |

## 走訪集合：for-each 與 `Iterator`

```java
for (String fruit : fruits) { ... }             // 只讀取時最簡單

Iterator<String> it = fruits.iterator();         // 走訪中要刪除元素
while (it.hasNext()) {
    if (it.next().startsWith("A")) it.remove();  // 安全；for-each 中呼叫 fruits.remove 會丟 ConcurrentModificationException
}
fruits.removeIf(f -> f.startsWith("A"));         // Java 8+ 更簡潔的寫法

ListIterator<String> li = names.listIterator();  // List 專用：可往回走、修改、插入
while (li.hasNext()) {
    if ("Bob".equals(li.next())) li.set("Bobby");
}
```

## Stream API

Java 8+ 以函數式風格處理集合：`來源 → 中間操作（惰性）→ 終端操作（觸發計算）`。

```java
import java.util.*;
import java.util.stream.*;

List<String> names = List.of("Ana", "Bob", "Alice", "Ben");

names.stream().filter(n -> n.startsWith("A")).forEach(System.out::println);   // Ana, Alice
long b = names.stream().filter(n -> n.startsWith("B")).count();              // 2（long）
List<String> upper = names.stream().map(String::toUpperCase).toList();       // Java 16+
int total = names.stream().mapToInt(String::length).sum();                   // 15
int total2 = names.stream().map(String::length).reduce(0, Integer::sum);     // 同上，用 reduce

Map<Character, List<String>> byInitial = names.stream()
    .collect(Collectors.groupingBy(n -> n.charAt(0)));                       // {A=[Ana, Alice], B=[Bob, Ben]}
Map<Character, Long> counts = names.stream()
    .collect(Collectors.groupingBy(n -> n.charAt(0), Collectors.counting()));
String joined = names.stream().sorted().collect(Collectors.joining(", "));   // "Alice, Ana, Ben, Bob"
```

| 操作 | 類型 | 作用 | 對應 pandas / SQL |
| --- | --- | --- | --- |
| `filter` | 中間 | 保留符合條件的元素 | `df[cond]` / `WHERE` |
| `map` | 中間 | 轉換每個元素 | `apply` / `SELECT expr` |
| `sorted`、`distinct`、`limit` | 中間 | 排序、去重、取前 n | `sort_values`、`drop_duplicates`、`head` |
| `collect(groupingBy(...))` | 終端 | 分組 | `groupby` / `GROUP BY` |
| `count`、`sum`、`reduce` | 終端 | 彙總成單一值 | `agg` |
| `toList`、`collect(toSet())` | 終端 | 收集成集合 | — |

| 適合 Stream | 用迴圈比較清楚 |
| --- | --- |
| 篩選 → 轉換 → 彙總的管線 | 需要修改原集合、提早跳出 |
| 產生新的結果集合 | 迴圈很短、邏輯直接 |
| 分組統計 | 需要多個累加狀態 |

> Stream 只能用一次；終端操作後再用會丟 `IllegalStateException`。平行 stream 見 [效能與並行](java-performance-and-concurrency.md#平行-stream)。
