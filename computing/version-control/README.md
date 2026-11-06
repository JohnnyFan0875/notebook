[Computing](../README.md) › 版本控制

# 版本控制 (Version Control)

用 Git 記錄程式碼的每個版本、用 GitHub 協作。分析程式碼、pipeline、筆記都應該放在版本控制下；資料與大型產出則不放進 Git（用 [DVC](../../data-science/machine-learning/production/dvc.md) 或資料倉儲）。

```text
Git（本機：commit、branch、merge、復原）→ GitHub（遠端：PR、review、CI、保護分支）
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Git](git.md) | 三個區域、日常流程、`.gitignore`、分支、merge vs rebase、衝突、復原、stash、tag、worktree | 怎麼記錄、切換、合併、還原版本？ |
| [GitHub 協作](github-concepts.md) | fork、PR 流程與合併方式、分支保護、`gh` CLI、Zenodo DOI | 團隊怎麼 review 與整合變更？ |

| 相關 | 筆記 |
| --- | --- |
| SSH 金鑰連 GitHub | [SSH](../developer-tools/ssh.md) |
| PR 自動測試 | [DevOps](../devops/README.md) |
| 換行符號 CRLF / LF | [編輯器](../developer-tools/editors.md) |
