# DataLab Workflow

這篇整理 DataCamp DataLab 的工作流心智模型。重點不是把每個 UI 按鈕都記起來，而是理解它在資料探索、SQL 查詢、快速視覺化與可交付 notebook 工作流中的角色。

Key point: DataLab 比較像一個把 notebook、SQL、DataFrame、chart 與 AI assistant 接在一起的分析工作台。它適合快速探索與分享，但不應把平台自動化能力誤認成 analysis 本身。

## What DataLab Is Good At

DataLab 特別適合：

- 快速連接 CSV 或 Google Sheets
- 在同一個 workbook 裡混用 SQL、Python、R
- 把 SQL 查詢結果直接變成 DataFrame 或 chart
- 用 AI assistant 加速草稿、debug 與 workbook 整理
- 多人一起在 notebook 式工作流中協作
- 把分析整理成可重跑、可分享的 notebook

如果需求是「先把資料拉進來，快速看資料、做幾個查詢、畫圖、再交付 workbook」，這類平台就很順手。

## Workbook vs Notebook

這是 DataLab 很值得先釐清的分層。

- notebook: 由 cell 組成，用來實際撰寫與執行分析
- workbook: notebook 的容器，也同時承載檔案、輸出與 data connections

心智模型上，可以把 workbook 想成分析專案的外層殼，notebook 則是裡面真正執行分析的工作頁。

這個區分很實用，因為它能幫你理解：

- 為什麼 workbook 比單一 notebook 更接近可交付分析包
- 為什麼資料連線、檔案與輸出會和 notebook 一起被管理
- 為什麼 DataLab 特別適合分享與協作

## Environment Model

DataLab 的 SQL cells 可以出現在 Python 與 R environment 中。  
心智模型上，它不是一個只會跑 SQL 的 database client，而是一個多語言分析工作台。

這代表：

- 你可以先用 SQL 篩資料
- 再把結果交給 Python / R 做後續處理
- 最後在同一份 workbook 裡補 chart 或說明文字

## Cell Model

cell 是 DataLab notebook 的基本組成單位。  
它們不只放 code，也負責把分析流程切成可閱讀、可檢查、可重跑的步驟。

常見角色包括：

- text cells: 補標題、說明、分析脈絡與操作指引
- SQL cells: 做篩選、彙總與查詢
- Python / R cells: 做資料處理、建模或後續分析
- chart / explore cells: 快速檢查結果與視覺化

如果 workbook 很快變亂，通常不是工具不行，而是 cell 粒度、命名與順序沒有整理好。

## Connecting Data Sources

對常見入門情境，DataLab 可以直接接：

- CSV files
- Google Sheets

它的好處是很多情境不需要自己先架資料庫或做額外安裝，就能開始查詢。

對 DataLab 來說，data connection 是 workbook 層級的重要資產，而不只是某一格 SQL 的臨時來源。

### Querying files

查 Google Sheet 時，sheet 名可直接當資料來源名稱：

```sql
SELECT *
FROM 'Sheet1';
```

查 CSV 時，檔名本身可以直接當成來源：

```sql
SELECT *
FROM sales_data.csv;
```

這種 workflow 很適合：

- demo
- 教學
- ad hoc exploration
- 輕量型分析草稿

但如果資料量、權限治理或資料品質要求變高，通常還是需要更正式的 warehouse / database workflow。

## SQL Cell Modes

DataLab 的 SQL cell 有兩種重要心智模式。

### DataFrame Mode

DataFrame mode 會把查詢結果存成 pandas DataFrame，讓結果能被後續 cell 重用。

適合：

- 想把查詢結果交給 Python 做後處理
- 想把中間結果保存成後續分析 building block
- 想在 notebook 內逐步拆解分析流程

### Query Mode

Query mode 會回傳查詢結果預覽，並保留查詢本身供後續重用。

適合：

- 查詢較慢時先保留 query layer
- 想把查詢當成後續 cell 的邏輯 building block
- 想把 SQL workflow 拆成幾個可檢查的步驟

課程中的心智模型把它類比成比較接近 `CTE` 的工作方式，重點是讓查詢邏輯可以分層。

## Chaining SQL With DataFrames

DataLab 的一個實用點是：SQL 查詢結果可以命名成 DataFrame，然後再被後續 SQL 或 Python 使用。

```sql
SELECT *
FROM sales_data.csv
WHERE customer_type = 'New';
```

把結果存成 `new_sales` 後，就可以在新 SQL cell 繼續：

```sql
SELECT *
FROM new_sales;
```

這個模式適合：

- 先做粗篩選
- 再做第二層 summary 或 visualization
- 把 notebook 寫成一串可讀的分析步驟

## Parameterized Queries

DataLab 支援把已存的變數插入 SQL 查詢中。

```sql
SELECT *
FROM sales_data.csv
WHERE quantity_sold > {{min_sales}};
```

這讓 workbook 更接近可重用分析模板，而不是一次性的查詢片段。

適合場景：

- 門檻值會改
- 不同 stakeholder 想看不同 cutoff
- 想保留互動式分析空間

## Explore And Chart Cells

DataLab 不只讓你查表，也讓你快速切到 Explore / Chart 視圖做視覺化。

這類視圖的價值通常在：

- 先快速看欄位
- 驗證查詢結果是否合理
- 用 chart 做初步 pattern check
- 在交付前快速補足基本視覺呈現

它適合 exploratory workflow，但不代表所有圖都應該直接沿用成最後交付版本。  
重要報告仍然要回到 chart design 與 audience fit。

## Collaboration Angle

DataLab 不只是個人 notebook，也很強調協作。

它特別適合：

- 和隊友共用同一份 workbook
- 一邊保留查詢與圖表，一邊補文字解釋
- 快速把分析草稿轉成別人看得懂的工作頁

如果團隊需求是「一起看同一份分析、一起修、一起交付」，這比單純把 `.ipynb` 檔案來回傳更順。

## AI Assistant Workflow

DataLab 的 AI assistant 主要可以幫幾件事：

- generate code
- fix / debug code
- 協助 workbook 管理

### Generate code with context

對 SQL 來說，先把資料載入、讓 assistant 看得到欄位與資料來源，再請它生成查詢，通常比從零開始要穩。

例如課程中的重點：

- 對 SQL，先載入資料再切到 AI
- prompt 越具體越好
- 一定要驗證生成結果

例如：

```sql
SELECT sales_amount
FROM sales_data.csv
WHERE discount > 0.1
  AND sales_rep = 'Bob'
  AND product_category = 'Clothing';
```

這類 prompt 如果條件講得明確，生成結果通常比較可用。

### Debugging with AI

AI 很適合用來：

- 補漏掉的語法細節
- 解釋錯誤訊息
- 幫忙改寫成更可讀的版本

但它不應替代你對欄位、資料定義與商業條件的理解。

## Workbook Management

DataLab 不只是跑一格查詢，而是把分析整理成 workbook。

這表示你要關心：

- cell 的順序是否清楚
- 中間結果是否命名合理
- chart 與文字是否能讓別人接手
- workbook 是否能被重新執行

如果資料會每天更新，DataLab 也支援 schedule runs 與通知。  
這讓它從單次探索更接近 recurring analysis workflow。

## Practical Workflow

1. 先接好 CSV / Google Sheets 等資料來源。
2. 用 SQL cell 做第一層篩選與 summary。
3. 視需要把重要中間結果存成 DataFrame。
4. 用後續 SQL / Python / R 接續分析。
5. 切到 Chart / Explore 快速驗證結果。
6. 需要時用 AI assistant 補草稿或 debug，但手動驗證輸出。
7. 把 workbook 整理成可重跑、可分享的交付物。

## When It Fits Well

- 教學與 demo
- exploratory analysis
- 輕量共享 notebook
- SQL + Python / R 混合的小型工作流
- 快速把資料探索轉成可交付 workbook

## Common Mistakes

- 把平台自動生成的查詢直接當正確答案
- 沒先載入或理解資料，就要求 AI 從零生成 SQL
- 把 quick chart 當成最終報表，卻沒檢查 audience 與設計品質
- 中間結果命名混亂，導致 workbook 難以接手
- 把 DataLab 的方便性誤認為正式資料治理已經到位

## Related Topics

- [Data-Driven Decision Making](./data-driven-decision-making.md)
- [Reports and Presentations](./reports-and-presentations.md)
- [Sigma Overview and Workflow](./sigma-overview-and-workflow.md)
- [Tableau](./tableau/README.md)
