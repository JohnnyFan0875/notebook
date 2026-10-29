[Machine Learning](../README.md) › [上線與維運](README.md) › DVC

# 資料版本控制與 DVC (Data Versioning with DVC)

同一份程式碼，換了資料版本或參數就可能得到不同結果。DVC (Data Version Control) 把大型資料、模型與 pipeline 的 metadata 交給 Git 管理、實際檔案放在 cache / remote storage，讓「這次結果用了哪份資料、哪組參數、哪版程式」都能回溯與重跑。

## 為什麼需要資料版本

| 要回答的問題 | 只有 Git 時 | 加上 DVC |
| --- | --- | --- |
| 這次模型 / 報表用了哪份資料？ | 大檔不能進 Git，只能靠檔名或口頭約定 | `.dvc` / `dvc.lock` 記錄內容 hash，跟著 commit 走 |
| 為什麼這次結果和上週不同？ | 只能 diff 程式碼 | `dvc params diff`、`dvc metrics diff` 同時比較參數與指標 |
| 能把當時的結果重跑出來嗎？ | 需要手動找回資料 | `git checkout <rev>` + `dvc checkout` / `dvc pull` + `dvc repro` |
| 這個 artifact 是哪個流程產生的？ | 看 notebook 執行順序（常不可靠） | `dvc.yaml` 定義 stage 的 deps / outs，`dvc dag` 畫依賴圖 |

可重現需要同時鎖住五樣東西：**資料、參數、程式、pipeline 步驟、輸出指標**；任一個漂移，結果就可能不同。`requirements.txt` 或 Git commit 只鎖住其中一部分（執行環境另見 [容器與環境](../../../computing/containers-and-env/README.md)）。

## Git、DVC 的分工

| | Git | DVC |
| --- | --- | --- |
| 追蹤對象 | 程式碼、`params.yaml`、`dvc.yaml`、`dvc.lock`、`*.dvc` | 資料、模型、中間 artifacts（內容存在 cache 與 remote） |
| 存放位置 | Git repo / GitHub | `.dvc/cache`（本機）+ remote（S3、GCS、Azure、SSH、本機共享目錄…） |
| 識別方式 | commit hash | 檔案內容 hash（相同內容只存一次） |
| 同步指令 | `git push` / `git pull` | `dvc push` / `dvc pull` |

> Git 與 DVC 是互補，不是替代：commit 只存 DVC 的「指標檔」，檔案本體在 remote。只 `git push` 沒有 `dvc push`，別人 clone 下來會拿不到資料。

## 和其他工具比較

| 工具 | 擅長 | 不擅長 / 限制 | 何時用 |
| --- | --- | --- | --- |
| DVC | 資料與 pipeline 版本跟 Git commit 綁在一起；`dvc repro` 只重跑變動的 stage | 實驗 UI 較陽春；不管模型部署 | 資料檔大、需要可重跑 pipeline、團隊共用資料版本 |
| [MLflow](mlflow.md) artifacts | 實驗追蹤 UI、模型打包與 Registry（alias、部署） | artifacts 綁在 run 上，不描述資料怎麼產生、不跟 Git 版本對齊 | 比較大量 run、管理上線模型版本 |
| Git LFS | 設定簡單，對 Git 使用者透明 | 沒有 pipeline / 指標概念；GitHub LFS 有容量與流量額度 | 少量中型二進位檔（圖片、小模型） |
| 工作流引擎（[Nextflow](../../../computing/workflow-engines/nextflow/README.md)、Snakemake） | 大規模平行、HPC / 雲端排程、容器整合、生資社群 pipeline（nf-core） | 不負責資料版本（輸入檔改了只會重跑，不會記錄歷史） | 生資前處理（比對、定量）等重度計算 |

常見組合：工作流引擎跑上游定序資料處理 → DVC 版本化下游的 count matrix、特徵表與模型 → MLflow 記錄每次訓練的指標並註冊模型。

## 基本流程

```bash
# 1. 初始化（在 Git repo 內）
git init && dvc init                      # 產生 .dvc/config、.dvc/.gitignore、.dvcignore
git commit -m "Initialize DVC"

# 2. 追蹤資料：產生 data/raw.dvc（含 hash），並把 data/raw 加進 .gitignore
dvc add data/raw
git add data/raw.dvc data/.gitignore
git commit -m "Track raw data"

# 3. 設定 remote 並上傳
dvc remote add -d storage s3://my-bucket/dvc-store
git commit .dvc/config -m "Add DVC remote"
dvc push

# 4. 別人或另一台機器：取得程式與資料
git clone <repo> && cd <repo>
dvc pull

# 5. 回到舊版本
git checkout <commit> data/raw.dvc
dvc checkout data/raw.dvc                 # 工作目錄的資料換成該版本
```

| 檔案 | 是否進 Git | 作用 |
| --- | --- | --- |
| `.dvc/config` | 是 | remote、cache 設定（帳密放 `.dvc/config.local`，不進 Git） |
| `.dvcignore` | 是 | 語法同 `.gitignore`；排除暫存檔，資料夾大時可減少掃描時間 |
| `*.dvc` | 是 | 單一資料檔 / 資料夾的 hash 與大小 |
| `dvc.yaml` / `dvc.lock` | 是 | pipeline 定義 / 每個 stage 實際用到的 deps 與 outs 的 hash |
| `.dvc/cache/` | 否 | 檔案內容（依 hash 存放） |

## Pipeline：`dvc.yaml` + `params.yaml`

參數集中在 `params.yaml`，作為前處理、訓練、評估共用的**單一來源**；`dvc.yaml` 把 workflow 從隱性的 notebook 執行順序變成顯性的依賴圖。

```yaml
# params.yaml
prepare:
  min_counts: 10
train:
  seed: 42
  n_estimators: 300
  max_depth: 8
```

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python src/prepare.py
    deps: [src/prepare.py, data/raw]
    params: [prepare.min_counts]           # 預設從 params.yaml 讀
    outs: [data/processed]
  train:
    cmd: python src/train.py
    deps: [src/train.py, data/processed]
    params: [train]                        # 整個 train 區塊
    outs: [models/model.pkl]
  evaluate:
    cmd: python src/evaluate.py
    deps: [src/evaluate.py, models/model.pkl, data/processed]
    metrics:
      - metrics.json:
          cache: false                     # 小檔直接進 Git，方便 diff
    plots:
      - plots/roc.csv:
          x: fpr
          y: tpr
```

| 欄位 | 意義 |
| --- | --- |
| `cmd` | 執行指令（腳本自己讀 `params.yaml`） |
| `deps` | 輸入檔或程式；任一 hash 改變，此 stage 與下游都要重跑 |
| `params` | 參數依賴；只有列出的 key 改變才會觸發重跑 |
| `outs` | 輸出，自動進 cache、加進 `.gitignore` |
| `metrics` / `plots` | 要追蹤與比較的結果檔（JSON / YAML / CSV） |

```bash
dvc repro                      # 依 dvc.yaml 重跑「有變動」的 stage，更新 dvc.lock
dvc dag                        # 顯示 stage 依賴圖
dvc status                     # 哪些 stage 過期
git add dvc.lock metrics.json && git commit -m "Retrain" && dvc push
```

> DVC 救不了混亂的原型碼：先把 notebook 拆成可測試的模組與 entry-point 腳本（`src/prepare.py` 等），讓 config、code、data、outputs 邊界清楚，再接上 `dvc.yaml`。專案結構見 [軟體工程實務](../../python-foundations/software-engineering.md)。

## 實驗與比較

```bash
# 不必改 params.yaml 就能跑不同設定；每個實驗都被記錄
dvc exp run -S train.max_depth=4
dvc exp run -S train.max_depth=12 -S train.n_estimators=500

dvc exp show                          # 表格：每個實驗的 params 與 metrics
dvc exp apply <exp-name>              # 把選中的實驗套用到工作目錄
git commit -am "Use max_depth=12"     # 再正式 commit
dvc exp push origin <exp-name>        # 或把實驗本身分享到 Git remote

dvc params diff main                  # 和 main 比參數
dvc metrics diff main                 # 和 main 比指標
dvc plots diff main                   # 產生比較圖（HTML）
```

這讓「模型變好了」變成可審計的比較：是資料版本還是參數造成改善？提升的是 precision 還是 recall？評估指標的選擇見 [模型評估](../evaluation/README.md)。

## 生資情境：大型 omics 檔案

FASTQ、BAM、單細胞 `.h5ad` 動輒數十 GB，重點是**不要讓每個人、每台機器都複製一份**。

| 需求 | 做法 |
| --- | --- |
| 原始定序資料已在機構儲存或公開資料庫 | 不必 `dvc add` 原始檔；用 `dvc import-url` 記錄來源與 hash，或只版本化下游的 count matrix |
| 大檔直接放到 remote、本機不留副本 | `dvc add --to-remote data/fastq`（之後需要時再 `dvc pull`） |
| HPC 上多人共用資料 | 設共享 cache：`dvc cache dir /shared/dvc-cache` + `dvc config cache.shared group` |
| 避免 workspace 與 cache 各存一份 | `dvc config cache.type reflink,symlink,hardlink,copy`（依序嘗試；link 型態下勿直接就地修改檔案） |
| 只要某個 stage 的輸出 | `dvc pull <stage 或檔案>`，不必拉整個 repo 的資料 |
| 清掉不再使用的 cache | `dvc gc -w`（只保留目前 workspace 用到的）；加 `--cloud` 會**刪除 remote 上的舊版本**，先確認沒有其他分支 / tag 要用 |
| 敏感資料（病人資料） | remote 放在機構允許的儲存；憑證寫在 `.dvc/config.local`；hash 本身不含內容，但檔名與路徑可能洩漏資訊 |

> 上游比對、定量這類重計算交給 Nextflow / Snakemake；DVC 適合管理「進入建模前」那段的資料版本與實驗。

## 何時適合 / 不適合

| 適合 | 可能過重 |
| --- | --- |
| 資料太大，不適合進 Git | 少量 CSV、一次性分析 |
| 需要追蹤資料、參數、模型輸出與指標的對應 | 沒有重跑需求 |
| pipeline 需要可重跑、只重算變動部分 | 單人、資料只放本機且不會改 |
| 團隊需要共用資料血緣 (lineage)，而不是各自保存一份 | 已有平台（如 Databricks、SageMaker）統一管資料版本 |

出現「這份資料是哪個版本？」「這次模型怎麼和上週不一樣？」「這個 artifact 是哪個流程生的？」這類問題時，就值得導入。

## 常見錯誤

| 錯誤 | 後果 | 修正 |
| --- | --- | --- |
| `git push` 了但忘了 `dvc push` | 別人 `dvc pull` 失敗 | 推送前兩個都做；可用 `dvc install` 裝 Git hooks 自動化 |
| 手動改 `outs` 裡的檔案 | 和 `dvc.lock` 不一致，下次 `repro` 被覆蓋 | 只透過 stage 的 `cmd` 產生輸出 |
| 參數寫死在腳本裡 | 改參數不會觸發重跑、無法 `params diff` | 從 `params.yaml` 讀，並列在 stage 的 `params` |
| 隨機性沒固定 | 同一版本重跑結果不同 | seed 放進 `params.yaml`（見 [可重現性](../../python-foundations/software-engineering.md)） |
| 把 remote 憑證寫進 `.dvc/config` | 憑證進 Git 歷史 | 用 `dvc remote modify --local` |
| 隨手 `dvc gc --cloud` | 舊版本資料永久消失 | 搭配 `--all-commits` / `--all-tags` 等選項，確認保留範圍 |
