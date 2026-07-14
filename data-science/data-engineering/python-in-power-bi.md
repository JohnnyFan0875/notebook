# Python in Power BI

`Python in Power BI` 可以先理解成一種 bridge workflow：

- 資料仍然在 Power BI 的 report / data prep 生態裡流動
- 但某些轉換、統計或視覺化，改交給 Python 來做

如果 [Power BI Overview](power-bi-overview.md) 偏整體平台工作流，這篇比較偏回答一個實務問題：

- 什麼時候 Power Query / Quick Measures 就夠了
- 什麼時候值得拉進 `pandas`、`matplotlib`、`seaborn`

## Why This Matters

很多 Power BI 工作其實卡在這種邊界上：

- GUI 步驟能做，但很繞
- 想畫的圖不是標準 visual
- 想做的統計摘要不只是單一 measure

這時 Python 的價值不是取代 Power BI，而是補它的空白：

- 更自由的資料轉換
- 更彈性的程式化處理
- 更客製的視覺化能力

反過來說，Power BI 對 Python 使用者的價值也很明確：

- 更快把分析結果包成 dashboard / report
- 更容易分享給非程式使用者
- 更容易落到日常商業消費場景

## A Simple Division of Labor

這份課程最有價值的地方，不是語法本身，而是兩邊分工的對照。

可以先這樣理解：

- `Power Query`: GUI-first 的資料載入、清理、join、reshape
- `Quick Measures` / report features: 常見商業計算與互動式報表
- `Python`: 程式化資料處理、缺失值處理、統計探索、自訂視覺化

一個簡化判斷法：

- 如果需求是可重現但不太複雜的清理流程，先想 Power Query
- 如果需求是比較特殊的轉換、imputation、統計摘要或圖表，才考慮 Python

## Setup in Power BI Desktop

在 Power BI Desktop 裡使用 Python，基本上先要讓 Desktop 知道你的 Python environment 在哪裡。

課程裡保留的操作路徑是：

- `File`
- `Options and settings`
- `Options`
- `Python scripting`

也就是說，Power BI 不是自己附 Python runtime，而是去接你本機已安裝好的 Python。

## Package Expectations

來源裡最基本提到的套件是：

- `pandas`
- `matplotlib`

如果要做更進一步的 Python visual，通常也會一起用：

- `seaborn`

對 notebook 來說，比較重要的不是安裝指令，而是先記住：

- Power BI 只是在呼叫本機 Python environment
- 需要的套件要先在那個 environment 裡可用

## Where Python Fits Best

這份課程實際拿了幾個很典型的任務來對照 Power BI 與 Python：

- importing and joining data
- finding missing data
- imputation
- custom visualizations
- correlation analysis

這些任務都有一個共通點：

- Power BI 能做一部分
- Python 往往能提供更自由的表達方式

## Importing and Joining Data

如果只是一般的 merge / append / join，Power Query 通常已經很好用。  
但如果你更習慣程式化流程，`pandas` 的價值在於：

- join 條件更明確寫在 code 裡
- 可以把一整段清理步驟當成程式邏輯維護
- 更容易和其他 Python 分析步驟串起來

所以這裡不是誰絕對比較強，而是：

- GUI workflow 比較重要時，用 Power Query
- 程式可重現性與分析自由度更重要時，用 `pandas`

## Missing Data in Power BI vs Python

來源很適合拿來建立一個簡單心法：

- 先辨識 missing data
- 再決定 missingness 的性質
- 最後才選擇 delete、indicator、imputation 或暫停分析

常見的 missing 表示可能包括：

- `null`
- `NA`
- 特殊占位值，例如 `99`
- 空字串

這提醒我們，missing data 不只是空值問題，也常是資料編碼與 upstream workflow 問題。

## Missing at Random vs Not at Random

這份課程雖然不算完整統計教材，但有一個很值得保留的決策分流：

### Missing at Random

如果缺失比較接近隨機，較常見的做法包括：

- delete the observations
- 加一個 missing indicator
- imputation

### Missing Not at Random

如果缺失本身就反映某種偏差或機制，先不要急著補值。  
比較穩的做法通常是：

- pause analysis
- understand reasons for missing data
- gather more data
- document assumptions and limitations

這個區分很重要，因為它提醒我們：

- 補值不是預設動作
- 有時候 missingness 本身就是訊號

## Imputation Heuristics

來源整理的幾種常見 imputation 包括：

- mean
- median
- mode
- previous / next values

還有兩個很務實的提醒：

- 缺失比例很低時，簡單 imputation 比較合理
- 用前值 / 後值這類方法前，先確認資料已正確排序

對 notebook 來說，可以先保留一個簡化心法：

- 先問 missingness 是不是能被簡化處理
- 再問補值方法是否符合欄位型態與資料順序

## Python Visuals in Power BI

Power BI 裡最值得用 Python 的一類場景，就是 custom visuals。

這份課程主要用 `seaborn` 當例子，因為它很適合快速做：

- histograms
- scatter plots
- joint plots
- pair plots

這些圖在資料探索階段很有價值，尤其當你想看：

- distribution
- relationship between variables
- multiple numeric variables 的整體結構

## A Minimal Plot Workflow

來源把 Power BI 裡建 Python visual 的流程收得很簡潔：

```python
import matplotlib.pyplot as plt
import seaborn as sns

# data transformation steps

sns.some_plot(
    data=dataset,
)

plt.show()
```

重點不是特定函式，而是這個順序：

1. Power BI 把資料交給 Python
2. 你先在 script 裡做必要的 transformation
3. 用 `matplotlib` / `seaborn` 畫圖
4. `plt.show()` 把圖交回 Power BI visual container

## Seaborn Patterns Worth Remembering

這份課程比較值得留下的是圖表類型的判斷，而不是每一頁例子。

### Histogram

`histogram` 比較適合看：

- 單一數值欄位的分布
- 集中區域
- 偏態
- 是否有長尾

### Scatter Plot

`scatter plot` 比較適合看：

- 兩個數值變數之間的關係
- 方向
- 離群點
- 是否可能存在群聚

### Joint Plot

`joint plot` 可以把：

- scatter relationship
- marginal distributions

放在同一張圖裡看，適合快速檢查兩變數關係與各自分布。

### Pair Plot

`pair plot` 比較像多變數 numeric EDA 的快篩工具。  
當你想快速看多個欄位彼此關係時，它通常比一張一張手畫更有效率。

## Correlation in Power BI and Python

這份課程另一個主軸是 `correlation coefficient`。

先保留最基本的心智模型即可：

- 範圍大致在 `-1` 到 `1`
- `-1` 接近強負相關
- `1` 接近強正相關
- `0` 接近沒有線性關係

課程也提醒了一個永遠值得留下的結論：

- correlation does not mean causation

也就是說，看到兩個變數一起動，不代表其中一個造成另一個。

## Correlation Matrix and Heatmap

當變數不只兩個時，用單一 correlation coefficient 就不夠了。  
這時比較自然的做法是：

- 先算 `correlation matrix`
- 再用 `heatmap` 呈現

來源裡的基本 pattern 是：

```python
import seaborn as sns

corr_matrix = dataset.corr()
sns.heatmap(corr_matrix, annot=True)
```

這種做法很適合：

- 快速掃多個 numeric features
- 找出高度相關欄位
- 幫後續建模或 EDA 決定下一步

## Practical Limitations

這份課程也提到幾個 Power BI 裡跑 Python 時要有的 operational awareness：

- Power BI 不是完整的 Python notebook environment
- 資料會以暫時性的 `DataFrame` 形式交給 script
- Python visual 與 script execution 會受資料量與平台限制影響

來源裡還提到一些特定數值限制。  
這些限制很可能隨版本變動，所以對 notebook 來說，比較值得保留的是原則：

- 不要期待在 Power BI Python visual 裡處理非常大的資料
- 需要大型資料處理時，應優先在上游先聚合、抽樣或整理
- Power BI 內的 Python 更適合最後一哩分析與視覺化，不適合當主 ETL 引擎

## When to Stay Native in Power BI

即使會 Python，也不代表每次都該把需求搬進 script。

通常更適合留在 Power BI 原生功能的情境包括：

- 一般 join / append / pivot / unpivot
- 常見商業度量與互動式 filter logic
- 需要讓更多非程式使用者容易維護的流程

因為一旦邏輯搬進 Python script：

- 維護門檻會提高
- 可讀性會更依賴程式背景
- 團隊接手成本也可能變高

## Practical Heuristics

- 先用 Power BI 原生能力解問題；真的不順手時再引入 Python。
- 如果需求是 custom visual、EDA 或特殊統計處理，Python 很有價值。
- missing data 先判斷 missingness，再決定 delete、indicator 或 imputation。
- correlation 只是探索訊號，不是因果證據。
- Power BI 裡的 Python script 比較像分析補充層，不像主資料工程層。

## Relation to Other Notes

- 如果你想先理解整體 Power BI 工作流，可以先看 [Power BI Overview](power-bi-overview.md)。
- 如果你想看 Power Query 的整理流程，可以接著看 [Data Preparation in Power BI](data-preparation-in-power-bi.md)。
- 如果你想看 Power Query 的 reshape / merge / custom column，可以接著看 [Data Transformation in Power BI](data-transformation-in-power-bi.md)。
- 如果你想看 Power BI 裡的報表層與原生視覺化設計，可以接著看 [Report Design in Power BI](report-design-in-power-bi.md)。
- 如果你想把 `pandas` 的 missing data 處理拆開來看，可以接著看 [pandas missing-data](../python-foundations/pandas/missing-data.md)。
- 如果你想把 Seaborn 常見圖表拆開來看，可以接著看 [Seaborn Basics](../data-manipulation-and-eda/visualization/seaborn/basics.md)。

## Mental Model

一句話總結：

Python in Power BI，可以先理解成用 `native BI workflow + selective Python augmentation` 把 Power BI 的資料整理、探索與視覺化邊界往外擴一點。
