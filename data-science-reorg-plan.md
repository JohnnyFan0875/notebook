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
- [ ] `data-engineering/customer-churn-analysis-in-power-bi.md`、`hr-analytics-in-power-bi.md`、`financial-analysis-in-power-bi.md`、`trend-analysis-in-power-bi.md`（4 篇 case studies）
- [ ] `data-engineering/microsoft-fabric-fundamentals.md`、`microsoft-fabric-environment-design-and-deployment.md`
- [ ] `data-engineering/power-bi-service-for-end-users.md`
- [ ] `data-engineering/python-in-power-bi.md`（內容已被 `machine-learning/preprocessing/imputation.md` 涵蓋）
- [ ] `data-communication/sigma-overview-and-workflow.md`、`datalab-workflow.md`
- [ ] `data-communication/data-fluency.md`、`data-driven-decision-making.md`（給商業分析師的素養內容）

**ai-strategy-and-governance**
- [ ] `ai-strategy.md`、`monetizing-ai.md`、`digital-transformation.md`、`data-strategy.md`、`data-management.md`、`understanding-artificial-intelligence.md`

**llm**
- [ ] `llm/integration/microsoft-copilot-productivity-workflows.md`、`llm-business-workflows.md`
- [ ] `llm/prompting/gpt-tools-and-practical-use.md`

**databases**
- [ ] `sql-server-triggers.md`、`sql-server-functions-and-stored-procedures.md`
- [ ] `oracle-sql-patterns.md`（救：NVL / TO_DATE → 後面的 dialect 對照表）
- [ ] `mysql.md`（救：`LOAD DATA` / 匯出指令）
- [ ] `business-analysis-in-sql.md`（救：ROLLUP / CUBE / GROUPING SETS、EXISTS / correlated subquery → `sql-reporting-patterns.md`）

**r-foundations / EDA / 其他**
- [ ] `r-foundations/social-media-analysis.md`（rtweet 依賴已停用的 Twitter API；LDA / sentiment 與 `text-analysis.md` 重複）
- [ ] `r-foundations/sas-to-r-mental-model.md`（救：「一切皆物件 / model object / broom」→ `tidyverse-workflow.md`）
- [ ] `data-manipulation-and-eda/cohort-analysis.md`（商業 retention；連結改指向 `statistics/survival-analysis/kaplan-meier.md`）
- [ ] `finance/corporate-finance/`（整個資料夾 9 篇）
- [ ] 跑連結檢查 → 修掉所有指向已刪檔的連結（README 表格列直接刪掉該列）→ commit

## Phase 2：跨資料夾搬移

- [ ] `data-engineering/scala-foundations.md` → `computing/programming-languages/scala-fundamentals.md`（與 java / julia 同層），更新該 README
- [ ] `python-foundations/web-scraping.md` → `web-scraping/scrapy-and-selectors.md`
- [ ] `r-foundations/web-scraping-in-r.md` → `web-scraping/rvest.md`
- [ ] `python-foundations/mongodb.md` → `databases/mongodb-pymongo.md`
- [ ] `python-foundations/database-access-sqlalchemy.md` → `databases/python-sqlalchemy.md`
- [ ] `r-foundations/modeling-with-tidymodels.md` → `machine-learning/packages/tidymodels/README.md`（與 scikit-learn、statsmodels 並列）
- [ ] `data-manipulation-and-eda/visualization/dashboard-design.md` → `data-communication/dashboard-design.md`
- [ ] `deep-learning/computer-vision/biomedical-image-analysis.md`、`image-processing-with-scikit-image.md` → 新資料夾 `data-science/image-analysis/`（古典影像處理，非 DL）；從 `deep-learning/computer-vision/README.md` 與 `biology/medical-imaging/README.md` 連過去
- [ ] `data-engineering/data-versioning-and-dvc.md` → `machine-learning/production/dvc.md`（與 mlflow 並列）
- [ ] `ai-strategy-and-governance/data-warehousing.md` → 併入 `data-engineering/dimensional-modeling-and-star-schema.md`（Phase 4 一起做也可）
- [ ] 建 `applied-domains/`（README），把 `finance/`、`marketing-analytics/`、`operations-research/`、`process-analytics/` 搬進去（`git mv` 整個資料夾，內容合併在 Phase 5）
- [ ] `ai-strategy-and-governance/` 改名 → `responsible-ai/`
- [ ] 更新 `data-science/README.md` 章節地圖與路線圖 → 連結檢查 → commit

## Phase 3：基礎層整併（Python / R / EDA / web-scraping / databases）

**python-foundations**
- [ ] datetime：`pandas/datetime.md` + `pandas/dtypes-strings.md` 的 datetime 段 + `data-type-transformation.md` 的 String↔Datetime → 統一到 `python-foundations/datetime.md`（stdlib + pandas 兩節）
- [ ] importing-data：`pandas/creating-data.md` 的 I/O 半部 + `data-type-transformation.md` → 併入 `importing-data.md`；HTTP 段改連 `api-http.md`
- [ ] 文字處理：`regex.md` + `string-matching.md` → `text-cleaning-and-regex.md`；連 `computing/operating-system/regex-wildcard.md`
- [ ] scripting：`argparse.md`、`if-name-main.md`、`subprocess.md`、`config-files.md`、`file-io.md`、`python-snippets.md` → `scripting-and-cli.md`
- [ ] 錯誤處理：`assert.md` + `try-except.md` → `errors-and-assertions.md`
- [ ] 效能：建 `performance-and-scaling/`：`efficient-python.md`、`parallel.md`（`multiprocessing.md` + `dask.md`）、`polars.md`；`pandas/performance.md` + `pandas/row-operations.md` 合成 `pandas/performance.md`
- [ ] numpy 8 → 4：`array-basics`（properties + creation + indexing）、`vectorization-and-reshape`（operations + reshape-concatenate）、`random-and-statistics`、`linear-algebra`；`operations.md` 裡 DataFrame boolean indexing 移去 pandas
- [ ] pandas 21 → ~11：`selection`（indexing-slicing + filtering）、`modifying`（updating + adding-removing）、`ordering-binning-sampling`（sorting + binning + sampling-duplicates）、`dtypes-categorical-strings`（dtypes-strings + categorical）；`index-multiindex`、`groupby`、`reshape-merge`、`statistics`、`missing-data`、`performance` 保留
- [ ] `pandas/time-series-visualization.md`：ACF / PACF / decomposition 段併入 `statistics/time-series-analysis/`（autocorrelation、decomposition），繪圖段併入 `pandas/visualization.md`
- [ ] `pandas/visualization.md` → 搬到 `data-manipulation-and-eda/visualization/pandas-plotting.md`
- [ ] `python-packages.md`：標記過時的 setup.py / MANIFEST.in，改寫階段換成 pyproject + uv（並連 `computing/containers-and-env/`）

**r-foundations**
- [ ] `vectors.md` + `data-frames.md` + `lists.md` → `data-structures.md`
- [ ] `functional-programming-with-purrr.md` + `-advanced.md` + `apply-family.md` → `functional-programming.md`（for vs apply vs purrr）
- [ ] `defensive-programming.md` 與 `functions.md` 的 Input Validation / Errors 段去重（併入 functions）
- [ ] `statistical-functions.md`：刪 regression 段（改連 `explanatory-modeling-in-r.md`）
- [ ] `sampling-in-r.md` + `survey-data-analysis.md` → `statistics/inferential-statistics/survey-sampling.md`（bootstrap 重複段改連 `sampling-estimation.md`）
- [ ] `missing-data.md`（R）：刪 MCAR/MAR/MNAR 理論，只留 naniar 工具用法，連到 EDA 的 missing-data

**data-manipulation-and-eda**
- [ ] `data-profiling.md` 併入 `eda-workflow.md`（profiling 作為第一節）
- [ ] missing data 單一歸屬：機制理論只在 `data-manipulation-and-eda/missing-data.md`；`pandas/missing-data.md` 只留 pandas / missingno API；插補方法只在 `machine-learning/preprocessing/imputation.md`；刪 `matplotlib/advanced.md` 的 missingno 段
- [ ] `geospatial-data-in-python.md`：留在原處但 README 標為「選讀」
- [ ] matplotlib `line-plot.md` vs `advanced.md` 雙軸 / annotation 去重；seaborn `categorical` vs `distribution` 的 countplot vs histplot 去重

**web-scraping**
- [ ] 三篇（scrapy、bs4-selenium、rvest）共用的 CSS vs XPath、User-Agent、節流、合法性移到 `web-scraping/README.md`，各篇只留工具用法
- [ ] 記下待修 bug：`random.randint(5)`、Selenium 4 前的 `webdriver.Chrome(ChromeDriverManager().install())`、Scrapy `extract_first` → `.get()`

**databases**
- [ ] `postgresql-window-functions-and-pivoting.md` + `sql-server-window-functions.md` → `sql-window-functions.md`（通用）；PG crosstab 留一小節
- [ ] `postgresql-transactions-and-exception-handling.md` + `sql-server-transactions-and-error-handling.md` → `sql-transactions.md`（PG / T-SQL 對照欄）
- [ ] `postgresql-query-performance.md` + `sql-server-query-performance.md` → `sql-query-performance.md`（通用 + EXPLAIN / execution plan 子節）
- [ ] `sql-server-basics.md` + `sql-server-tsql-patterns.md` + `snowflake-sql-patterns.md` + Oracle 救下來的段落 → `sql-dialect-cheatsheet.md`（TOP / LIMIT、NVL / ISNULL / COALESCE、日期函式、FLATTEN 對照表）
- [ ] `postgresql.md` → 精簡成 `postgresql-psql-and-copy.md`（psql、`COPY` 匯入匯出）
- [ ] JOIN / NULL / aggregation 重複段只留在 `sql-query-foundations.md` 與 `sql-joins-and-set-operations.md`
- [ ] 連結檢查 → commit

## Phase 4：中間層整併（data-engineering / data-communication / responsible-ai / llm）

**data-engineering**
- [ ] `etl.md` 併入 `processing-and-pipelines.md`
- [ ] `ai-strategy` 的 `data-warehousing.md` 併入 `dimensional-modeling-and-star-schema.md`；`data-modeling-foundations.md` 的 1NF–3NF 改連 `databases/database-normalization.md`
- [ ] `databricks-foundations.md` + `databricks-data-management.md` + `databricks-sql.md` → `databricks.md`
- [ ] `spark-and-pyspark.md` + `spark-sql-in-pyspark.md` → `spark.md`；`sparklyr.md` 保留；`scalable-processing-and-out-of-core.md` 保留並連 `python-foundations/performance-and-scaling/`、`r-foundations/parallel-programming-in-r.md`
- [ ] `snowflake-foundations.md` + `bigquery-foundations.md` + `redshift-foundations.md` → `cloud-data-warehouses.md`（比較表為主）
- [ ] `streaming-and-kafka.md` + `aws-streaming-with-kinesis-and-lambda.md` → `streaming.md`
- [ ] `governance.md` + `responsible-ai/data-governance.md` → `data-engineering/governance.md`
- [ ] `responsible-ai/data-quality.md` + `data-quality-with-great-expectations.md` → `data-engineering/data-quality-checks.md`；連 `statistics/descriptive-statistics/data-quality.md`
- [ ] Power BI 剩下 8 篇 → `data-communication/bi-tools/`：`power-query.md`（data-connections + data-preparation + data-transformation）、`power-bi-modeling-and-dax.md`（overview + semantic-models + dax）、`power-bi-reports.md`（reports + report-design）
- [ ] tableau 3 篇 → `data-communication/bi-tools/tableau.md`

**data-communication**
- [ ] `communicating-data-insights.md` + `reports-and-presentations.md` → `communicating-results.md`（加可重現報告角度，連 `r-foundations/reporting-with-r-markdown.md`）
- [ ] 保留 `forming-analytical-questions.md`、`dashboard-design.md`、`bi-tools/`

**responsible-ai**（原 ai-strategy-and-governance）
- [ ] `ai-ethics.md` + `responsible-ai.md` + `data-ethics.md`（保留 FAIR）+ `responsible-ai-data-management.md` + `ai-governance.md` → `responsible-ai.md`
- [ ] `data-bias-in-ai.md` → `data-bias-and-representativeness.md`（改寫時補 GWAS ancestry bias、EHR selection bias）
- [ ] `data-privacy.md` + `understanding-gdpr.md` + `data-security.md` → `privacy-and-regulation.md`（改寫時補 HIPAA、de-identification、dbGaP 受控存取）
- [ ] `understanding-the-eu-ai-act.md` 保留（改寫時補醫療器材 high-risk、MDR / IVDR）
- [ ] `data-privacy-and-anonymization-in-python.md` → `anonymization-in-python.md`（改寫時補 k-anonymity 對基因型無效）
- [ ] `ai-security-and-risk-management.md` 保留，連 `machine-learning/production/deployment-and-monitoring.md`

**llm**
- [ ] foundations：`chatgpt-overview.md` + `generative-ai-overview.md` + `large-language-models.md` → `foundations/llm-foundations.md`（transformer 內部改連 deep-learning）
- [ ] prompting：`prompt-engineering.md` + `chatbot-prompt-design.md` + `chatgpt-customization-and-reusable-workflows.md` → `prompt-engineering.md`
- [ ] integration：`llm-application-patterns.md` + `llm-workflows-in-python.md`（API 部分）+ `openai-api-workflows.md` → `llm-api-patterns.md`；`managed-llm-platforms.md` 併入 `choosing-llm-providers-and-model-families.md`
- [ ] integration：`multimodal-models-with-hugging-face.md` + `multimodal-openai-workflows.md` → `multimodal.md`
- [ ] fine-tuning：`deep-learning/nlp-and-transformers/llm-fine-tuning.md` + `llm-workflows-in-python.md` 的 fine-tune / eval 段 → `llm/integration/fine-tuning.md`（prompt vs RAG vs fine-tune 決策 + LoRA / PEFT）
- [ ] operations：`llmops.md` + `operating-agent-systems.md` → `llmops.md`
- [ ] rag：`rag/README.md`（135 行完整筆記）內容抽成 `rag/rag-pipeline.md`，README 改回精簡索引
- [ ] 資料夾只剩 1 篇的子資料夾（foundations、prompting、operations）考慮攤平到 `llm/` 根目錄
- [ ] 連結檢查 → commit

## Phase 5：上層整併（statistics / ML / DL / applied-domains / network-analysis）

**statistics / machine-learning**（已改寫，只做小幅合併）
- [ ] `machine-learning/workflow/data-splitting-and-leakage.md` 拆入 `foundations/data-leakage.md`（概念）與 `preprocessing/train-test-split.md`（操作）後刪除
- [ ] `machine-learning/foundations/evaluation-mindset.md` 併入 `evaluation/README.md`
- [ ] `statistics/multivariate-analysis/multiple-regression.md`（prediction + Ridge / Lasso / p>n）併入 `machine-learning/foundations/high-dimensional-data.md` / `regularization.md`
- [ ] `statistics/multivariate-analysis/logistic-lda.md` 刪掉重複的 logistic 段，改名 `lda.md`
- [ ] `statistics/multivariate-analysis/clustering.md` 精簡成概觀 + validation / profiling，方法細節連到 ML clustering
- [ ] `machine-learning/workflow/kaggle-competition-workflow.md`：blending 段刪掉（連 `ensemble/stacking.md`），README 標「選讀」
- [ ] README 標「選讀」：`recommender-systems/`、`association-rules/`、`evaluation/gains-and-lift-curves.md`、`structural-equation-modeling-with-lavaan.md`
- [ ] 補交叉連結：`statsmodels/diagnostics` ↔ `assumptions-diagnostics`；`imputation` ↔ EDA missing-data；`descriptive-statistics/data-quality` ↔ `eda-workflow`；`sampling-estimation` ↔ `survey-sampling`；`regression-analysis` → `r-foundations/explanatory-modeling-in-r.md`；`workflow/pipeline-basic` → `packages/tidymodels`；production README → `dvc.md`

**deep-learning**（結構調整；內容補強留到改寫）
- [ ] `computer-vision/image-classification-workflow.md` 併入 `convolutional-neural-networks.md`
- [ ] `nlp-and-transformers/sequence-models-for-text.md` + `text-representations-and-embeddings.md` → `text-and-sequence-models.md`；連 `llm/rag/embeddings-and-semantic-search.md`、`r-foundations/text-analysis.md`
- [ ] `fundamentals/tensorflow-and-keras-basics.md` 標記改寫時縮成「Keras 對照」表
- [ ] 記下改寫時要新增：PyTorch 訓練迴圈（Dataset / DataLoader、optimizer、scheduler、early stopping、dropout / batchnorm）、attention 深入（Q/K/V、multi-head、positional encoding）、autoencoder / VAE、GNN、生資序列與蛋白模型（one-hot CNN、ESM、DNABERT / Enformer、AlphaFold 概念）、單細胞 DL（scVI）、U-Net 分割
- [ ] 記下待修：`torch.cuda.amp` → `torch.amp`；`backpropagation.md` code block 內 `#` 被當標題；`##Kaiming` 標題格式；殘留課程來源字樣與 emoji

**applied-domains**
- [ ] `finance/`：`portfolio-analysis.md` + `quantitative-risk-management.md` + `stock-price-simulation-and-volatility.md` → `portfolio-and-risk.md`；`trading-strategies-and-backtesting.md`、`credit-risk-modeling.md` 保留；`insurance-and-annuity-valuation.md` 保留（連 survival analysis）；`fundamental-financial-concepts.md` + `bond-valuation-and-interest-rate-risk.md` → `financial-concepts.md`；`financial-data-ingestion-and-cleaning.md` 只留金融特有段併入 `financial-concepts.md`；`autocorrelation.md` 併入 `statistics/time-series-analysis/autocorrelation.md` 的金融小節
- [ ] `marketing-analytics/` 3 篇 → `applied-domains/marketing-response-and-choice-models.md`（保留與 `ab-testing.md` 互連）
- [ ] `operations-research/` 2 篇 → `applied-domains/optimization.md`
- [ ] `process-analytics/` → `applied-domains/process-mining.md`（強調醫療流程 event log）
- [ ] `applied-domains/README.md` 寫成精簡索引

**network-analysis**
- [ ] 保留 4 篇；`network-analysis-case-studies.md` 刪掉重複的指標說明；記下改寫時補 PPI / 共表現網路範例
- [ ] 連結檢查（data-science + 全 notebook）→ commit

## Phase 6：頂層 README 與入口

- [ ] 重寫 `data-science/README.md`：新章節地圖、依讀者類型的建議路線（生資 / ML / 選讀的工程與 BI），移除已刪章節
- [ ] `understanding-data-science.md` 精簡（改寫階段處理文字）
- [ ] 全 notebook 連結檢查零錯誤 → commit → 合併回 master（使用者確認後）

## Phase 7：用 `/rewrite-notes` 分批改寫

每批 10–30 篇、一個子資料夾；每批完成跑連結檢查、commit 再做下一批。依「被引用越多越先做」排序：

| 批次 | 目標資料夾 | 備註 |
| --- | --- | --- |
| 1 | `python-foundations/`（不含 numpy / pandas） | 補 pyproject + uv、`default_rng`、scipy.stats 對照 |
| 2 | `python-foundations/numpy/` + `pandas/` | view vs copy、dtype、Parquet / HDF5 |
| 3 | `r-foundations/`（前半：資料結構、tidyverse、dplyr、tidyr、data.table、importing、datetime、missing） | 連 Bioconductor 筆記 |
| 4 | `r-foundations/`（後半：functional、OOP、效能、Rcpp、parallel、package、R Markdown、regex、text） | 補 renv、Quarto |
| 5 | `data-manipulation-and-eda/`（含 visualization/） | |
| 6 | `databases/` + `web-scraping/` | 修 web-scraping bug；考慮補 DuckDB / Parquet |
| 7 | `deep-learning/` | 依 Phase 5 清單補新筆記 |
| 8 | `llm/` | 評估、幻覺、成本、隱私；生資文獻探勘 / bio-LLM |
| 9 | `responsible-ai/` | HIPAA、EU AI Act 醫材、基因資料匿名化 |
| 10 | `data-engineering/` + `data-communication/` | Spark 處理大型 omics（Glow / Hail） |
| 11 | `applied-domains/` + `network-analysis/` + `image-analysis/` + `understanding-data-science.md` | |
| 12（選做） | 新增筆記：AnnData / scanpy / h5ad、scipy.sparse、ggplot2 | 填補缺口 |
| 13（選做） | `biology/` RNA-seq、DESeq2、QTL、ChIP-seq 筆記補連到 statistics（multiple-testing、glm-count-models、mixed-effects、confounding-bias、pca） | 跨領域連結 |

## 驗證

- 每階段：`uv run --no-project .claude/skills/rewrite-notes/check_links.py data-science` 與 `... check_links.py .` 都只輸出 `Checked N files`
- 每階段 `git status` 確認搬移都是 rename（`git mv`），刪除都是預期中的檔
- Phase 6 後抽查 `data-science/README.md` 每個連結都能點開，且沒有任何 README 指向不存在的筆記
- 預期結果：筆記數由 ~490 降到約 330–350，每個主題只有一個主檔

## 附錄：data-science 外部的連入（搬移時必修）

| 來源 | 指向 |
| --- | --- |
| `computing/cloud/gcp-fundamentals.md` | `data-engineering/spark-sql-in-pyspark.md` |
| `computing/cloud/boto3-for-aws-services.md`、`aws-services-overview.md` | `data-engineering/aws-streaming-with-kinesis-and-lambda.md`、`python-foundations/api-http.md`、`machine-learning/production/mlops-overview.md` |
| `computing/cloud/azure-services-overview.md` | `data-engineering/databricks-foundations.md` |
| `computing/cloud/azure-management-and-governance.md` | `data-engineering/governance.md` |
| `computing/cloud/azure-fundamentals.md` | `machine-learning/production/mlops-overview.md` |
| `computing/workflow-engines/airflow/README.md` | `data-engineering/processing-and-pipelines.md`、`etl.md` |
| `computing/devops/devops-fundamentals.md` | `machine-learning/production/deployment-and-monitoring.md` |
| `README.md`（notebook 根） | 只連 `data-science/README.md` |
