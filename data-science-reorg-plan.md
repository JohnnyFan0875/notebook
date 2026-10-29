# Data Science 重整計畫與 Checklist

## 現況（2026-10-29 檢查）

原計畫 Phase 0–7（刪除 → 搬移 → 整併 → README → `/rewrite-notes` 批次 1–13）已全部完成並合併回 master，已完成項目已自本檔移除（細節見 git log：`Restructure data-science: phase *`、`Rewrite data-science: phase 7 batch *`）。

| 檢查項目 | 結果 |
| --- | --- |
| `check_links.py data-science` / `check_links.py .` | 皆只輸出 `Checked N files`（397 / 726） |
| 原計畫要刪 / 併的檔案與資料夾 | 皆已不存在 |
| 檔頭「待改寫」「待修」註記 | 已全部清除 |
| 舊 API（`torch.cuda.amp`、`pretrained=True`、`extract_first`、`find_element_by_*`、`np.npv`、`select([...])`、`np.random.seed`） | 只出現在「舊 → 新」對照表或註解中，非實際用法 |
| 孤兒筆記（沒有任何檔案連入） | 無 |
| 筆記數 | 393 篇（原預估 330–350；差額主要是 Phase 7 新增的筆記，屬預期） |

以下是仍待處理的項目。

## 通用規則

- 改寫一律用 `/rewrite-notes` 的風格（麵包屑、`# 中文標題 (English Title)`、表格優先、精簡程式碼）。
- 改 H1 / 小節標題前先 `Grep` 整個 notebook 找 `#anchor` 連入，改完同步修正。
- 每批完成跑連結檢查，零錯誤才 commit：
  ```bash
  uv run --no-project ".claude/skills/rewrite-notes/check_links.py" data-science
  uv run --no-project ".claude/skills/rewrite-notes/check_links.py" .
  ```

Phase 8（補改寫 `dvc.md`、`tidymodels/README.md`、`survey-sampling.md`）與 Phase 9（renv 索引、5 個 H1 中英並列）已完成，見 git log。

## Phase 10：程式碼實跑驗證（需 R 環境）

本機目前沒有 R（`Rscript` 不存在、Docker engine 未啟動），批次 12 的 ggplot2 筆記註明「未執行」。可用 Docker（`rocker/tidyverse`）或 conda-forge `r-base` 免管理員權限安裝。

- [ ] 裝 R（或用有 R 的機器 / 容器）後實跑 `data-manipulation-and-eda/visualization/ggplot2.md` 全部範例，確認 `after_stat()`、`linewidth`、patchwork / ggrepel 寫法可執行
- [ ] 順便抽查 `r-foundations/` 批次 3–4 新補的程式（`join_by()` 區間 join、data.table `foverlaps`、purrr 1.0 `list_rbind` 等）與 Phase 8 改寫後的 `survey-sampling.md`、`tidymodels/README.md`（兩篇的 R 程式碼依官方文件整理、未實跑；`survey-sampling.md` 的 Python `svy` 段已在 svy 0.36 驗證）
- [ ] 修正後連結檢查 → commit

## 完成後

- [ ] 全部項目勾完後，刪除本檔（`git rm data-science-reorg-plan.md`），重整歷程留在 git log 即可

## 附錄：data-science 外部的連入（改標題 / 搬檔時必查）

| 來源 | 指向 |
| --- | --- |
| `computing/cloud/gcp-fundamentals.md` | `data-engineering/spark.md#spark-sql` |
| `computing/cloud/boto3-for-aws-services.md`、`aws-services-overview.md` | `data-engineering/streaming.md`、`python-foundations/api-http.md`、`machine-learning/production/mlops-overview.md` |
| `computing/cloud/azure-services-overview.md` | `data-engineering/databricks.md` |
| `computing/cloud/azure-management-and-governance.md` | `data-engineering/governance.md` |
| `computing/cloud/azure-fundamentals.md` | `machine-learning/production/mlops-overview.md` |
| `computing/workflow-engines/airflow/README.md` | `data-engineering/processing-and-pipelines.md` |
| `computing/devops/devops-fundamentals.md` | `machine-learning/production/deployment-and-monitoring.md` |
| `biology/`（RNA-seq、DESeq2、QTL、ChIP-seq） | `statistics/` 的 multiple-testing、glm-count-models、mixed-effects、confounding-bias、pca（批次 13 建立的雙向連結） |
| `README.md`（notebook 根） | 只連 `data-science/README.md` |
