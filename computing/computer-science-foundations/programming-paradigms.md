[Computing](../README.md) › [CS 基礎](README.md) › 程式設計範式

# 程式設計範式 (Programming Paradigms)

範式 (paradigm) 是組織程式的思考方式：怎麼拆解邏輯、怎麼管理狀態、什麼是可重用的單位。重點不在語法，而在結構。同一個問題可以用不同範式解，現代語言（Python、R、Scala、Julia、Java 8+）多半是多範式，依情境混用。

## 總覽

| 大類 | 強調 |
| --- | --- |
| 命令式 (imperative) | **怎麼做**：一步步改變狀態 |
| 宣告式 (declarative) | **要什麼**：描述結果，不寫出每一步 |

| 範式 | 大類 | 拆解單位 | 狀態 | 典型語言 / 工具 |
| --- | --- | --- | --- | --- |
| 程序式 (procedural) | 命令式 | 程序 / 函式 + 依序控制流 | 可變、常共享 | C、bash、腳本式 Python / R |
| 物件導向 (object-oriented, OOP) | 命令式 | 物件（資料 + 行為） | 封裝在物件內 | Java、C++、Python class |
| 函數式 (functional) | 宣告式 | 純函式與轉換 | 盡量不可變 | Haskell、Scala、R 的 `purrr`、Python `map` |
| 宣告式查詢 / 設定 | 宣告式 | 規則、查詢 | 由系統管理 | SQL、Snakemake 規則、Dockerfile、[React](../web-development/react/react-overview.md) |

```python
# 同一個問題：品質分數 >= 30 的 reads 平均長度
reads = [("r1", 150, 35), ("r2", 120, 28), ("r3", 148, 33)]   # (id, 長度, 品質)

# 程序式：迴圈 + 可變狀態
total, n = 0, 0
for _id, length, q in reads:
    if q >= 30:
        total += length; n += 1
mean = total / n                                       # 149.0

# 函數式：篩選 → 轉換 → 彙總，不修改任何變數
from statistics import mean
mean(length for _id, length, q in reads if q >= 30)    # 149.0

# 宣告式（SQL）：SELECT AVG(length) FROM reads WHERE q >= 30;
```

## 程序式 (Procedural)

程式由程序（子程式、函式）組成，依序執行並修改變數。

| 優點 | 限制 |
| --- | --- |
| 控制流清楚、好上手 | 共享的可變狀態在大型系統中難以追蹤 |
| 適合腳本、自動化、有明確步驟的任務 | 責任沒分清時容易高度耦合 |

## 函數式 (Functional)

以函式組合來表達程式，強調**純函式 (pure function)**：相同輸入永遠回傳相同輸出，且沒有副作用（不改共享狀態、不寫檔）。

| 概念 | 說明 |
| --- | --- |
| 不可變 (immutability) | 建立新值而不是修改舊值 |
| 高階函式 (higher-order function) | 函式可當參數或回傳值：`map`、`filter`、`reduce`、`sorted(key=...)` |
| 組合 (composition) | 小函式串成管線：pandas method chaining、R 的 `\|>` |

| 優點 | 限制 |
| --- | --- |
| 容易推理與測試（輸入決定輸出） | 本質上有狀態的問題寫起來彆扭 |
| 天然適合平行（沒有共享狀態） | 抽象風格的學習曲線 |
| 適合資料轉換管線 | — |

> 資料分析其實大量使用函數式思維：pandas / dplyr 的 method chaining、Spark 的 transformation、[工作流引擎](../workflow-engines/README.md)的每個步驟（輸入檔 → 輸出檔，無隱藏狀態）。R 的函數式寫法見 [R 函數式程式設計](../../data-science/r-foundations/README.md)。

## 物件導向 (Object-Oriented)

把資料與操作它的行為綁在物件裡。

| 概念 | 意義 |
| --- | --- |
| 類別 (class) | 藍圖：定義共有的結構與行為 |
| 物件 / 實例 (object / instance) | 依類別建立的具體個體 |
| 屬性 (attribute / field) | 物件存的資料 |
| 方法 (method) | 物件的行為 |
| 封裝 (encapsulation) | 隱藏內部狀態，只透過方法存取 |
| 繼承 (inheritance) | 子類別沿用父類別的結構與行為 |
| 多型 (polymorphism) | 同一介面，不同類別各自實作（`model.fit()` 對任何 sklearn 模型都成立） |

| 優點 | 限制 |
| --- | --- |
| 適合描述有狀態與行為的實體 | 過深的繼承階層讓程式難懂 |
| 封裝降低耦合，適合大型應用 | 不是每個問題都適合建模成一群物件 |

> **組合優於繼承 (composition over inheritance)**：只有真正的「is-a」關係且抽象穩定時才用繼承；需要彈性組裝行為時用組合（物件持有其他物件）。Python 的 OOP 見 [Class](../../data-science/python-foundations/class.md)，Java 見 [Java OOP](../programming-languages/java/java-oop.md)。

## 怎麼選

| 問題特性 | 傾向 |
| --- | --- |
| 依序執行的步驟、一次性腳本 | 程序式 |
| 主要是資料轉換、需要平行 | 函數式 |
| 有狀態的實體互動（模擬、GUI、遊戲、大型應用） | 物件導向 |
| 描述想要的結果，讓系統決定怎麼做 | 宣告式（SQL、設定檔、規則） |

把範式當設計決策而不是信仰；在同一個專案中依各部分的特性混用，通常比強迫單一風格更好。
