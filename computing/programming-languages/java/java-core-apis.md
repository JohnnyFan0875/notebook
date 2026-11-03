[程式語言](../README.md) › [Java](README.md) › 核心 API

# Java 核心 API (Core APIs)

標準函式庫中常用、但不屬於語法、OOP 或集合的幾個主題：日期時間 (`java.time`)、列舉 (enum)、`Optional`、遞迴。

## 日期與時間：`java.time`

Java 8+ 的 `java.time` 取代舊的 `Date` / `Calendar`：物件不可變、執行緒安全、日期與時間概念分開。

| 型別 | 表示 | 例子 |
| --- | --- | --- |
| `LocalDate` | 日期，沒有時間與時區 | 生日、採檢日期 |
| `LocalTime` | 時間，沒有日期 | 營業時間 |
| `LocalDateTime` | 日期 + 時間，沒有時區 | 本地時間戳記 |
| `ZonedDateTime` | 日期 + 時間 + 時區 | 跨時區的會議時間 |
| `Instant` | UTC 時間軸上的一點 | log、資料庫時間戳記 |
| `Duration` / `Period` | 時間長度（秒、奈秒）/ 日期長度（年月日） | 執行時間 / 年齡 |

```java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

LocalDate today = LocalDate.now();
LocalDate d = LocalDate.parse("2024-03-10");                      // ISO 格式直接 parse
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("MM/dd/yyyy");
LocalDate us = LocalDate.parse("03/10/2024", fmt);                 // 自訂格式要給 formatter
String s = d.format(fmt);                                          // "03/10/2024"

d.plusDays(7);  d.minusMonths(1);  d.withDayOfMonth(1);            // 回傳新物件（不可變）
ChronoUnit.DAYS.between(d, today);                                 // 相差天數
Period.between(LocalDate.of(1990, 5, 1), today).getYears();        // 年齡

Instant t0 = Instant.now();
Duration elapsed = Duration.between(t0, Instant.now());
```

| 陷阱 | 說明 |
| --- | --- |
| 格式不符 | `parse` 丟 `DateTimeParseException` |
| `yyyy` vs `YYYY`、`MM` vs `mm` | `YYYY` 是週年（跨年那週會錯）、`mm` 是分鐘 |
| 用字串存日期再比較 | 先 parse 成 `LocalDate`，才能安全比較與運算 |
| `LocalDateTime` 用在跨時區資料 | 存 `Instant`（UTC），顯示時再轉時區 |

Python / pandas 的對應操作見 [Datetime](../../../data-science/python-foundations/datetime.md)。

## 列舉 (Enum)

定義一組固定、封閉的合法值，取代魔術字串或整數。

```java
enum Status {
    PENDING("等待中"), RUNNING("執行中"), DONE("完成"), FAILED("失敗");

    private final String label;                 // enum 可以有欄位、建構子、方法
    Status(String label) { this.label = label; }
    public String label() { return label; }
    public boolean isTerminal() { return this == DONE || this == FAILED; }
}

Status s = Status.valueOf("RUNNING");           // 字串 → enum；不合法丟 IllegalArgumentException
for (Status st : Status.values()) {
    System.out.println(st + " " + st.ordinal() + " " + st.label());
}

String msg = switch (s) {                       // 搭配 switch：漏掉某個值時編譯器會提醒
    case PENDING, RUNNING -> "in progress";
    case DONE -> "ok";
    case FAILED -> "check logs";
};
```

| 好處 | 說明 |
| --- | --- |
| 防止無效值 | 只能是宣告過的常數 |
| 意圖明確 | `Status.DONE` 比 `"done"` 或 `3` 清楚 |
| 集中管理 | 相關常數、標籤、行為放在一起 |

> `ordinal()` 是宣告順序，插入新常數就會改變；不要存進資料庫或當商業邏輯，存 `name()`。

## `Optional`

明確表示「可能沒有值」，取代回傳 `null`：

```java
Optional<String> found = names.stream().filter(n -> n.startsWith("Z")).findFirst();
found.orElse("none");                          // 沒有值時的預設
found.ifPresent(System.out::println);
found.map(String::length).orElse(0);
```

只用在回傳值；不要用在欄位或方法參數。

## 遞迴 (Recursion)

方法呼叫自己來解較小的子問題；必須有**基底情況 (base case)** 讓呼叫停止。

```java
static long factorial(int n) {
    if (n <= 1) return 1;            // 基底情況
    return n * factorial(n - 1);     // 遞迴情況：問題變小
}
```

| 適合 | 不適合 |
| --- | --- |
| 結構自相似：樹、目錄、巢狀資料 | 深度很大（JVM 預設堆疊約數千到上萬層，超過丟 `StackOverflowError`） |
| 分治法：合併排序、二分搜尋 | 子問題大量重疊卻沒記憶化（費氏數列的天真遞迴是指數時間） |

演算法層面的說明見 [排序演算法](../../computer-science-foundations/sorting-algorithms.md)、[圖走訪](../../computer-science-foundations/graph-traversal.md)。
