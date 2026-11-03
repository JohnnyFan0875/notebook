[程式語言](../README.md) › [Java](README.md) › 控制流程與方法

# Java 控制流程與方法 (Control Flow and Methods)

把邏輯包成可重用的方法 (method)，用條件選擇要執行的程式碼，用迴圈重複執行。本篇停在程序式層次；類別設計見 [OOP](java-oop.md)。

## 方法

```java
public class Main {
    static void sayHello(String name) {           // void：不回傳值
        System.out.println("Hello " + name);
    }

    static int square(int number) {               // 回傳型別 int，必須 return 對應的值
        return number * number;
    }

    static boolean isEven(int n) {
        return n % 2 == 0;
    }

    public static void main(String[] args) {
        sayHello("Maria");                        // 定義了也要呼叫才會執行
        int squared = square(5);                  // 25
        System.out.println(isEven(2345) ? "Even" : "Odd");
    }
}
```

| 組成 | 說明 |
| --- | --- |
| 修飾詞 | `public` / `private`、`static`（屬於類別，不需建立物件就能呼叫） |
| 回傳型別 | `void` 或任何型別 |
| 參數 | 輸入；多個參數以逗號分隔，各有型別 |
| 傳值 (pass by value) | 基本型別傳值的複本；物件傳「參考的複本」：方法內修改物件內容會影響外部，但重新指派參數不會 |

> `static main` 只能直接呼叫 `static` 方法；要呼叫非 static 方法得先建立物件（`new Main().sayHello(...)`）。

## 條件

```java
if (score >= 90) {
    System.out.println("Excellent");
} else if (score >= 70) {                         // 一旦某分支成立，後面的分支不再檢查
    System.out.println("Good effort");
} else {
    System.out.println("Keep trying");
}

if (score > 80 && isAttending) { ... }            // && 且、|| 或、! 非；短路求值
```

### `switch`

```java
// 傳統寫法：每個 case 要 break，否則會「穿透」執行到下一個 case
switch (direction) {
    case 'N':
        System.out.println("North");
        break;
    case 'S':
        System.out.println("South");
        break;
    default:
        System.out.println("Unknown");
}

// Java 14+：箭頭語法不會穿透，且可當運算式回傳值（優先使用）
String label = switch (direction) {
    case 'N' -> "North";
    case 'S' -> "South";
    case 'E', 'W' -> "East/West";
    default -> "Unknown";
};
```

## 迴圈

```java
for (int i = 0; i < 5; i++) { ... }               // 初始化; 繼續條件; 每輪更新

String[] names = {"Ana", "Ben", "Cara"};
for (int i = 0; i < names.length; i++) {          // 需要索引時
    System.out.println(i + ": " + names[i]);
}
for (String name : names) {                       // 增強型 for：只需要元素時
    System.out.println(name);
}

int counter = 0;
while (counter < 3) {                             // 次數未知時；確保條件會變成 false
    counter++;
}

do { ... } while (cond);                          // 至少執行一次

for (int i = 0; i < 10; i++) {
    if (i == 2) break;                            // 跳出迴圈：只印 0、1
    if (i % 2 == 1) continue;                     // 跳過本輪
}
```

| 迴圈 | 何時用 |
| --- | --- |
| `for` | 次數已知、需要索引 |
| 增強型 `for` | 走訪陣列或集合的每個元素 |
| `while` | 依條件重複，次數未知（讀檔到結尾、重試） |
| Stream | 篩選 / 轉換 / 彙總的資料管線，見 [Stream API](java-file-io-and-streams.md#stream-api) |

## 常見錯誤

| 錯誤 | 結果 |
| --- | --- |
| 傳統 `switch` 忘了 `break` | 穿透執行後續 case |
| `for` 邊界寫成 `i <= arr.length` | 差一錯誤 (off-by-one)，`ArrayIndexOutOfBoundsException` |
| `while` 內沒有改變條件依賴的變數 | 無限迴圈 |
| 非 `void` 方法某條路徑沒有 `return` | 編譯錯誤 |
| 從 `static main` 呼叫非 static 方法 | 編譯錯誤 |
| 條件寫得又長又密 | 抽成有名稱的 `boolean` 變數或方法 |
