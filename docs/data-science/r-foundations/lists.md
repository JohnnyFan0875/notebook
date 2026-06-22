# Lists in R

當你需要把不同型別、不同形狀的物件包在一起時，R 的 list 是最自然的容器。它和 vector 不同，list 不要求每個元素型別一致。

## Why Lists Exist

分析工作常需要把多種物件放在一起，例如：

- 一個資料表
- 一段 metadata
- 幾個模型物件
- 一組參數設定

這時 list 比 vector 或 data frame 更適合。

## Creating a List

```r
company_name <- "DataCampers Inc."

cash <- data.frame(
  company = c("A", "A", "A", "B", "B", "B", "B"),
  cash_flow = c(1000, 4000, 550, 1500, 1100, 750, 6000),
  year = c(1, 3, 4, 1, 2, 4, 5)
)

my_company <- list(company_name, cash)
```

這個 list 的第一個元素是字串，第二個元素是 data frame。這正是 list 的價值所在。

## Practical Uses

list 在 R 裡非常常見，因為很多函數本來就會回傳 list，例如：

- 模型擬合結果
- API 回應
- 巢狀資料結構
- 多步驟分析的中間結果

當你後面開始使用 `lapply()`、`sapply()` 時，list 也會變成核心資料結構。

## Mental Model

可以把 list 想成一個容器，裡面每個 slot 都能放完全不同的東西。重點不是長得整齊，而是把相關物件組成一個可攜帶、可傳遞的分析單位。

## Common Mistakes

- 以為 list 應該像 data frame 一樣每個元素長度一致。
- 把本來應該拆成欄位的表格資料硬塞進 list，讓後續操作變複雜。
- 不清楚 list 與 vector 的差別，導致 indexing 與回傳型別判讀混亂。
