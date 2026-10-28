[Data Science](../README.md) › [R Foundations](README.md) › R Markdown 與 Quarto

# R Markdown 與 Quarto 報告 (Reproducible Reporting)

把文字、程式碼、圖表放在同一份檔案，報告由程式**重新執行產生**，而不是手動把數字和圖貼進 Word。資料更新、樣本剔除或方法修改後，重新 render 一次全部結果就同步更新。**Quarto**（`.qmd`）是 R Markdown（`.Rmd`）的後繼者，支援 R、Python、Julia，新專案建議直接用 Quarto；兩者觀念與大部分語法相同。溝通層面的寫作原則見 [溝通分析結果](../data-communication/communicating-results.md)。

## R Markdown vs Quarto

| | R Markdown | Quarto |
| --- | --- | --- |
| 副檔名 | `.Rmd` | `.qmd`（也能直接 render `.ipynb`） |
| 本體 | R 套件 `rmarkdown` | 獨立 CLI（RStudio 內建），R 端用 `quarto` 套件呼叫 |
| 語言 | 主要是 R | R、Python、Julia、Observable JS |
| chunk 選項 | 寫在 chunk header：`{r, echo=FALSE}` | 寫在 chunk 內：`#\| echo: false` |
| YAML 輸出格式 | `output: html_document` | `format: html` |
| 網站 / 書 / 投影片 | blogdown、bookdown、xaringan（各自的套件） | 內建：`project: type: website / book`、`format: revealjs` |
| 狀態 | 維護中，不再新增大功能 | 主力開發 |

## 文件結構

````markdown
---
title: "RNA-seq QC report"
author: "Lab"
date: today
format:
  html:
    toc: true
    number-sections: true
    code-fold: true          # 程式碼預設摺疊，讀者可展開
    embed-resources: true    # 單一 HTML 檔，方便寄送
execute:
  echo: false                # 全域：不顯示程式碼
  warning: false
params:
  min_count: 10
---

```{r}
#| label: setup
#| include: false
library(tidyverse)
counts <- read_tsv("data/counts.tsv")
```

## 摘要

共 `{r} ncol(counts) - 1` 個樣本，過濾門檻為每基因至少 `{r} params$min_count` reads。

```{r}
#| label: fig-libsize
#| fig-cap: "各樣本的 library size"
#| fig-width: 7
colSums(counts[-1]) |> enframe() |> ggplot(aes(name, value)) + geom_col()
```

如 @fig-libsize 所示……
````

| 元素 | R Markdown 寫法 | Quarto 寫法 |
| --- | --- | --- |
| YAML 標頭 | `output: html_document` | `format: html` |
| 行內程式碼 | `` `r nrow(df)` `` | `` `{r} nrow(df)` ``（舊寫法也可用） |
| chunk 選項 | ` ```{r label, echo=FALSE} ` | ` ```{r} ` 下一行 `#\| echo: false` |
| 交叉引用圖表 | 需 bookdown | `#\| label: fig-xxx` + `@fig-xxx` |
| 渲染 | `rmarkdown::render("a.Rmd")` | `quarto render a.qmd`（終端機）或 `quarto::quarto_render()` |

## Chunk 選項

| 選項（Quarto 名） | 執行程式？ | 顯示程式碼？ | 顯示結果？ | 用途 |
| --- | --- | --- | --- | --- |
| `include: false` | ✓ | ✗ | ✗ | 載入套件、讀資料、設定 |
| `echo: false` | ✓ | ✗ | ✓ | 給讀者看圖表，不看實作 |
| `eval: false` | ✗ | ✓ | ✗ | 示範程式碼、教學 |
| `output: false` | ✓ | ✓ | ✗ | 只顯示程式碼 |
| `message: false` / `warning: false` | ✓ | | 隱藏訊息 / 警告 | 套件載入訊息 |
| `cache: true` | 只在程式變動時重跑 | | | 耗時的步驟（注意上游資料變了快取不會自動失效） |
| `fig-width` / `fig-height` / `fig-cap` | | | | 圖的尺寸與說明 |

R Markdown 用 `.` 分隔（`fig.width`），Quarto 用 `-`（`fig-width`）。全域設定：R Markdown 用 setup chunk 裡的 `knitr::opts_chunk$set(echo = FALSE)`，Quarto 用 YAML 的 `execute:`。

> `warning: false` 是為了版面，不是為了忽略問題：交付前至少看過一次所有警告。

## 表格

```r
knitr::kable(summary_tbl, digits = 2, caption = "各組摘要")   # 簡單、所有格式都能輸出
gt::gt(summary_tbl) |> gt::fmt_number(decimals = 2)            # 精細排版（HTML / PDF / Word）
DT::datatable(de_results)                                       # HTML 可搜尋、排序的互動表格（差異表現結果）
```

## 參數化報告

同一模板對不同樣本批次、組織、日期區間各產出一份，比複製十份檔案再手改穩定得多。

```r
# R Markdown
rmarkdown::render("qc.Rmd", params = list(batch = "B2"),
                  output_file = "qc_B2.html")

# Quarto（R 端）
quarto::quarto_render("qc.qmd", execute_params = list(batch = "B2"),
                      output_file = "qc_B2.html")

# 批次產出
purrr::walk(c("B1", "B2", "B3"), \(b)
  quarto::quarto_render("qc.qmd", execute_params = list(batch = b),
                        output_file = paste0("qc_", b, ".html")))
```

```bash
quarto render qc.qmd -P batch:B2 --output qc_B2.html
```

文件內用 `params$batch` 取值。

## 輸出格式

| 格式 | Quarto `format:` | 備註 |
| --- | --- | --- |
| HTML | `html` | 互動圖表、`code-fold`、`embed-resources: true` 產生單檔 |
| PDF | `pdf` / `typst` | `pdf` 需 LaTeX（`quarto install tinytex`）；`typst` 不需 LaTeX、編譯快 |
| Word | `docx` | 可用 `reference-doc:` 套用期刊 / 機構的樣式範本 |
| 投影片 | `revealjs` | 實驗室會議報告 |
| 網站 / 書 | `_quarto.yml` 中 `project: type: website` / `book` | 多頁實驗手冊、分析紀錄 |
| 期刊稿件 | Quarto journal extensions、`manuscript` 專案 | 圖表引用、參考文獻（`bibliography: refs.bib`） |

## 可重現報告的檢查清單

| 項目 | 做法 |
| --- | --- |
| 從頭到尾能跑 | 在乾淨 session render（不依賴 console 裡殘留的物件）；RStudio 的 Render 本來就在新 session 執行 |
| 路徑 | 用相對路徑或 `here::here()`，不要寫死 `C:/Users/...` |
| 套件版本 | [renv](reproducible-environments-with-renv.md) 鎖定；報告結尾附 `sessionInfo()` |
| 亂數 | setup chunk `set.seed()` |
| 耗時步驟 | 預先跑完存成 `.rds`，報告只讀入（比 `cache: true` 更透明） |
| 原始資料 | 唯讀，不在報告中覆寫 |

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 在 console 能跑、render 失敗 | 報告用到 console 才有的物件；所有讀取都寫在文件裡 |
| 把整個清理流程塞進一個巨大 chunk | 拆成有 label 的小 chunk，或把清理放在獨立 script，報告只 `source()` / 讀結果 |
| 手動在文字中寫數字 | 改用行內程式碼，資料更新時不會不一致 |
| `cache: true` 後改了上游資料，結果沒更新 | 加 `dependson`，或清除快取資料夾重 render |
| HTML 寄出後圖片不見 | `embed-resources: true`（R Markdown：`self_contained: true`） |
