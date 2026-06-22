# Data Versioning and DVC

## Why Data Versioning Exists

code versioning 很成熟，但資料版本管理其實是另一個問題。

原因很直接：

- codebase 通常比 dataset 小得多
- dataset 會隨時間更新、清理、重抽樣
- 同一份 code，在不同資料版本上可能得到不同結果
- 同一份資料，在不同參數設定下也可能得到不同結果

所以 data versioning 的目標，不只是「保存舊資料」，而是讓團隊可以回答：

- 這次模型或報表是用哪份資料做的？
- 資料是什麼時候變的？
- 為什麼這次結果和上次不同？
- 我能不能把當時的結果重跑出來？

## What Data Versioning Means

data versioning 可以把它想成資料世界裡的 version control。

它的核心工作是：

- 監控資料變化
- 對資料做 snapshots
- 保留可回溯的版本歷史
- 讓資料、參數、程式與結果之間的關係可追蹤

實務上的價值通常落在：

- retrieval and scrutiny
- consistency
- accountability
- lineage

## Data Versioning vs. Code Versioning

兩者精神很像，但對象不同。

| Theme | Code Versioning | Data Versioning |
| --- | --- | --- |
| 主要工具 | Git | DVC 這類工具搭配 Git |
| 對象 | source code | datasets、artifacts、metrics、pipeline metadata |
| 難點 | merge 與協作 | 資料量大、複製成本高、追蹤鏈較長 |
| 主要價值 | 回溯程式變更 | 回溯資料與結果變更 |

可以把 Git 想成管理 repository 的文字歷史，而 DVC 這類工具是在補上「大型資料與實驗輸出不適合直接進 Git」的那一段。

## Why This Matters for Reproducibility

很多模型或資料流程不可重現，不是因為演算法太複雜，而是因為沒有同時鎖住這些東西：

- data version
- parameter version
- code version
- pipeline steps
- output metrics

只要其中一個漂移，就可能讓結果不同。

例如：

- dataset 換了，metrics 可能變
- hyperparameters 換了，metrics 也可能變
- code refactor 後沒有保持同樣邏輯，結果還是會變

所以 reproducibility 不是單靠 `requirements.txt` 或 Git commit 就能完成，而是要連資料與執行流程一起被版本化。

## What DVC Adds

DVC 常被用來補 Git 的不足，特別是在以下幾件事上：

- 追蹤大型資料檔與 artifacts
- 用 metadata 方式描述資料，而不是把大型檔案直接塞進 Git
- 管理 pipeline stages 與 dependencies
- 比較 metrics 與 plots
- 串接 remote storage

從工作方式來看，可以把它想成：

- Git 追蹤 code 與小型設定檔
- DVC 追蹤 data、artifacts、pipeline metadata

## Basic DVC Workflow

一個最基本的 DVC 專案通常會有這樣的節奏：

1. 先初始化 Git repository
2. 在 repo 內執行 `dvc init`
3. 用 `dvc add` 追蹤資料檔或資料夾
4. 把 DVC 產生的 metadata 與設定檔交給 Git 管理
5. 視需要設定 remote storage

這個流程的重點不是指令本身，而是責任分工：

- Git 管理版本歷史與協作
- DVC 管理大型資料與可重現流程

## Internal Files and Ignore Rules

DVC 初始化後，通常會建立一些應該納入 Git 的內部檔案，例如：

- `.dvc/config`
- `.dvc/.gitignore`
- `.dvcignore`

其中 `.dvcignore` 的角色很像 `.gitignore`：

- 使用相似語法
- 指定哪些檔案或資料夾不該被 DVC 納入處理
- 在資料很多時能降低掃描與操作成本

這一點很重要，因為 data versioning 不是「所有東西都追」，而是要明確界定哪些是正式資料資產、哪些只是暫存或不重要輸出。

## Cache and Storage Mindset

DVC 會用 cache 的概念來管理資料內容，而不是單純依檔名工作。

實務上這代表：

- 相同內容可以被穩定辨識
- repository 不必把每個大型檔案都直接複製進 Git 歷史
- local workspace、cache 與 remote storage 之間可以分工

這也是為什麼 DVC 通常很適合：

- 大型訓練資料
- 中繼 artifacts
- 模型輸出
- 需要多人協作但不想把大檔塞進 Git 的專案

但同時也要注意：

- cache 會佔空間
- 清 cache 前要先確認哪些資料仍被 workspace 或版本使用
- remote policy 要先想好，不然團隊很容易只在本地「看起來可重現」

## Parameters and Single Source of Truth

production-grade pipeline 的一個重要特徵，是參數不要散落在不同 script 裡。

好的做法通常是：

- 把參數集中在 `params.yaml` 之類的檔案
- 讓 preprocessing、training、evaluation 共用同一份 parameter source
- 用明確結構區分不同 stage 需要的設定

這樣做的好處是：

- 比較容易重跑
- 比較容易 diff
- 比較容易審查實驗變更
- 減少「改了某個 notebook cell 但忘了記錄」的風險

## Reproducible Pipeline Structure

DVC 不只管檔案，也能描述 pipeline。

核心檔案通常是 `dvc.yaml`，裡面會定義一連串 stages，以及每個 stage 的：

- `deps`: 輸入資料或腳本
- `params`: 參數依賴
- `cmd`: 執行命令
- `outs`: 產出 artifacts
- `metrics` / `plots`: 要追蹤的結果

這種設計的價值在於：workflow 不再只存在某個 notebook 的執行順序，而是被正式描述成一個可重跑、可視覺化、可版本化的 pipeline。

## Reproducibility and Code Quality

這個課程也提醒了一個很實務的點：DVC 不能拯救混亂的原型碼。

如果程式本身：

- 不模組化
- 重複邏輯太多
- 沒有單一參數來源
- 缺乏明確 entry points

那就算加了 DVC，流程也很難真正變成 production-ready。

比較健康的方向通常是：

- 把 prototype code 拆成可測試模組
- 用 entry-point scripts 連接 stages
- 把 evaluation 邏輯抽成獨立函式
- 讓 config、code、data、outputs 的邊界清楚

## Metrics and Plots Tracking

DVC 的另一個價值，是把實驗結果也納入可比較範圍。

常見能力包括：

- 顯示 metrics
- 比較不同版本的 metrics
- 顯示 plots
- 比較不同版本的 plots

這讓團隊不只能說「模型變好了」，而是能回答：

- 哪個參數改動帶來改善？
- 是資料版本影響比較大，還是模型設定影響比較大？
- 這次的提升是 precision 還是 recall 在變？

對資料科學與機器學習專案來說，這是把「實驗感覺」轉成「可審計比較」的重要一步。

## When DVC Fits Well

DVC 特別適合這些情境：

- dataset 太大，不適合直接進 Git
- 需要追蹤資料、參數、模型輸出與實驗結果
- pipeline 需要可重跑
- 團隊需要 shared lineage，而不是每個人本地各自保存一份資料

如果只是少量 CSV、一次性分析、沒有重跑需求，那 DVC 可能偏重。

但只要專案開始出現下面訊號，就很值得考慮：

- 「這份資料是哪個版本？」
- 「這次模型怎麼和上週不一樣？」
- 「這個結果還能不能重現？」
- 「這個 artifact 是哪個流程生的？」

## Practical Reminders

- data versioning 的核心不是備份，而是可回溯與可重現。
- Git 與 DVC 不是替代關係，而是互補關係。
- `params.yaml` 這類設定檔的價值，在於把參數從零散腳本中拉回單一來源。
- `dvc.yaml` 把 workflow 從隱性執行順序，變成顯性依賴圖。
- 如果 code 還停留在 prototype 階段，只加 DVC 通常不會自動得到 production-grade reproducibility。

[Back to Data Engineering](README.md)
