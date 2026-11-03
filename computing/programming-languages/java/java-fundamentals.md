[程式語言](../README.md) › [Java](README.md) › 基礎

# Java 基礎 (Java Fundamentals)

Java 是靜態型別、編譯成位元組碼在 JVM 上執行的通用語言。比 Python 冗長、規則嚴格，但明確的型別與結構讓大型程式容易維護；生資領域的 GATK、Picard、IGV、Nextflow（Groovy，跑在 JVM）都建立在 JVM 上。本篇涵蓋程式結構、型別、字串、陣列、運算子與 package。

> 三個觀念解釋大部分「為什麼這麼正式」：程式碼都放在 class 裡；變數都有宣告的型別；語法明確標出邊界（`{}`、`;`）。

## 程式結構與執行

```java
// Main.java：檔名必須和 public class 同名
public class Main {
    public static void main(String[] args) {   // 程式進入點
        System.out.println("Hello, Java!");
    }
}
```

```bash
javac Main.java          # 編譯成 Main.class（位元組碼）
java Main                # 在 JVM 上執行
java Main.java           # Java 11+：單一檔案可直接執行，不必先 javac
```

| 名詞 | 意義 |
| --- | --- |
| JDK | 開發工具：`javac`、`java`、`jshell`（互動式 REPL）等 |
| JVM | 執行位元組碼的虛擬機；同一個 `.class` / `.jar` 可在不同作業系統執行 |
| `.jar` | 打包好的 class 檔；`java -jar picard.jar ...` |
| LTS 版本 | 17、21、25；生產環境選 LTS |
| 建置工具 | Maven（`pom.xml`）、Gradle（`build.gradle`）：管理依賴、編譯、測試、打包 |

| 規則 | 說明 |
| --- | --- |
| 區分大小寫 | `Main` 與 `main` 不同 |
| 陳述句以 `;` 結尾 | 空白只影響可讀性，不能取代語法 |
| `=` vs `==` | 指派 vs 比較 |
| 命名慣例 | 類別 `PascalCase`、變數與方法 `camelCase`、常數 `UPPER_SNAKE_CASE` |

## 變數與型別

```java
String message = "Java is awesome!";   // 型別 變數名 = 值;
int age = 29;
boolean isActive = true;
var count = 10;                        // Java 10+：區域變數型別推斷（仍是靜態型別 int）
final double PI = 3.14159;             // final：不可重新指派
```

| 類別 | 型別 | 說明 |
| --- | --- | --- |
| 整數 | `int`（預設）、`long`（範圍更大，字面值加 `L`）、`short`、`byte` | `int` 上限約 21 億，超過會**溢位**而不報錯 |
| 小數 | `double`（預設）、`float`（精度較低，字面值加 `f`） | 浮點數是近似值，金額用 `BigDecimal` |
| 其他基本型別 | `boolean`（`true` / `false`）、`char`（單一字元，單引號） | — |
| 參考型別 (reference type) | 類別、介面、enum、陣列、`String` | 變數存的是物件的參考，可以是 `null` |

| | 基本型別 (primitive) | 參考型別 (reference) |
| --- | --- | --- |
| 存什麼 | 值本身 | 指向物件的參考 |
| 可以是 `null` | 否 | 是 |
| `==` 比較 | 值 | **是不是同一個物件**；比內容用 `.equals()` |
| 預設值（欄位） | `0`、`false` | `null` |

### 包裝類別 (Wrapper Classes)

每個基本型別都有對應的物件版本：`int` → `Integer`、`double` → `Double`、`boolean` → `Boolean`、`char` → `Character`（其餘 `Byte`、`Short`、`Long`、`Float`）。

| 用途 | 例子 |
| --- | --- |
| 集合只能放物件 | `List<Integer>`，不能寫 `List<int>` |
| 提供方法與常數 | `Integer.parseInt("8")`、`Integer.MAX_VALUE`、`Boolean.parseBoolean("true")` |
| 表示「沒有值」 | `Integer age = null;` |

基本型別與包裝類別之間會自動轉換：自動裝箱 (autoboxing) `list.add(5)`、自動拆箱 (unboxing) `int x = list.get(0)`。

> 拆箱 `null` 會丟 `NullPointerException`；包裝類別用 `==` 比較只在 -128 到 127 之間碰巧成立（快取），一律用 `.equals()`。

## 字串

```java
char initial = 'J';                      // char：單引號、一個字元
String name = "Jim";                     // String：雙引號；"J" 也是 String 不是 char

String user = "JSmith13";
user.length();                           // 8（方法，有括號）
user.toLowerCase();                      // "jsmith13"
user.substring(0, 6);                    // "JSmith"
user.contains("13");                     // true
"a,b,c".split(",");                      // ["a", "b", "c"]
String full = "Java is" + " " + "awesome";   // + 串接；一邊是 String 時另一邊自動轉字串
String msg = String.format("%s has %d reads", "S1", 1200);
String block = """
    多行文字區塊 (text block)，Java 15+
    """;

"abc".equals(other);                     // 比較內容；不要用 ==
```

字串不可變 (immutable)：每次修改都產生新物件。迴圈中大量串接用 `StringBuilder`，見 [效能與並行](java-performance-and-concurrency.md)。

## 陣列

```java
int[] prices = {10, 20, 30, 40};
int[] zeros = new int[5];               // 長度 5，元素預設 0
int first = prices[0];                  // 索引從 0 開始
prices[2] = 95;
int n = prices.length;                  // 屬性，沒有括號（String 是 .length() 方法）
System.out.println(java.util.Arrays.toString(prices));   // [10, 20, 95, 40]
```

陣列長度建立後固定；需要增減元素時用 `ArrayList`，見 [集合與例外處理](java-collections-and-exception-handling.md)。

## 運算子

| 類別 | 運算子 |
| --- | --- |
| 算術 | `+ - * / %`、`++`、`--`、`+=` |
| 比較（結果為 `boolean`） | `> < >= <= == !=` |
| 邏輯 | `&&`（且）、`\|\|`（或）、`!`（非）；短路求值 |
| 三元 | `cond ? a : b` |

```java
int numOrders = 100, days = 30;
int avg = numOrders / days;                  // 3：兩個整數相除是整數除法，小數被捨去
double avgD = (double) numOrders / days;     // 3.333...：至少一邊轉成 double
int r = 7 % 3;                               // 1：餘數
```

## Package 與 import

Package 是命名空間加目錄結構，用來組織類別，名稱全小寫、以點分隔，自訂 package 慣例用反轉網域：`com.example.app` 對應目錄 `com/example/app/`。

```java
package com.example.app;                // 檔案第一行：本檔所屬 package

import java.util.List;                  // 明確匯入單一類別（優先）
import java.util.*;                     // 萬用字元匯入整個 package
import java.math.BigDecimal;
```

| Package | 內容 |
| --- | --- |
| `java.lang` | `String`、`System`、`Math`、包裝類別、`Exception`；**自動匯入** |
| `java.util` | 集合、`Scanner`、`Optional` |
| `java.time` | 日期時間，見 [核心 API](java-core-apis.md) |
| `java.nio.file` | 檔案與路徑，見 [檔案 I/O 與 Stream](java-file-io-and-streams.md) |
| `java.math` | `BigInteger`（任意大整數）、`BigDecimal`（精確小數） |

```java
import java.math.BigDecimal;

BigDecimal exact = new BigDecimal("0.1").add(new BigDecimal("0.2"));   // 0.3（精確）
double approx = 0.1 + 0.2;                                            // 0.30000000000000004
```

> `BigDecimal` 要用字串建構：`new BigDecimal(0.1)` 會把 double 的誤差一起帶進來。

## 常見錯誤

| 錯誤 | 結果 |
| --- | --- |
| 預期整數除法得到小數 | `100 / 30` 是 `3` |
| 用 `==` 比較字串或包裝類別 | 比的是參考，結果看似隨機 |
| `char` 與 `String` 混用 | `'ab'` 編譯錯誤 |
| 陣列索引超出範圍 | `ArrayIndexOutOfBoundsException` |
| `System.out.println(array)` | 印出 `[I@1b6d3586` 這類位址，要用 `Arrays.toString` |
| 金額用 `double` | 累積誤差 |
