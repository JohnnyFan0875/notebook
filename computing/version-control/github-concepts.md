[Computing](../README.md) › [版本控制](README.md) › GitHub 協作

# GitHub 協作 (GitHub Collaboration)

Git 負責記錄歷史；GitHub 是建立在 Git repo 之上的協作平台：託管、issue、pull request、review、CI、權限與分支保護。GitLab、Bitbucket 的概念大致相同（GitLab 稱 merge request）。

## 核心概念

| 概念 | 用途 |
| --- | --- |
| Repository | 程式碼、issue、歷史的共同家園；public / private |
| Branch | 隔離的工作線；預設分支通常是 `main` |
| Fork | 複製一份別人的 repo 到自己帳號下，用於貢獻沒有寫入權限的專案 |
| Issue | 追蹤 bug、需求、待辦；可用 `#123` 互相引用 |
| Pull request (PR) | 提出一組變更，供討論、review、檢查後合併 |
| Review | 留言、要求修改、核准 |
| Actions | CI/CD：push 或 PR 時自動跑測試、建置、部署（見 [DevOps](../devops/README.md)） |
| Branch protection / rulesets | 限制重要分支的直接修改 |
| Release | 以 tag 為基礎的版本發佈，可附檔案；可連結 Zenodo 取得 DOI |

## Pull Request 流程

```
1. 建立 feature 分支           git switch -c fix/bed-parser
2. 在本機 commit               git commit -m "Fix off-by-one in BED parser"
3. 推送分支                    git push -u origin fix/bed-parser
4. 開 PR（網頁或 gh CLI）      gh pr create --fill
5. CI 檢查 + review            依意見修改，再 push 到同一分支（PR 自動更新）
6. 合併到受保護的 main         Merge / Squash / Rebase
7. 刪除分支、更新本機           git switch main && git pull
```

PR 不只是合併按鈕，而是 review 與討論的單位：

| 好的 PR | 說明 |
| --- | --- |
| 範圍集中 | 一個 PR 一件事；大改動拆成多個 |
| 說明為什麼 | 動機、做法、如何測試；UI 或圖表改動附截圖 |
| 連結 issue | 描述中寫 `Closes #123`，合併時自動關閉 issue |
| 先自己看過 diff | 移除除錯輸出、無關的格式變動 |
| CI 通過才請人 review | 不浪費 reviewer 時間 |

| 合併方式 | 結果 | 適合 |
| --- | --- | --- |
| Create a merge commit | 保留所有 commit + 一個 merge commit | 需要完整歷史 |
| Squash and merge | 整個 PR 壓成一個 commit | commit 很零碎的 feature；main 歷史最乾淨 |
| Rebase and merge | 逐一重新套用到 main，線性歷史 | commit 本身已整理好 |

## 分支保護

在 Settings → Branches（或 Rules → Rulesets）對 `main` 設定：

| 規則 | 效果 |
| --- | --- |
| 合併前必須開 PR | 禁止直接 push 到 main |
| 需要 N 個核准 | 至少有人看過 |
| 必須通過狀態檢查 | 測試、lint 沒過不能合併 |
| 分支必須是最新的 | 合併前要包含 main 的最新變更 |
| 禁止強制推送與刪除 | 保護歷史 |

這些是工作流程的安全網，不是為了官僚：減少意外弄壞 main，讓協作可預期。

## 其他實用功能

| 功能 | 用途 |
| --- | --- |
| `gh` CLI | 命令列操作 PR、issue、Actions：`gh pr list`、`gh pr checkout 42`、`gh run watch` |
| CODEOWNERS | 指定各路徑的負責人，PR 自動請他們 review |
| Issue / PR 範本 | `.github/ISSUE_TEMPLATE/`、`.github/pull_request_template.md` |
| Dependabot | 自動開 PR 更新相依套件與安全修補 |
| GitHub Pages | 從 repo 發佈靜態網站（文件、報告） |
| Codespaces | 雲端開發環境，可用 dev container 設定 |
| Zenodo 整合 | 每次 release 自動封存並產生 DOI，供論文引用程式碼 |

> 研究程式碼的可重現性：公開 repo + 打 tag 的 release + Zenodo DOI + 鎖定的環境檔，論文中引用 DOI 而不是會變動的分支。
