[Computing](../README.md) › [DevOps](README.md) › GitHub Actions

# GitHub Actions

GitHub Actions 是 GitHub 內建的 CI/CD：在 push、PR、排程等事件發生時，自動在 GitHub 提供的虛擬機（runner）上跑測試、lint、建置容器映像檔、部署文件。設定檔是 repo 中 `.github/workflows/*.yml`。CI/CD 的觀念見 [DevOps 基礎](devops-fundamentals.md)。

## 結構

```text
workflow（一個 .yml 檔）
├── on：觸發條件（push、pull_request、schedule…）
└── jobs：可平行執行的工作
    └── job：在一台 runner 上執行（runs-on）
        └── steps：依序執行
            ├── uses：使用現成的 action（actions/checkout）
            └── run：執行 shell 指令
```

| 名詞 | 意義 |
| --- | --- |
| Workflow | 一個自動化流程，一個 YAML 檔 |
| Event / trigger | 觸發 workflow 的事件 |
| Job | 一組在同一台 runner 上執行的 steps；不同 job 預設平行，可用 `needs` 指定順序 |
| Step | 一個指令或一個 action |
| Action | 可重用的步驟，來自 Marketplace 或自己的 repo |
| Runner | 執行 job 的機器：GitHub 託管（`ubuntu-latest`、`windows-latest`、`macos-latest`）或自架 |
| Secret | 加密的機密（API token、雲端憑證），以 `${{ secrets.NAME }}` 使用 |
| Artifact | job 產出的檔案，可下載或傳給其他 job |

## 範例：Python 專案測試

```yaml
# .github/workflows/tests.yml
name: tests

on:
  push:
    branches: [main]
  pull_request:                         # 每個 PR 都跑；搭配分支保護「必須通過」

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false                  # 一個組合失敗，其他組合仍繼續跑
      matrix:                           # 矩陣：每個組合各跑一次 job（這裡是 2 × 3 = 6 個）
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4                     # 取得 repo 程式碼
      - uses: astral-sh/setup-uv@v6                   # 安裝 uv（含快取）
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync --locked                         # 依 uv.lock 安裝依賴
      - run: uv run ruff check .                      # lint
      - run: uv run pytest --cov=mypkg                # 測試 + 覆蓋率
```

> action 的版本（`@v4`、`@v6`）以各 action 的 README 為準。需要更嚴格的供應鏈安全時，把版本固定到 commit SHA。

pytest 的寫法見 [測試](../../data-science/python-foundations/testing.md)；套件管理見 [uv](../../data-science/python-foundations/python-packages.md)。

## 觸發條件

| `on:` | 何時執行 |
| --- | --- |
| `push`（可加 `branches`、`paths`、`tags`） | 推送時；`paths: ["src/**"]` 只在相關檔案變更時跑 |
| `pull_request` | PR 開啟或更新時 |
| `schedule: - cron: "0 2 * * 1"` | 定時（UTC），例如每週一檢查外部資料或依賴是否壞掉 |
| `workflow_dispatch` | 在網頁上手動按按鈕執行，可帶輸入參數 |
| `release` | 發布 release 時，例如建置並推送容器映像檔 |

## 常用功能

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make report
      - uses: actions/upload-artifact@v4        # 保存產出（報告、圖表、測試結果）
        with:
          name: report
          path: results/report.html

  deploy:
    needs: build                                # 等 build 成功才執行
    if: github.ref == 'refs/heads/main'         # 只在 main 分支
    runs-on: ubuntu-latest
    environment: production                     # 可設定需要人工核准
    steps:
      - run: ./deploy.sh
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}   # 機密從 repo / environment 設定中取得，log 中會被遮蔽
```

| 功能 | 用途 |
| --- | --- |
| `needs` | job 之間的順序與依賴 |
| `if` | 條件執行 |
| 快取（`actions/cache`，或 setup-* action 內建） | 依 lock 檔快取套件，加速 |
| `upload-artifact` / `download-artifact` | 保存產出、在 job 之間傳遞 |
| `services` | 在 job 旁啟動資料庫等容器（整合測試） |
| `environment` | 部署環境的機密與保護規則（人工核准） |
| `concurrency` | 同一分支新的執行取消舊的 |
| reusable workflow | 把共用流程寫一次，多個 repo 呼叫 |

## 資料與生資專案的常見用途

| 用途 | 做法 |
| --- | --- |
| 分析套件的單元測試 | 上面的 Python 範例；R 套件用 `r-lib/actions` |
| pipeline 煙霧測試 | 用極小的測試資料跑完整 pipeline（nf-core：`nextflow run . -profile test,docker`；Snakemake：`snakemake -n` 乾跑 + 小資料實跑） |
| 建置並推送容器映像檔 | `docker/build-push-action` 推到 `ghcr.io`，給 pipeline 使用 |
| 文件與報告網站 | 建置 MkDocs / Quarto，部署到 GitHub Pages |
| 筆記連結檢查 | 每次 push 跑連結檢查腳本 |
| 依賴更新 | Dependabot 開 PR，CI 驗證後再合併 |

## 注意事項

| 項目 | 說明 |
| --- | --- |
| 計費 | 公開 repo 的標準 runner 免費；私有 repo 有每月免費分鐘數，超過計費（macOS / Windows 分鐘數倍率較高） |
| 機密 | 不要寫進 YAML 或印出；來自 fork 的 PR 預設拿不到 secrets |
| 雲端憑證 | 優先用 OIDC 讓 workflow 臨時取得雲端權限，不存長期金鑰 |
| 大型資料 | runner 磁碟與記憶體有限，CI 只放小型測試資料；真正的分析在 HPC / 雲端跑 |
| 本機除錯 | `act` 可在本機模擬執行 workflow |
| 失敗時 | 在 Actions 頁面看各 step 的 log；可「Re-run failed jobs」 |
