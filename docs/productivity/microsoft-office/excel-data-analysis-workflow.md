# Excel Data Analysis Workflow

這份筆記整理的是 Excel 在實務分析中的一條常見工作流：先探索資料、再做分類與彙總、接著跑 what-if 分析，最後進到基礎 forecasting。

## Where Excel Fits

Excel 很適合處理這類問題：

- 手上已有 tabular data，想先快速理解資料分布
- 需要用 business-friendly 的方式切分客群或群組
- 想測試不同假設對結果的影響
- 想做初步趨勢外推，而不是直接進統計建模或 Python pipeline

如果需求是快速回答商業問題，Excel 常常不是最完整的工具，但很常是最先被打開的工具。

## 1. Start with Exploratory Analysis

### PivotTables as the First Lens

當資料量已經超過肉眼掃描，`PivotTable` 通常是第一個該想到的分析工具。

它的角色不是單純「做報表」，而是先快速回答：

- 哪些維度最值得切分
- 哪些群組差異最大
- 哪些指標值得往下追

### Useful PivotTable Features

在探索階段，特別值得記住的是：

- `Calculated Fields` 或計算欄位：補出原始資料沒有直接提供的指標
- `Grouping`: 將日期、區間或類別做更高層級整理
- `Slicers` 與 `Timeline slicers`: 讓 filter 變得更可操作，也更適合 demo 或 review

一個很實務的心法是：

- raw table 保持乾淨
- 分析邏輯先盡量在 pivot layer 驗證
- 等指標與切法穩定後，再決定是否要把流程搬去 Power Query、SQL 或 BI

## 2. Create Business Segments with Logical Functions

### Why Segmentation Matters

很多分析其實不是直接問「總銷售多少」，而是問：

- 哪些客戶值得關注
- 哪些群組成長最快
- 哪些分類方式能對應商業決策

這時候 spreadsheet 裡最常見的下一步，就是先做 customer segmentation 或 rule-based labeling。

### Core Logical Patterns

#### `IF`

最基本的條件判斷：

```excel
=IF(logical_test, value_if_true, value_if_false)
```

適合二元判斷，例如：

- 是否達標
- 是否續約
- 是否屬於某區間

#### Nested `IF`

當分類不只兩種時，會看到巢狀 `IF`：

```excel
=IF(test_1, result_1, IF(test_2, result_2, fallback))
```

它能做事，但很快就會變難讀。只要規則超過幾層，就要開始考慮是否有更好的寫法。

#### `IFS`

`IFS` 用來取代過長的 nested `IF`：

```excel
=IFS(test_1, result_1, test_2, result_2, test_3, result_3)
```

特點是：

- 回傳第一個為 `TRUE` 的結果
- 沒有內建 `else`
- 若沒有任何條件成立，可能回傳 `#N/A`

因此常見寫法會在最後補一個永遠為真的 fallback 條件。

#### `SWITCH`

當情境是「某個值對應某個固定輸出」，`SWITCH` 比多層 `IF` 更清楚：

```excel
=SWITCH(expression, value1, result1, value2, result2, default)
```

適合：

- code-to-label 映射
- status 轉換
- 等值分類

### Aggregation Functions for Segments

做完分類後，下一步常常不是逐列看結果，而是針對群組做彙總。

這時候常用：

- `SUMIF`
- `SUMIFS`
- 以及同型的條件聚合函數

心智模型很簡單：

- 先用邏輯函數把群組定義清楚
- 再用條件聚合把每個群組的指標算出來

## 3. Use What-If Analysis Before Committing to a Decision

### Scenario Analysis

scenario analysis 問的是：

- 如果某些輸入改變，結果會變成什麼？

它比較像是建立幾組離散版本，例如：

- conservative
- base
- aggressive

重點不是求唯一正確答案，而是比較不同假設下的結果差異。

### Sensitivity Analysis

sensitivity analysis 問的是：

- 當某個輸入在一段範圍內變動時，輸出會怎麼反應？

它比 scenario analysis 更連續、更開放，適合看：

- 哪個輸入最敏感
- 結果是否穩定
- 風險是否集中在少數假設

### Key Concepts

- `Independent variables`: 模型外部給定的輸入
- `Dependent variables`: 依賴輸入計算出的輸出

例如：

```text
Taxes Owed = (Total Income - Deductions) * Tax Rate
```

這裡輸入是 income、deductions、tax rate，輸出則是 taxes owed。

### Excel Tools to Remember

#### Goal Seek

當你知道「想要的結果」，但不知道要把哪個輸入改成多少時，用 `Goal Seek` 很方便。

典型問題：

- 毛利率要到 `20%`，售價該設多少？
- 期末金額要到某目標，本期投入該是多少？

#### Scenario Manager

當你有幾組固定假設要反覆比較時，`Scenario Manager` 比手動改格子穩定得多。

適合：

- best / base / worst case
- 不同價格組合
- 不同成長率假設

#### Data Table

當你想觀察一個或兩個輸入在一個範圍中變化時對輸出的影響，`Data Table` 很適合做 sensitivity grid。

它常用來回答：

- 折扣率從 `5%` 到 `30%` 時，利潤怎麼變？
- 單價與銷量同時變動時，營收怎麼變？

## 4. Move from Description to Forecasting

### Forecasts Are Not Outcomes

forecasting 的基本心法很重要：

- forecast 是 prediction，不是事實
- 它依賴歷史資料與方法假設
- 環境變了，模型可能很快失效

### Basic Concepts

#### Seasonality

seasonality 指的是表現和時間週期之間存在規律關聯，例如：

- 月份
- 季節
- 節日

如果你的資料有明顯 seasonality，用單純平均去預測通常會失真。

#### Bias

forecast bias 可以理解成預測長期偏高或偏低的系統性偏差。

這類問題常見於：

- 模型只跟到舊趨勢
- 有結構變化卻沒更新方法
- 使用過度簡化的平均法

#### Confidence Intervals

confidence interval 不是保證區間，而是用來表達預測不確定性。

實務上它提醒我們：

- 不要只看單點預測
- 預測範圍越寬，不確定性越高

### Simple Forecasting Techniques

#### Simple Moving Average

用最近幾期的平均值作為下一期預測。

優點：

- 簡單
- 適合平滑短期波動

限制：

- 對突發變化反應慢
- 不會自動理解 seasonality

#### Weighted Moving Average

給近期資料更高權重。

概念上是：

```text
sum(value * weight) / sum(weight)
```

例如：

```text
[(2 x 0.15) + (3 x 0.35) + (4 x 0.50)] / (0.15 + 0.35 + 0.50) = 3.6
```

它比簡單平均更能反映「最近資料比較重要」的情境。

#### Trendlines

如果需求主要是看方向，chart 上的 trendline 是非常直覺的起點。

它不是完整預測系統，但很適合先回答：

- 整體是上升還是下降
- 線性趨勢是否明顯

#### `FORECAST.ETS()` and `FORECAST.ETS.CONFINT()`

當資料有時間序列結構時，Excel 內建的 ETS 系列函數可以比手動平均更進一步。

可以先這樣理解：

- `FORECAST.ETS()`: 產生預測值
- `FORECAST.ETS.CONFINT()`: 估計預測區間寬度

它適合做 workbook 內的時間序列預測原型，但若需求涉及模型比較、特徵工程或回測，通常就該離開純 Excel。

## 5. A Practical Flow

可以把整條分析路線濃縮成這樣：

1. 先用 `PivotTable` 找出值得追的維度與指標。
2. 用 `IF` / `IFS` / `SWITCH` 建立業務上可用的分類。
3. 用 `SUMIF(S)` 等函數把群組結果彙總出來。
4. 用 `Goal Seek`、`Scenario Manager`、`Data Table` 測試假設。
5. 用 moving average、trendline 或 `FORECAST.ETS()` 做初步外推。
6. 當流程變得重複、資料變大、邏輯變複雜，再移往 Power Query、BI、SQL 或 Python。

## Mental Model

這份筆記的重點不是「Excel 也能做資料科學」，而是：

- Excel 很適合分析起步
- 它擅長把商業問題快速轉成表格邏輯
- 當分析需求成長時，最重要的是知道什麼時候該升級工具
