# Data Science 重整計畫與 Checklist

> 執行時把本檔複製到 `notebook/data-science-reorg-plan.md`，之後依序勾選。

## Context

`data-science/` 約 490 篇（不含 `src/`）。`statistics/`（88）與 `machine-learning/`（101）已用 `/rewrite-notes` 改寫完成；其餘 ~300 篇仍是原始風格（無麵包屑、英文標題、中英混雜），而且有三類問題：

1. **重複**：同一主題散在多處（missing data ×4、datetime ×3、web scraping ×3、SQL window/transactions/performance 各 PG + SQL Server 一份、AI ethics ×5、LLM prompting ×4、Power BI ×16…）。
2. **位置不對**：Power BI 放在 data-engineering、Scala 放在 data-science、R 的 tidymodels / survey 散在 r-foundations、古典影像處理放在 deep-learning、ACF/分解放在 pandas。
3. **對目標讀者（生資 / ML scientist）價值低**：BI case studies、Fabric 部署、SQL Server triggers / stored procedures、corporate finance、AI strategy / monetizing、Copilot、Sigma / DataLab 等。

目標：先完成**結構整併（刪 → 搬 → 併 → 修連結）**，讓每個主題只有一個家；再用 `/rewrite-notes` 分批改寫風格。結構階段不追求文字品質，合併時可先粗略拼接、刪重複段落，交給改寫階段潤飾。

### 已決定

| 項目 | 決定 |
| --- | --- |
| 低價值筆記 | 直接 `git rm`（git history 可救回） |
| finance / marketing / OR / process-analytics | 收進 `applied-domains/`，保留可遷移的方法，刪 corporate-finance |
| Power BI / Tableau / Sigma | 精簡成 `data-communication/bi-tools/` 下 3–4 篇，刪 case studies、Fabric、Sigma、DataLab |

## 通用規則（每個階段都適用）

- 搬移一律 `git mv`（保留歷史）；合併時把被併檔的獨特內容貼進目標檔，再 `git rm` 被併檔。
- 每搬 / 併 / 刪一個檔，立刻 `Grep` 整個 notebook 找舊路徑，修正所有連入（含 `#anchor`）。已知外部連入見文末附錄。
- 合併時**保留獨特知識點**，只刪重複段落；被併檔的程式碼若是唯一範例要保留。
- 每階段結束跑連結檢查，零錯誤才 commit：
  ```bash
  uv run --no-project ".claude/skills/rewrite-notes/check_links.py" data-science
  uv run --no-project ".claude/skills/rewrite-notes/check_links.py" .
  ```
- 每階段一個 commit（訊息如 `Restructure data-science: phase 1 deletions`）。

---

## Phase 0：準備

- [x] 確認 `git status` 乾淨，從 master 開分支 `ds-restructure`
- [x] 把本計畫存成 `notebook/data-science-reorg-plan.md`

## Phase 1：刪除低價值筆記

先刪，減少後面要搬、要改的量。刪前快速看一眼是否有該救的段落（括號內）。

**data-engineering / BI**
- [x] `data-engineering/customer-churn-analysis-in-power-bi.md`、`hr-analytics-in-power-bi.md`、`financial-analysis-in-power-bi.md`、`trend-analysis-in-power-bi.md`（4 篇 case studies）
- [x] `data-engineering/microsoft-fabric-fundamentals.md`、`microsoft-fabric-environment-design-and-deployment.md`
- [x] `data-engineering/power-bi-service-for-end-users.md`
- [x] `data-engineering/python-in-power-bi.md`（內容已被 `machine-learning/preprocessing/imputation.md` 涵蓋）
- [x] `data-communication/sigma-overview-and-workflow.md`、`datalab-workflow.md`
- [x] `data-communication/data-fluency.md`、`data-driven-decision-making.md`（給商業分析師的素養內容）

**ai-strategy-and-governance**
- [x] `ai-strategy.md`、`monetizing-ai.md`、`digital-transformation.md`、`data-strategy.md`、`data-management.md`、`understanding-artificial-intelligence.md`

**llm**
- [x] `llm/integration/microsoft-copilot-productivity-workflows.md`、`llm-business-workflows.md`
- [x] `llm/prompting/gpt-tools-and-practical-use.md`

**databases**
- [x] `sql-server-triggers.md`、`sql-server-functions-and-stored-procedures.md`
- [x] `oracle-sql-patterns.md`（救：NVL / TO_DATE → 已先建 `databases/sql-dialect-cheatsheet.md`）
- [x] `mysql.md`（救：`LOAD DATA` / 匯出指令 → `sql-dialect-cheatsheet.md`）
- [x] `business-analysis-in-sql.md`（救：ROLLUP / CUBE / GROUPING SETS、EXISTS / correlated subquery → `sql-reporting-patterns.md`）

**r-foundations / EDA / 其他**
- [x] `r-foundations/social-media-analysis.md`（rtweet 依賴已停用的 Twitter API；LDA / sentiment 與 `text-analysis.md` 重複）
- [x] `r-foundations/sas-to-r-mental-model.md`（救：「一切皆物件 / model object / broom」→ `tidyverse-workflow.md`）
- [x] `data-manipulation-and-eda/cohort-analysis.md`（商業 retention；連結改指向 `statistics/survival-analysis/kaplan-meier.md`）
- [x] `finance/corporate-finance/`（整個資料夾 9 篇）
- [x] 跑連結檢查 → 修掉所有指向已刪檔的連結（README 表格列直接刪掉該列）→ commit

## Phase 2：跨資料夾搬移

- [x] `data-engineering/scala-foundations.md` → `computing/programming-languages/scala-fundamentals.md`（與 java / julia 同層），更新該 README
- [x] `python-foundations/web-scraping.md` → `web-scraping/scrapy-and-selectors.md`
- [x] `r-foundations/web-scraping-in-r.md` → `web-scraping/rvest.md`
- [x] `python-foundations/mongodb.md` → `databases/mongodb-pymongo.md`
- [x] `python-foundations/database-access-sqlalchemy.md` → `databases/python-sqlalchemy.md`
- [x] `r-foundations/modeling-with-tidymodels.md` → `machine-learning/packages/tidymodels/README.md`（與 scikit-learn、statsmodels 並列）
- [x] `data-manipulation-and-eda/visualization/dashboard-design.md` → `data-communication/dashboard-design.md`
- [x] `deep-learning/computer-vision/biomedical-image-analysis.md`、`image-processing-with-scikit-image.md` → 新資料夾 `data-science/image-analysis/`（古典影像處理，非 DL）；從 `deep-learning/computer-vision/README.md` 與 `biology/medical-imaging/README.md` 連過去
- [x] `data-engineering/data-versioning-and-dvc.md` → `machine-learning/production/dvc.md`（與 mlflow 並列）
- [x] `ai-strategy-and-governance/data-warehousing.md` → 併入 `data-engineering/dimensional-modeling-and-star-schema.md`（已在 Phase 2 完成，標題改為 Data Warehousing and Dimensional Modeling）
- [x] 建 `applied-domains/`（README），把 `finance/`、`marketing-analytics/`、`operations-research/`、`process-analytics/` 搬進去（`git mv` 整個資料夾，內容合併在 Phase 5）
- [x] `ai-strategy-and-governance/` 改名 → `responsible-ai/`
- [x] 更新 `data-science/README.md` 章節地圖與路線圖 → 連結檢查 → commit

## Phase 3：基礎層整併（Python / R / EDA / web-scraping / databases）

**python-foundations**
- [x] datetime：`pandas/datetime.md` + `pandas/dtypes-strings.md` 的 datetime 段 + `data-type-transformation.md` 的 String↔Datetime → 統一到 `python-foundations/datetime.md`（stdlib + pandas 兩節）
- [x] importing-data：`pandas/creating-data.md` 的 I/O 半部 + `data-type-transformation.md` → 併入 `importing-data.md`；HTTP 段改連 `api-http.md`
- [x] 文字處理：`regex.md` + `string-matching.md` → `text-cleaning-and-regex.md`；連 `computing/operating-system/regex-wildcard.md`
- [x] scripting：`argparse.md`、`if-name-main.md`、`subprocess.md`、`config-files.md`、`file-io.md`、`python-snippets.md` → `scripting-and-cli.md`
- [x] 錯誤處理：`assert.md` + `try-except.md` → `errors-and-assertions.md`
- [x] 效能：建 `performance-and-scaling/`：`efficient-python.md`、`parallel.md`（`multiprocessing.md` + `dask.md`）、`polars.md`；`pandas/performance.md` + `pandas/row-operations.md` 合成 `pandas/performance.md`
- [x] numpy 8 → 4：`array-basics`（properties + creation + indexing）、`vectorization-and-reshape`（operations + reshape-concatenate）、`random-and-statistics`、`linear-algebra`；`operations.md` 裡 DataFrame boolean indexing 移去 pandas
- [x] pandas 21 → ~11：`selection`（indexing-slicing + filtering）、`modifying`（updating + adding-removing）、`ordering-binning-sampling`（sorting + binning + sampling-duplicates）、`dtypes-categorical-strings`（dtypes-strings + categorical）；`index-multiindex`、`groupby`、`reshape-merge`、`statistics`、`missing-data`、`performance` 保留
- [x] `pandas/time-series-visualization.md`：ACF / PACF / decomposition 段併入 `statistics/time-series-analysis/`（autocorrelation、decomposition），繪圖段併入 `pandas/visualization.md`
- [x] `pandas/visualization.md` → 搬到 `data-manipulation-and-eda/visualization/pandas-plotting.md`
- [x] `python-packages.md`：標記過時的 setup.py / MANIFEST.in，改寫階段換成 pyproject + uv（並連 `computing/containers-and-env/`）（已在檔頭加「待改寫」註記）

**r-foundations**
- [x] `vectors.md` + `data-frames.md` + `lists.md` → `data-structures.md`
- [x] `functional-programming-with-purrr.md` + `-advanced.md` + `apply-family.md` → `functional-programming.md`（for vs apply vs purrr）
- [x] `defensive-programming.md` 與 `functions.md` 的 Input Validation / Errors 段去重（併入 functions）
- [x] `statistical-functions.md`：刪 regression 段（改連 `explanatory-modeling-in-r.md`）
- [x] `sampling-in-r.md` + `survey-data-analysis.md` → `statistics/inferential-statistics/survey-sampling.md`（bootstrap 重複段改連 `sampling-estimation.md`）
- [x] `missing-data.md`（R）：刪 MCAR/MAR/MNAR 理論，只留 naniar 工具用法，連到 EDA 的 missing-data

**data-manipulation-and-eda**
- [x] `data-profiling.md` 併入 `eda-workflow.md`（profiling 作為第一節）
- [x] missing data 單一歸屬：機制理論只在 `data-manipulation-and-eda/missing-data.md`；`pandas/missing-data.md` 只留 pandas / missingno API；插補方法只在 `machine-learning/preprocessing/imputation.md`；刪 `matplotlib/advanced.md` 的 missingno 段
- [x] `geospatial-data-in-python.md`：留在原處但 README 標為「選讀」
- [x] matplotlib `line-plot.md` vs `advanced.md` 雙軸 / annotation 去重；seaborn `categorical` vs `distribution` 的 countplot vs histplot 去重

**web-scraping**
- [x] 三篇（scrapy、bs4-selenium、rvest）共用的 CSS vs XPath、User-Agent、節流、合法性移到 `web-scraping/README.md`，各篇只留工具用法
- [x] 記下待修 bug：`random.randint(5)`、Selenium 4 前的 `webdriver.Chrome(ChromeDriverManager().install())`、Scrapy `extract_first` → `.get()`（已在各篇檔頭加「待修」註記）

**databases**
- [x] `postgresql-window-functions-and-pivoting.md` + `sql-server-window-functions.md` → `sql-window-functions.md`（通用）；PG crosstab 留一小節
- [x] `postgresql-transactions-and-exception-handling.md` + `sql-server-transactions-and-error-handling.md` → `sql-transactions.md`（PG / T-SQL 對照欄）
- [x] `postgresql-query-performance.md` + `sql-server-query-performance.md` → `sql-query-performance.md`（通用 + EXPLAIN / execution plan 子節）
- [x] `sql-server-basics.md` + `sql-server-tsql-patterns.md` + `snowflake-sql-patterns.md` + Oracle 救下來的段落 → `sql-dialect-cheatsheet.md`（TOP / LIMIT、NVL / ISNULL / COALESCE、日期函式、FLATTEN 對照表）
- [x] `postgresql.md` → 精簡成 `postgresql-psql-and-copy.md`（psql、`COPY` 匯入匯出）
- [x] JOIN / NULL / aggregation 重複段只留在 `sql-query-foundations.md` 與 `sql-joins-and-set-operations.md`
- [x] 連結檢查 → commit

## Phase 4：中間層整併（data-engineering / data-communication / responsible-ai / llm）

**data-engineering**
- [x] `etl.md` 併入 `processing-and-pipelines.md`
- [x] ~~`ai-strategy` 的 `data-warehousing.md` 併入 `dimensional-modeling-and-star-schema.md`~~（Phase 2 已完成）；`data-modeling-foundations.md` 的 1NF–3NF 改連 `databases/database-normalization.md`
- [x] `databricks-foundations.md` + `databricks-data-management.md` + `databricks-sql.md` → `databricks.md`
- [x] `spark-and-pyspark.md` + `spark-sql-in-pyspark.md` → `spark.md`；`sparklyr.md` 保留；`scalable-processing-and-out-of-core.md` 保留並連 `python-foundations/performance-and-scaling/`、`r-foundations/parallel-programming-in-r.md`
- [x] `snowflake-foundations.md` + `bigquery-foundations.md` + `redshift-foundations.md` → `cloud-data-warehouses.md`（比較表為主）
- [x] `streaming-and-kafka.md` + `aws-streaming-with-kinesis-and-lambda.md` → `streaming.md`
- [x] `governance.md` + `responsible-ai/data-governance.md` → `data-engineering/governance.md`
- [x] `responsible-ai/data-quality.md` + `data-quality-with-great-expectations.md` → `data-engineering/data-quality-checks.md`；連 `statistics/descriptive-statistics/data-quality.md`（雙向）
- [x] Power BI 剩下 8 篇 → `data-communication/bi-tools/`：`power-query.md`（data-connections + data-preparation + data-transformation）、`power-bi-modeling-and-dax.md`（overview + semantic-models + dax）、`power-bi-reports.md`（reports + report-design）
- [x] tableau 3 篇 → `data-communication/bi-tools/tableau.md`（另建 `bi-tools/README.md` 索引，刪 `tableau/`）

**data-communication**
- [x] `communicating-data-insights.md` + `reports-and-presentations.md` → `communicating-results.md`（加可重現報告角度，連 `r-foundations/reporting-with-r-markdown.md`）
- [x] 保留 `forming-analytical-questions.md`、`dashboard-design.md`、`bi-tools/`

**responsible-ai**（原 ai-strategy-and-governance）
- [x] `ai-ethics.md` + `responsible-ai.md` + `data-ethics.md`（保留 FAIR）+ `responsible-ai-data-management.md` + `ai-governance.md` → `responsible-ai.md`
- [x] `data-bias-in-ai.md` → `data-bias-and-representativeness.md`（改寫時補 GWAS ancestry bias、EHR selection bias；已在檔頭加「待改寫」註記）
- [x] `data-privacy.md` + `understanding-gdpr.md` + `data-security.md` → `privacy-and-regulation.md`（改寫時補 HIPAA、de-identification、dbGaP 受控存取；已加註記）
- [x] `understanding-the-eu-ai-act.md` 保留（改寫時補醫療器材 high-risk、MDR / IVDR；已加註記）
- [x] `data-privacy-and-anonymization-in-python.md` → `anonymization-in-python.md`（改寫時補 k-anonymity 對基因型無效；已加註記）
- [x] `ai-security-and-risk-management.md` 保留，連 `machine-learning/production/deployment-and-monitoring.md`

**llm**
- [x] foundations：`chatgpt-overview.md` + `generative-ai-overview.md` + `large-language-models.md` → `foundations/llm-foundations.md`（transformer 內部改連 deep-learning）
- [x] prompting：`prompt-engineering.md` + `chatbot-prompt-design.md` + `chatgpt-customization-and-reusable-workflows.md` → `prompt-engineering.md`
- [x] integration：`llm-application-patterns.md` + `llm-workflows-in-python.md`（API 部分）+ `openai-api-workflows.md` → `llm-api-patterns.md`；`managed-llm-platforms.md` 併入 `choosing-llm-providers-and-model-families.md`
- [x] integration：`multimodal-models-with-hugging-face.md` + `multimodal-openai-workflows.md` → `multimodal.md`
- [x] fine-tuning：`deep-learning/nlp-and-transformers/llm-fine-tuning.md` + `llm-workflows-in-python.md` 的 fine-tune / eval 段 → `llm/integration/fine-tuning.md`（prompt vs RAG vs fine-tune 決策 + LoRA / PEFT，已補決策表與 LoRA / QLoRA 小節）
- [x] operations：`llmops.md` + `operating-agent-systems.md` → `llmops.md`
- [x] rag：`rag/README.md`（135 行完整筆記）內容抽成 `rag/rag-pipeline.md`，README 改回精簡索引
- [x] 資料夾只剩 1 篇的子資料夾（foundations、prompting、operations）考慮攤平到 `llm/` 根目錄（已攤平：`llm/llm-foundations.md`、`llm/prompt-engineering.md`、`llm/llmops.md`）
- [x] 連結檢查 → commit

## Phase 5：上層整併（statistics / ML / DL / applied-domains / network-analysis）

**statistics / machine-learning**（已改寫，只做小幅合併）
- [x] `machine-learning/workflow/data-splitting-and-leakage.md` 拆入 `foundations/data-leakage.md`（概念）與 `preprocessing/train-test-split.md`（操作）後刪除
- [x] `machine-learning/foundations/evaluation-mindset.md` 併入 `evaluation/README.md`
- [x] `statistics/multivariate-analysis/multiple-regression.md`（prediction + Ridge / Lasso / p>n）併入 `machine-learning/foundations/high-dimensional-data.md` / `regularization.md`（解釋 vs 預測段移到 `regression-analysis/multiple-linear-regression.md`）
- [x] `statistics/multivariate-analysis/logistic-lda.md` 刪掉重複的 logistic 段，改名 `lda.md`
- [x] `statistics/multivariate-analysis/clustering.md` 精簡成概觀 + validation / profiling，方法細節連到 ML clustering
- [x] `machine-learning/workflow/kaggle-competition-workflow.md`：blending 段刪掉（連 `ensemble/stacking.md`），README 標「選讀」
- [x] README 標「選讀」：`recommender-systems/`、`association-rules/`、`evaluation/gains-and-lift-curves.md`、`structural-equation-modeling-with-lavaan.md`
- [x] 補交叉連結：`statsmodels/diagnostics` ↔ `assumptions-diagnostics`；`imputation` ↔ EDA missing-data；`descriptive-statistics/data-quality` ↔ `eda-workflow`；`sampling-estimation` ↔ `survey-sampling`；`regression-analysis` → `r-foundations/explanatory-modeling-in-r.md`；`workflow/pipeline-basic` → `packages/tidymodels`；production README → `dvc.md`

**deep-learning**（結構調整；內容補強留到改寫）
- [x] `computer-vision/image-classification-workflow.md` 併入 `convolutional-neural-networks.md`
- [x] `nlp-and-transformers/sequence-models-for-text.md` + `text-representations-and-embeddings.md` → `text-and-sequence-models.md`；連 `llm/rag/embeddings-and-semantic-search.md`、`r-foundations/text-analysis.md`
- [x] `fundamentals/tensorflow-and-keras-basics.md` 標記改寫時縮成「Keras 對照」表（已加檔頭註記）
- [x] 記下改寫時要新增：PyTorch 訓練迴圈（Dataset / DataLoader、optimizer、scheduler、early stopping、dropout / batchnorm）、attention 深入（Q/K/V、multi-head、positional encoding）、autoencoder / VAE、GNN、生資序列與蛋白模型（one-hot CNN、ESM、DNABERT / Enformer、AlphaFold 概念）、單細胞 DL（scVI）、U-Net 分割（清單即本項，Phase 7 批次 7 依此補）
- [x] 記下待修：`torch.cuda.amp` → `torch.amp`；`backpropagation.md` code block 內 `#` 被當標題；`##Kaiming` 標題格式；殘留課程來源字樣與 emoji（已在各檔頭加「待修」註記；`backpropagation.md` 檢查後 code fence 正常，`#` 只是註解，不需修）

**applied-domains**
- [x] `finance/`：`portfolio-analysis.md` + `quantitative-risk-management.md` + `stock-price-simulation-and-volatility.md` → `portfolio-and-risk.md`；`trading-strategies-and-backtesting.md`、`credit-risk-modeling.md` 保留；`insurance-and-annuity-valuation.md` 保留（連 survival analysis）；`fundamental-financial-concepts.md` + `bond-valuation-and-interest-rate-risk.md` → `financial-concepts.md`；`financial-data-ingestion-and-cleaning.md` 只留金融特有段併入 `financial-concepts.md`；`autocorrelation.md` 併入 `statistics/time-series-analysis/autocorrelation.md` 的金融小節
- [x] `marketing-analytics/` 3 篇 → `applied-domains/marketing-response-and-choice-models.md`（保留與 `ab-testing.md` 互連）
- [x] `operations-research/` 2 篇 → `applied-domains/optimization.md`
- [x] `process-analytics/` → `applied-domains/process-mining.md`（強調醫療流程 event log）
- [x] `applied-domains/README.md` 寫成精簡索引

**network-analysis**
- [x] 保留 4 篇；`network-analysis-case-studies.md` 刪掉重複的指標說明；記下改寫時補 PPI / 共表現網路範例（已加檔頭註記）
- [x] 連結檢查（data-science + 全 notebook）→ commit

## Phase 6：頂層 README 與入口

- [x] 重寫 `data-science/README.md`：新章節地圖、依讀者類型的建議路線（生資 / ML / 選讀的工程與 BI），移除已刪章節
- [x] `understanding-data-science.md` 精簡（改寫階段處理文字）（已刪 Where Python Fits / 入門 CSV 範例 / 重複的 mental model 段，加麵包屑）
- [x] 全 notebook 連結檢查零錯誤 → commit → 合併回 master（使用者確認後）（已合併）

## Phase 7：用 `/rewrite-notes` 分批改寫

每批 10–30 篇、一個子資料夾；每批完成跑連結檢查、commit 再做下一批。依「被引用越多越先做」排序：

- [X] 批次 1：`python-foundations/`（不含 numpy / pandas）（補 pyproject + uv、`default_rng`、scipy.stats 對照）（已新增 `scipy-stats.md`；`python-packages.md` 改為 pyproject + uv；補回 phase 3 合併時被截斷的 `datetime.md` pandas 段）
- [X] 批次 2：`python-foundations/numpy/` + `pandas/`（view vs copy、dtype、Parquet / HDF5）（已新增 `pandas/memory-and-storage.md`；NumPy view vs copy、dtype 溢位；pandas 3 Copy-on-Write / `str` dtype；更新 `applymap`、`resample("M")`、`stack(dropna=)`、`np.random.seed`；補回被截斷的 `creating-data.md` / `modifying.md` 結尾）
- [X] 批次 3：`r-foundations/` 前半：資料結構、tidyverse、dplyr、tidyr、data.table、importing、datetime、missing（連 Bioconductor 筆記）（另含 categorical、control-flow、functions、defensive-programming、statistical-functions、README；補 matrix / `SummarizedExperiment`、`join_by()` 區間 join、`relationship`、data.table rolling / `foverlaps`、httr2、DBI 參數化查詢、arrow / duckdb、生資檔案格式表、Excel 基因名轉日期；修 `&&` 長度 > 1 在 R ≥ 4.3 報錯、`separate()` → `separate_wider_*()`、`across(..., na.rm=)` 棄用、`XLConnect` → `openxlsx`；`bioconductor-introduction.md` 加回連）
- [X] 批次 4：`r-foundations/` 後半：functional、OOP、效能、Rcpp、parallel、package、R Markdown、regex、text（補 renv、Quarto）（另含 string-distance、explanatory-modeling、README；新增 `reproducible-environments-with-renv.md`；R Markdown 改為 R Markdown 與 Quarto 對照；OOP 補 S4 / Bioconductor accessor；parallel 補 BiocParallel、平行亂數、`availableCores()`；purrr 1.0 新寫法（`list_rbind`、`list_flatten`、`list_transpose`、`pluck_depth`）；修 `amatch()` 預設 `maxDist = 0.1` 回傳 NA、`partial(mean, trim = 2)`；explanatory-modeling 補 formula 語法、參考組、emmeans、glm）
- [X] 批次 5：`data-manipulation-and-eda/`（含 visualization/）（全 21 篇改寫；EDA 補 omics 矩陣 QC（樣本 / metadata 對齊、library size、PCA 看批次）、Python ↔ R 對照；missing-data 補生資缺失型態（proteomics MNAR、scRNA 0、genotype、EHR、dropout）並以模擬圖取代外連圖；圖表設計補 dynamite plot、色盤 / 色盲、出版輸出；seaborn 補 `ecdfplot`、`common_norm` 陷阱、`errorbar` 對照、`clustermap` 表現量矩陣；新增 4 張圖（缺失機制、bar vs points、overplotting、bins / 頻寬）；修 `boxplot(labels=)` → `tick_labels=`、`vert=` → `orientation=`、`ci=` → `errorbar=`、`join=False`、`sym=`、`iris.corr()` → `numeric_only=True`、logistic `regplot` 字串 y、`resample("M"/"Q"/"Y")` → `ME/QE/YE`、`Series.hist(title=)`、`"seaborn"` 樣式名、box plot 鬚 ≠ min/max、`residplot` x 軸標籤、Q-Q `line="45"` 需標準化殘差）
- [X] 批次 6：`databases/` + `web-scraping/`（修 web-scraping bug；考慮補 DuckDB / Parquet）（全 19 篇改寫 + 新增 `databases/duckdb-and-parquet.md`（查 CSV / Parquet / DataFrame、分區 Parquet、BED vs VCF 座標的區間 join、R 用法）；SQL 補 NULL 三值邏輯與 `NOT IN` 陷阱、join 列數膨脹、`LEFT JOIN` 條件放 `ON` vs `WHERE`、`EXCEPT`、window frame `RANGE` 同值陷阱、`QUALIFY`、條件聚合 pivot、隔離層級異常表、index 失效寫法 / 最左前綴 / keyset 分頁、方言表加 DuckDB 欄與跨平台陷阱、GO 祖先遞迴查詢與防環、PostgreSQL 權限 `DEFAULT PRIVILEGES` / `pg_restore`、SQL ↔ pandas ↔ dplyr 對照；修整數除法造成佔比為 0、`DATE_PART('month')` 混年份、`crosstab` 單參數缺值錯位、空泛的 `ROW_NUMBER` 去重範例、SQLAlchemy 1.x API（`select([...])`、`autoload=True`、`table_names()`、`Decimal`、未 commit）→ 2.x；web-scraping 修 `random.randint(5)`、`ChromeDriverManager` / `find_element_by_*` → Selenium 4、`extract_first` → `.get()`、迴圈內 `//` 抓到整頁、`html_elements` 造成欄位錯位、httr → httr2、補 `read_html_live()`、`polite`、Scrapy 節流 / 快取設定與除錯表）
- [X] 批次 7：`deep-learning/`（依 Phase 5 清單補新筆記）（全 18 篇改寫 + 新增 8 篇：`fundamentals/regularization-and-normalization.md`（dropout、weight decay / AdamW、BatchNorm vs LayerNorm、生醫 augmentation）、`training-workflows/pytorch-training-loop.md`（Dataset / DataLoader、完整 train / eval 模板、torchmetrics、scheduler、early stopping、病人 / 同源序列 / 染色體切分、可重現性）、`computer-vision/u-net-segmentation.md`（Dice loss、nnU-Net / Cellpose / StarDist / MONAI）、新模組 `representation-learning/`（`autoencoders-and-vae.md`、`graph-neural-networks.md`）與 `bio-applications/`（`sequence-and-protein-models.md`：one-hot CNN、Enformer、DNA LM、ESM 零樣本變異分數、AlphaFold pLDDT / PAE、同源洩漏；`single-cell-deep-learning.md`：scVI / scANVI、整合評估、單細胞基礎模型的限制）；Transformer 補 Q/K/V、multi-head、位置編碼 / RoPE、encoder vs decoder、長序列；Keras 筆記縮成 PyTorch ↔ Keras 對照表；新增 5 張圖（激活函數與導數、學習率、初始化與深度、early stopping、位置編碼 / causal attention）；修 `CrossEntropyLoss` 前接 `Softmax`、整數輸入 `nn.Linear`、`with no_grad` 內重設 `nn.Parameter`、未定義的 `custom_layer`、`##Kaiming` 標題、Hinge loss 說法、`KLDivLoss` 輸入、`torch.cuda.amp` → `torch.amp`、`pretrained=True` → `weights=`、`ToTensor` → v2、`torch.load` 的 `weights_only` 預設（≥ 2.6）、`"1" in name` 判斷層、凍結層 BN 仍更新、Keras 3 `input_shape`；移除課程來源字樣與 emoji）
- [X] 批次 8：`llm/`（評估、幻覺、成本、隱私；生資文獻探勘 / bio-LLM）（全 19 篇改寫 + 新增 `evaluation-and-hallucination.md`（評估集設計、題數與 Wilson CI、配對比較、指標選擇、LLM-as-judge 偏誤與校正、幻覺類型、引用 / 實體驗證、PMID 檢查程式）、`bio-and-medical-llm.md`（用途與可信度表、PubMed → 篩選 → 擷取 → 標準化 → 驗證流程、證據句驗證、生醫 encoder vs 通用 LLM、PHI / 基因資料隱私、常見錯誤）；LLMOps 補成本 / 延遲（模型路由、prompt caching、Batch API、自架）、版本鎖定、tracing 中的個資；API 改為 OpenAI v1 / Anthropic SDK 實際程式（多輪、structured output 用 pydantic、tool calling 迴圈、錯誤類別與重試、moderation、prompt injection、token 計算）；RAG 補 hybrid search（BM25）、reranking、父子 chunk、引用式 grounding、檢索 vs 生成分開評估、GraphRAG / 長 context 取捨；向量資料庫補 HNSW / IVF / PQ、FAISS 與 pgvector 範例、過濾時機、多租戶隔離；Hugging Face 補 BiomedBERT、tokenizer 截斷陷阱；fine-tuning 改用 `trl` `SFTTrainer` + LoRA、蒸餾、災難性遺忘；LangGraph 補 checkpointer、`recursion_limit`、`interrupt_before` 人工核准；foundations 補取樣參數、訓練階段（含推理模型）、tokenization 對基因名 / DNA 的影響；ChatGPT / custom GPT 等產品段落精簡成表格；新增 2 張圖（temperature / top-p、評估題數 vs CI 寬度））
- [X] 批次 9：`responsible-ai/`（HIPAA、EU AI Act 醫材、基因資料匿名化）（全 7 篇改寫；隱私與法規補 GDPR / HIPAA / 台灣個資法比較表、假名化 vs 匿名化、HIPAA Safe Harbor 18 類識別碼與 Expert Determination / Limited Data Set、基因資料再識別途徑（Y-STR 姓氏推論、系譜資料庫、彙總統計推論）、dbGaP / EGA 受控存取與 DUA、可信研究環境、聯邦式分析、NIST CSF 2.0；EU AI Act 補 MDR / IVDR 與高風險分類（Rule 11、notified body）、高風險義務、GPAI 下游責任、時程依 Digital Omnibus（Regulation (EU) 2026/1744）更新為附件 III 2027-12-02、附件 I 2028-08-02、罰則；資料偏誤補 GWAS / PRS 族群偏誤、EHR 偏誤（就醫選擇、MNAR、編碼、治療混淆）、site / batch effect、代理目標案例、子群評估程式與公平性準則不相容；匿名化補 k-anonymity pandas 實作、l-diversity / t-closeness、Laplace 機制、diffprivlib bounds、合成資料效用 / 隱私檢查、臨床文字 / DICOM 去識別、基因資料限制；AI 資安補 prompt injection、成員推論、訓練資料擷取、供應鏈（safetensors、`weights_only`）；Responsible AI 補生醫倫理四原則、同意模式（broad / dynamic）、FAIR 例子、Model Card / Datasheet；新增 1 張圖（差分隱私 ε 與雜訊））
- [X] 批次 10：`data-engineering/` + `data-communication/`（Spark 處理大型 omics（Glow / Hail））（全 25 篇改寫 + 新增 `data-engineering/spark-for-genomics.md`（Glow 讀 VCF、拆多等位 / 標準化、call stats / HWE、0-based `start` 陷阱；Hail MatrixTable、sample / variant QC、LD pruning + PCA、`linear_regression_rows` 截距、logistic / Firth、陷阱表）；資料工程補檔案格式表（Parquet / Arrow / h5ad / Zarr / VCF / CRAM）、Iceberg / Hudi、生資擷取問題（Excel 基因名、checksum、bgzip + tabix、參考基因體版本）、全量 / 增量 / CDC、冪等與重跑、Nextflow / Snakemake 對照、patient–sample–run 建模例子與 Ensembl ID 當 key、pandera 與 GX Core 1.x 實作、metadata ↔ 計數矩陣一致性檢查、可合併部分結果表（平均、Welford、XᵀX、近似分位數 / HyperLogLog）與 Polars / DuckDB / R（bigmemory、iotools、arrow）範例、Spark 執行架構 / shuffle / broadcast / pandas UDF / AQE / 效能表、MLlib Pipeline 與時間切分、Kafka consumer group / offset / 傳遞語意、Structured Streaming 範例、Databricks liquid clustering / `VACUUM` 與 time travel、BigQuery `LIMIT` 不省掃描量 / `--dry_run`、Snowflake auto-suspend；修 dbt `source('raw','orders')` 與定義不符、snapshot 缺 `unique_key` / `strategy`、`tests:` → `data_tests:`、`MERGE` 只有 `WHEN MATCHED`（新 key 不會插入）、`OPTIMIZE WHERE` 只能用 partition 欄、Redshift 源自 PostgreSQL 8.0.2（非 9）、Spark Streaming（DStream）→ Structured Streaming、Kinesis Firehose → Amazon Data Firehose 與兩種 Lambda 事件格式（`Records` vs `records` + 回傳格式）、Elasticsearch → OpenSearch、DLT → Lakeflow Declarative Pipelines、Kafka 4.0 移除 ZooKeeper、sparklyr `ml_predict` 後 `pull()` 再按順序合併會錯位、DAX `SUM(Sales)` 缺欄位 / `ADDCOLUMNS` 欄位引用、`FILTER(fact, RELATED())` 改直接篩選、M 沒有 `^` 運算子、RLS 不限制 workspace 作者；data-communication 補生醫例子的分析問題、可信度（不確定性、多重檢定、關聯 vs 因果）、可重現性表、實驗室 QC dashboard 與工具表、Power BI vs Tableau 比較、Composite / Direct Lake、Tableau relationship 與 LOD；改寫外部連入 anchor（airflow、aws-services-overview、boto3））
- [X] 批次 11：`applied-domains/` + `network-analysis/` + `image-analysis/` + `understanding-data-science.md`（全 19 篇改寫；network-analysis 補 closeness / PageRank、相似度要先轉距離再算最短路徑、研究偏差造成的 hub、G(n, m) 與保留 degree 的隨機基準（經驗 p 值）、Louvain / Leiden / label propagation 比較與 resolution、二分 projection 加權（Jaccard）與假 hub、時間切片程式，案例補 STRING API、WGCNA（`blockwiseModules`、樣本數、批次）、scanpy kNN + Leiden 參數表；image-analysis 補影像 dtype / `img_as_float`、rolling ball 背景校正、閾值方法比較、distance transform + watershed 細胞核分割與 `regionprops_table`、像素大小 / 邊緣物件 / 生物重複、SimpleITK 與 nibabel 讀取（`(z,y,x)` vs `(x,y,z)` 軸順序陷阱、DICOM 依位置排序）、CT HU vs MRI 任意單位、opening / closing、體積換算與射出分率、SimpleITK registration（mutual information）、標籤用最近鄰內插；applied-domains 補生醫對應欄、FBA 線性規劃例子（多重最佳解）、Hill 曲線 `curve_fit`、PuLP 設施選址模型、Ledoit-Wolf 收縮與最大 Sharpe / 最小變異最佳化、風險貢獻、VaR / CVaR 三種算法程式、Kupiec 回測、GBM 模擬程式、RSI / 均線訊號與交易成本、deflated Sharpe 與多重比較、信用風險時間切分 + isotonic 校準 + 策略表程式、reject inference、壽命表 EPV 程式（年金、保證期、定期 / 遞延壽險、保費）、DCE / conditional logit / 願付價格、Poisson GLM 處理 0 銷量、uplift 與 geo experiment；新增 5 張圖（degree vs betweenness、空手道網路 vs 隨機圖基準、細胞核 watershed 流程、LP 頂點與非凸局部最小值、效率前緣 + 厚尾 VaR / CVaR）；修 `milp` 未給 `integrality` 時其實只解 LP、`NonlinearConstraint` 範例其實是線性的、LP 用 `minimize` 求解、PuLP 4 API 變更（`LpVariable.dicts` / `PULP_CBC_CMD` / `LpStatus` 移除、不再內建 CBC → `add_variable_dict` + `HiGHS`）、bupaR `resource =` → `resource_id =`、append 後欄名 `processing_time_case` 與 `throughput_time` 不符、`imageio.volread` / `meta["sampling"]` → SimpleITK / `imageio.v2`、`remove_small_objects(min_size=)` 已棄用（改以 regionprops 面積過濾）、`mean_intensity` → `intensity_mean`、`find_contours` 在二值圖用 0.5、`corner_harris` 後需 `corner_peaks`、financial `np.npv` 已移除 → `numpy_financial`（與 Excel `NPV()` 的 t = 0 差異）、壽命表 LaTeX `\|` → `\mid`、混入的非中文字元「बदल」、交易回測訊號需 `shift(1)` 避免 look-ahead；understanding-data-science 改寫為中文並補生醫資料來源與受控存取資料）
- [ ] 批次 12（選做）：新增筆記：AnnData / scanpy / h5ad、scipy.sparse、ggplot2（填補缺口）
- [ ] 批次 13（選做）：`biology/` RNA-seq、DESeq2、QTL、ChIP-seq 筆記補連到 statistics（multiple-testing、glm-count-models、mixed-effects、confounding-bias、pca）（跨領域連結）

## 驗證

- 每階段：`uv run --no-project .claude/skills/rewrite-notes/check_links.py data-science` 與 `... check_links.py .` 都只輸出 `Checked N files`
- 每階段 `git status` 確認搬移都是 rename（`git mv`），刪除都是預期中的檔
- Phase 6 後抽查 `data-science/README.md` 每個連結都能點開，且沒有任何 README 指向不存在的筆記
- 預期結果：筆記數由 ~490 降到約 330–350，每個主題只有一個主檔

## 附錄：data-science 外部的連入（搬移時必修）

| 來源 | 指向 |
| --- | --- |
| `computing/cloud/gcp-fundamentals.md` | `data-engineering/spark.md#spark-sql` |
| `computing/cloud/boto3-for-aws-services.md`、`aws-services-overview.md` | `data-engineering/streaming.md#aws-streaming-with-kinesis-and-lambda`、`python-foundations/api-http.md`、`machine-learning/production/mlops-overview.md` |
| `computing/cloud/azure-services-overview.md` | `data-engineering/databricks.md` |
| `computing/cloud/azure-management-and-governance.md` | `data-engineering/governance.md` |
| `computing/cloud/azure-fundamentals.md` | `machine-learning/production/mlops-overview.md` |
| `computing/workflow-engines/airflow/README.md` | `data-engineering/processing-and-pipelines.md`（含 `#etl-and-pipelines`） |
| `computing/devops/devops-fundamentals.md` | `machine-learning/production/deployment-and-monitoring.md` |
| `README.md`（notebook 根） | 只連 `data-science/README.md` |
