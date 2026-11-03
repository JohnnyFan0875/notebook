[Computing](../README.md) › [版本控制](README.md) › Git

# Git

Git 記錄專案每一次快照 (commit)，讓你可以回到任何版本、在分支上平行開發、與他人合併變更。依任務分節；GitHub 上的協作（PR、review、branch protection）見 [GitHub 協作](github-concepts.md)。

## 心智模型：三個區域

```
工作目錄 (working directory) ──git add──► 暫存區 (staging area / index) ──git commit──► 儲存庫歷史 (repository)
        ▲                                                                                │
        └──────────────────────── git restore / git switch ◄──────────────────────────────┘
                                           本機 repo ──git push──► 遠端 (origin) ──git pull / fetch──► 本機
```

| 區域 | 內容 |
| --- | --- |
| 工作目錄 | 正在編輯的檔案 |
| 暫存區 | 挑選要放進下一個 commit 的變更 |
| 儲存庫 | 已提交的快照，每個 commit 有唯一 ID（hash） |

`git add` 與 `git commit` 分開，是為了讓你挑選、檢查要提交的內容；`git status` 隨時顯示每個檔案在哪個區域。

## 初次設定

```bash
git config --global user.name "Jane Doe"
git config --global user.email "jane@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"       # commit 訊息用 VS Code 編輯
git config --global core.autocrlf input             # Linux / WSL / macOS：提交時把 CRLF 轉成 LF
git config --global pull.rebase false               # pull 時用 merge（或 true：用 rebase）
git config --list --show-origin                     # 查看所有設定與來源檔案
```

| 範圍 | 檔案 | 優先順序 |
| --- | --- | --- |
| `--local` | `<repo>/.git/config` | 最高 |
| `--global` | `~/.gitconfig`（Windows：`C:\Users\<name>\.gitconfig`） | 中 |
| `--system` | `/etc/gitconfig`（Windows：`C:\Program Files\Git\etc\gitconfig`） | 最低 |

連到 GitHub 建議用 SSH 金鑰（`git@github.com:user/repo.git`），設定見 [SSH](../developer-tools/ssh.md#金鑰登入)；HTTPS 則用 Git Credential Manager 或 personal access token。

## 建立與取得 repo

```bash
git clone git@github.com:user/repo.git            # 下載既有 repo
git clone --depth 1 <url>                         # 只要最新版本（大 repo、CI）

git init                                          # 把目前資料夾變成 repo
git remote add origin git@github.com:user/repo.git
git remote -v                                     # 查看遠端
```

## 日常流程

```bash
git status                                  # 1. 看狀態
git diff                                    # 2. 看尚未暫存的變更；git diff --staged 看已暫存的
git add analysis.py                         # 3. 暫存特定檔案
git add .                                   #    暫存目前目錄下所有變更（新增、修改、刪除）
git add -p                                  #    逐段挑選要暫存的變更
git add . ':!data/'                         #    全部但排除 data/
git commit -m "Add QC summary plot"         # 4. 提交；第二個 -m 可加詳細說明
git push                                    # 5. 推到遠端（第一次：git push -u origin main）
git pull                                    # 取得遠端更新並合併（= fetch + merge）
git fetch                                   # 只下載遠端更新，不改動本機分支
```

| commit 訊息 | 說明 |
| --- | --- |
| 第一行 50 字內、祈使句 | `Fix off-by-one in BED parser` |
| 空一行後寫原因 | 為什麼改，而不只是改了什麼 |
| 一個 commit 一件事 | 方便 review、revert、找 bug（`git bisect`） |

## `.gitignore`：不要追蹤的檔案

```gitignore
# 資料與大型產出：不放進 Git
data/
results/
*.bam
*.fastq.gz
# 環境與暫存
.venv/
__pycache__/
.ipynb_checkpoints/
.Rproj.user/
.DS_Store
# 機密
.env
*.pem
```

> **不要把大型資料、模型、機密提交進 Git**：Git 保存所有歷史，刪掉的大檔仍留在 `.git` 裡，repo 會永久變大；機密一旦推上遠端就要視為外洩並更換。大檔用 Git LFS 或 [DVC](../../data-science/machine-learning/production/dvc.md)；已經提交的檔案要停止追蹤：`git rm --cached <file>`，再加進 `.gitignore`。

## 分支

```bash
git branch                           # 列出本機分支；-a 含遠端
git switch -c feature/qc-plot        # 建立並切換（舊寫法：git checkout -b）
git switch main                      # 切換（舊寫法：git checkout main）
git branch new-branch 9a1b3c2        # 從指定 commit / tag 建立分支
git push -u origin feature/qc-plot   # 推送新分支並設定追蹤
git diff main...feature/qc-plot      # 分支相對於 main 的變更

git switch main
git merge feature/qc-plot            # 把分支合併進 main
git branch -d feature/qc-plot        # 刪除已合併的本機分支（-D 強制）
git push origin -d feature/qc-plot   # 刪除遠端分支
```

> 分支彼此隔離：在自己的分支推送壞掉的程式碼，只要沒有人合併或切換到這個分支，其他分支不受影響。

### Merge vs Rebase

```
merge：                         rebase：
main    A─B─C───M               main    A─B─C
         \     /                               \
feature   D─E                   feature         D'─E'   （在 C 之上重新套用，產生新的 commit）
```

| | `git merge` | `git rebase` |
| --- | --- | --- |
| 做法 | 產生 merge commit 結合兩條歷史 | 把 commit 重新套用到新的基底上 |
| 歷史 | 保留分支結構，較雜 | 線性、乾淨 |
| 風險 | 低 | **改寫歷史**：已推送、他人在用的分支不要 rebase |
| 適合 | 整合共享分支 | 把自己的 feature 分支更新到最新 main、整理本機 commit |

```bash
git switch feature/qc-plot
git rebase main                      # 把 feature 移到最新的 main 之上
git rebase -i HEAD~3                 # 互動式：squash、重排、改訊息（只對未推送的 commit）
git push --force-with-lease          # rebase 後推送自己的分支（比 --force 安全）
```

### 衝突

合併時兩邊改了同一段，Git 會在檔案中標記：

```text
<<<<<<< HEAD
threshold = 30
=======
threshold = 20
>>>>>>> feature/qc-plot
```

編輯成最終想要的內容並刪除標記 → `git add <file>` → `git commit`（merge）或 `git rebase --continue`。放棄：`git merge --abort` / `git rebase --abort`。以最終程式應有的樣子為準，而不是盲目選一邊；解完跑測試。

## 復原

| 想做的事 | 指令 |
| --- | --- |
| 取消暫存（保留修改） | `git restore --staged <file>` |
| 丟棄工作目錄中的修改 | `git restore <file>`（**無法復原**） |
| 同時取消暫存並丟棄 | `git restore --staged --worktree <file>` |
| 修改上一個 commit（訊息或補檔案，尚未推送） | `git commit --amend` |
| 撤銷最近 n 個 commit，變更留在工作目錄 | `git reset HEAD~n`（預設 `--mixed`） |
| 撤銷 commit，變更保留在暫存區 | `git reset --soft HEAD~1` |
| 撤銷 commit 並丟棄所有變更 | `git reset --hard <commit>`（**危險**） |
| 撤銷**已推送**的 commit | `git revert <commit>`：產生一個反向的新 commit，不改寫歷史 |
| 找回誤刪的 commit / 分支 | `git reflog` 找到 ID，再 `git branch rescue <id>` |
| 停止追蹤但保留檔案 | `git rm --cached <file>` |
| 刪除檔案（下次 commit 生效） | `git rm <file>`、`git rm -r <folder>` |

> 已推送到共享分支的 commit 用 `revert`，不要 `reset` 後強制推送，否則會打亂其他人的歷史。

## Stash：暫存未完成的工作

```bash
git stash push -m "WIP: QC plot"     # 存起未提交的變更（含已暫存），工作目錄回到乾淨狀態
git stash list
git stash pop                        # 取回最近一筆並從清單刪除；apply 則保留在清單中
git stash drop stash@{1}             # 刪除特定一筆；git stash clear 刪除全部
```

情境：有未提交的修改卻要切換分支（`stash` → `switch` → 回來後 `stash pop`）；或先 stash 再 `pull`，之後 `pop`。

## 歷史與標籤

```bash
git log --oneline -n 10                          # 最近 10 個 commit
git log --oneline --graph --all --decorate       # 分支圖
git log -p -- analysis.py                        # 某檔案的修改歷史與內容
git log -S "threshold"                           # 哪個 commit 加入 / 移除了這個字串
git blame analysis.py                            # 每一行最後是誰、哪個 commit 改的
git show 4e5f6g7                                 # 某個 commit 的內容

git tag -a v1.0 -m "Paper submission" 4e5f6g7    # 附註標籤：標記版本、投稿時的程式碼
git push origin v1.0                             # 標籤要另外推送（或 git push --tags）
git switch --detach v1.0                         # 檢視某個版本
```

> 論文投稿或分析交付時打標籤，日後可精確重現當時的程式碼；搭配環境鎖定（`uv.lock`、`environment.yml`、容器）才完整。

## Worktree：同時檢出多個分支

```bash
git worktree add -b hotfix ../repo-hotfix main   # 在另一個資料夾開新分支，不影響目前工作
git worktree list
git worktree remove ../repo-hotfix
git worktree prune
```

適合：正在跑長時間分析的分支不想切走，又需要在另一個分支修 bug。

## 在提示字元顯示目前分支

```bash
# ~/.bashrc
parse_git_branch() { git branch 2>/dev/null | sed -n 's/^\* \(.*\)/(\1)/p'; }
export PS1="\u@\h \[\e[32m\]\w \[\e[91m\]\$(parse_git_branch)\[\e[00m\]$ "
```

`source ~/.bashrc` 重新載入。Git for Windows 的 Git Bash 預設已顯示分支。

| 參考 | 連結 |
| --- | --- |
| GitHub Git 速查表 | [Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf) |
| 官方文件 | [git-scm.com/docs](https://git-scm.com/docs) |
