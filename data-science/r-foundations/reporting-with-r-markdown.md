# Reporting with R Markdown

R Markdown 把文字、R 程式碼、圖表與文件 metadata 放在同一份檔案裡。它的核心價值不是排版本身，而是讓分析報告可以重新執行、重新輸出，而且不用手動把結果貼到文件中。

如果你的工作是固定每週、每月或每個國家都要重新產出一份報告，R Markdown 幾乎一定比手工複製貼上更穩定。

## 文件的三個元素

一份 `.Rmd` 通常同時包含三層內容：

- metadata：標題、作者、日期、輸出格式等 YAML header。
- text：Markdown 文字說明。
- code：R code chunks 與 inline R。

最小範例：

```yaml
---
title: "Investment Report"
author: "Data Team"
date: "`r Sys.Date()`"
output: html_document
---
```

```markdown
# Summary

This report contains `r nrow(df)` rows.

```{r}
summary(df)
```
```

重點不是語法片段，而是「結果由程式生成，不是手貼進來」。

## Knit 的心智模型

Knit 時會發生幾件事：

- 先讀 YAML header 決定輸出格式。
- 依序執行 code chunks。
- 把 chunk 結果、圖和文字組成最終文件。

這代表報告輸出品質依賴兩件事：

- 資料和程式碼本身是否可重現。
- chunk 選項是否清楚分離「執行邏輯」與「呈現邏輯」。

## 常用 code chunk 寫法

```r
```{r setup, include=FALSE}
library(readr)
library(dplyr)
library(ggplot2)
```
```

```r
```{r}
projects %>%
  count(region)
```
```

常見做法：

- `setup` chunk 放套件載入、全域設定、主資料讀取。
- 真正的分析與圖表拆成獨立 chunk，讓報告更容易維護。
- 不要把大量資料清理邏輯都塞進同一個 chunk。

## 重要 chunk options

最常用的是這三個：

```r
```{r, include=FALSE}
```

```{r, echo=FALSE}
```

```{r, eval=FALSE}
```
```

差異要記清楚：

- `include = FALSE`：程式會跑，但程式碼與結果都不顯示。
- `echo = FALSE`：程式會跑，只隱藏程式碼，保留結果。
- `eval = FALSE`：程式碼顯示，但不執行。

很實用的記法：

- 初始化資料與載入套件常用 `include = FALSE`。
- 想讓讀者看圖表、不看實作細節時常用 `echo = FALSE`。
- 教學文件或示範模板常用 `eval = FALSE`。

也常一起搭配：

```r
```{r, message=FALSE, warning=FALSE}
```
```

避免套件訊息和 warning 把報告版面弄亂。

## Inline R

當你只想在一句文字中插入數值，不需要整塊 code chunk。

```markdown
There were `r nrow(projects)` projects in the filtered dataset.
```

這對摘要段落很好用，因為文字與數值能一起更新，不需要手動改報告敘述。

## 用 Markdown 組織報告

R Markdown 不只是執行 R，也要把內容結構寫清楚。常見元素包括：

- 標題階層 `#`, `##`, `###`
- bulleted lists
- numbered lists
- 一般表格

實務上，標題階層最重要，因為它會直接影響 table of contents 與閱讀導航。

## 表格輸出

如果資料框直接印出來不夠適合閱讀，可以用 `knitr::kable()`。

```r
knitr::kable(
  summary_table,
  caption = "Regional investment summary"
)
```

常見可調整項目：

- 欄名先整理成人類可讀格式。
- 對齊方式依欄位型別調整。
- 補上 caption，讓表格在長報告裡更容易被引用。

如果你只是把 tibble 原樣印出來，技術上可行，但常不夠像正式交付物。

## 文件導覽設定

YAML header 可以直接控制輸出文件的閱讀體驗。

```yaml
---
title: "Regional Report"
output:
  html_document:
    toc: true
    toc_depth: 3
    number_sections: true
    toc_float: true
---
```

常用選項：

- `toc: true`：加入目錄。
- `toc_depth`：控制目錄深度。
- `number_sections: true`：標題自動編號。
- `toc_float: true`：HTML 報告裡加入浮動目錄。

如果章節很多，這些設定比調字體顏色更重要，因為它們直接影響讀者能不能快速找到內容。

## 參數化報告

R Markdown 很適合做同一模板、不同輸入值的批次報告。

YAML 先定義參數：

```yaml
---
title: "Country Report"
params:
  country: "Indonesia"
output: html_document
---
```

在文件中使用：

```r
```{r}
country_projects <- projects %>%
  filter(country == params$country)
```
```

這樣同一份模板就能為不同國家、部門、日期區間重複產出。

必要時可以從外部呼叫：

```r
rmarkdown::render(
  "report.Rmd",
  params = list(country = "Indonesia")
)
```

這比複製十份 `.Rmd` 再各自手改內容穩定得多。

## 什麼內容該藏起來，什麼該露出來

好的報告不會把所有分析細節都顯示給讀者。可以用這個原則判斷：

- 讀者需要結果，但不需要看到資料讀取與清理細節：隱藏 code，保留輸出。
- 讀者需要審查方法：保留關鍵 code。
- 只是報告基礎設定：直接 `include = FALSE`。

R Markdown 的價值不只是「能執行」，而是把同一份分析分成：

- 報告要呈現給讀者的部分。
- 為了產生報告而存在、但不必讓讀者看到的部分。

## 什麼時候適合用 R Markdown

R Markdown 特別適合：

- 定期更新的分析報告。
- 需要把文字、圖表、程式碼放在一起審查的團隊。
- 需要保留可重現交付紀錄的專案。

如果只是一次性的簡單探索，純 script 可能更快；但只要報告會反覆重跑或交給別人維護，R Markdown 很快就會回本。

## 和 Quarto 的關係

現在很多團隊也會用 Quarto。可以把它看成更通用的後繼工作流，但 R Markdown 的核心觀念沒有變：

- 文件是程式生成的。
- metadata 控制輸出。
- code chunk 控制執行與呈現。
- 報告模板應該可以重跑，而不是靠手工修補。
