[Data Communication](../README.md) › [BI 工具](README.md) › Tableau

# Tableau

Tableau 是視覺分析工具：拖放探索、快速迭代問題與圖表、交付互動式 dashboard。它最適合放在分析與溝通的交界，當作分析流程的交付層，而不只是畫圖介面。好的 Tableau 作品從分析問題開始，而不是從空白 dashboard 開始。

## 工作流程

```
形成問題 → 連接資料 → 定義欄位 → 分析 → 組成 dashboard → 溝通決策
```

| 步驟 | 問題 |
| --- | --- |
| 連接 (Connect) | 需要哪些資料來源與表？ |
| 準備 (Prepare) | 欄位需要清理、重新編碼或分組嗎？ |
| 計算 (Calculate) | 缺哪些指標或衍生欄位？ |
| 分析 (Analyze) | 哪些 dimension 與 measure 能揭露模式？ |
| 呈現 (Present) | 哪個 worksheet 或 dashboard 最能支持決策？ |

## Dimension 與 Measure

| 類型 | 意義 | 在視覺中 |
| --- | --- | --- |
| Dimension | 類別 / 質性欄位，用來分組、切分、標籤 | 產生標題列 / 分組（藍色＝離散） |
| Measure | 數值欄位，通常會被聚合（預設 `SUM`） | 產生軸（綠色＝連續） |

常見的建模工作是把數值欄位改成 dimension：郵遞區號、樣本編號、年份這類「數字」不應該被加總。

## 合併資料

視覺再整齊，底層資料合併錯了一樣會誤導。

| 方式 | 用途 | 結果 |
| --- | --- | --- |
| Union | 欄位相同的表縱向堆疊（依月份、地區、檔案拆開的資料） | 列變多；主要風險是各檔 schema 不一致 |
| Join | 依 key 橫向合併互補的欄位 | 欄變多；在資料來源層合併成一張表 |
| Relationship（Tableau 2020.2 起的預設） | 定義表之間的邏輯關係，依視覺用到的欄位才在查詢時 join | 各表保留自己的 grain，較不會因 join 重複計算 |

| Join 類型 | 保留 |
| --- | --- |
| Inner | 兩邊都配對到的列 |
| Left | 左表全部 + 配對到的右表 |
| Right | 右表全部 + 配對到的左表 |
| Full outer | 兩邊所有列 |

選 join 前先問：key 是什麼？分析單位 (grain) 是什麼？需要沒配對到的列嗎？會不會意外重複列？錯誤的 join 是計數膨脹與聚合錯誤的常見來源，見 [JOIN 列數膨脹](../../databases/sql-joins-and-set-operations.md#列數膨脹-fan-out)。不同 grain 的表（訂單 vs 訂單明細）優先用 relationship 而非 join。

## 計算欄位 (Calculated Fields)

計算欄位用既有資料建立新的分析邏輯：補上缺少的指標、轉換欄位、重新編碼或分箱、把業務規則放進視覺層。

| 類型 | 意義 | 例子 |
| --- | --- | --- |
| 列層級 (row-level) | 對每筆記錄個別計算 | `[Sales] - [Cost]`、`DATEPART('year', [Order Date])` |
| 聚合 (aggregate) | 對目前視覺中的一組記錄計算 | `SUM([Profit]) / SUM([Sales])` |
| LOD 運算式 | 在指定的 grain 聚合，不受視覺當前的層級影響 | `{FIXED [Customer ID] : MIN([Order Date])}`（每位客戶的首購日） |
| Table calculation | 對視覺中已算好的值再計算 | 累計總和、排名、與前期差異、佔總計比例 |

```
// 列層級 vs 聚合：利潤率要先聚合再相除
Profit Ratio (錯)  = [Profit] / [Sales]                  // 每列算比率，視覺再加總 → 比率被加總
Profit Ratio (對)  = SUM([Profit]) / SUM([Sales])

// 條件分類
IF [Sales] >= 10000 THEN "High" ELSEIF [Sales] >= 1000 THEN "Mid" ELSE "Low" END

// LOD：客戶層級的指標，再拿來分群
{FIXED [Customer ID] : SUM([Sales])}
```

| 常見錯誤 | 說明 |
| --- | --- |
| 混用列層級與聚合 | 「無法在同一運算式中混合聚合與非聚合引數」 |
| 函式套用到不相容的型別 | 文字欄當數字算、日期未轉型 |
| 語法 | 漏 `END`、逗號、括號 |
| 計算層級與業務意義不符 | 公式有效但分析上錯誤（比率被加總） |

先決定邏輯屬於列層級還是分組層級；公式保持小而可組合；以業務意義命名；用在 dashboard 前先手動抽查結果。

## Dashboard

Tableau dashboard 把多個 worksheet 組成一個互動的決策畫面，支援 drill-down、跨分群比較、KPI 監控、引導式探索（filter action、highlight action、parameter）。價值在於支持決策，而不是展示互動功能；設計原則見 [Dashboard 設計](../dashboard-design.md)。
