[Computing](../README.md) › [開發者工具](README.md) › tmux 與 screen

# tmux 與 screen (Terminal Multiplexers)

終端機多工器 (terminal multiplexer) 讓你在一個 SSH 連線裡開多個 shell，並且可以**中斷連線 (detach) 後程序繼續跑**，之後重新接回 (attach)。在遠端伺服器跑長時間的工作（比對、下載、互動式分析）時，網路斷線或關掉筆電都不會中斷程序。tmux 功能較完整，是新環境的首選；screen 歷史較久，許多舊伺服器預設已安裝。

```
SSH 登入 → tmux new -s align → 啟動工作 → Ctrl+b d（detach）→ 登出
       ↓（隔天）
SSH 登入 → tmux a -t align → 工作仍在跑，畫面與輸出都在
```

> 在 HPC 的**登入節點**上用 tmux 保持互動式 session 可以，但重運算要交給排程器（Slurm），不要在登入節點跑。

## 對照表

| 任務 | tmux（前綴 `Ctrl + b`） | screen（前綴 `Ctrl + a`） |
| --- | --- | --- |
| 新 session | `tmux` | `screen` |
| 新 session（命名） | `tmux new -s name` | `screen -S name` |
| 列出 session | `tmux ls` | `screen -ls` |
| 接回 | `tmux a -t name`（`a` = attach） | `screen -r name` |
| 強制接回（另一處仍連著） | `tmux a -d -t name` | `screen -d -r name` |
| 中斷連線 (detach) | 前綴 `d` | 前綴 `d` |
| 新視窗 | 前綴 `c` | 前綴 `c` |
| 下一個 / 上一個視窗 | 前綴 `n` / `p` | 前綴 `n` / `p` |
| 列出視窗並切換 | 前綴 `w` | 前綴 `"` |
| 重新命名 session | `tmux rename-session -t 0 name` 或前綴 `$` | 前綴 `:sessionname name` |
| 水平 / 垂直分割窗格 | 前綴 `"` / `%` | 前綴 `S` / `\|`（較陽春） |
| 切換窗格 | 前綴 方向鍵 | 前綴 `Tab` |
| 捲動歷史輸出 | 前綴 `[`，方向鍵 / PgUp 捲動，`q` 離開 | 前綴 `Esc`，捲動後 `Esc` 離開 |
| 關閉目前視窗 | `exit` 或 `Ctrl + d` | `exit` |
| 結束指定 session | `tmux kill-session -t name` | `screen -X -S name quit` |
| 結束全部 | `tmux kill-server` | — |

> 前綴鍵的用法：同時按 `Ctrl` 與 `b`，**放開**，再按下一個鍵（例如 `c`）。

## 實用設定（`~/.tmux.conf`）

```bash
set -g mouse on                  # 滑鼠捲動、點選窗格、拖曳調整大小
set -g history-limit 50000       # 捲動歷史行數
set -g base-index 1              # 視窗從 1 開始編號
bind r source-file ~/.tmux.conf \; display "reloaded"   # 前綴 r 重新載入設定
```

修改後在 tmux 中按前綴 `:` 輸入 `source-file ~/.tmux.conf`，或重開 session。

## 常見用法

| 情境 | 做法 |
| --- | --- |
| 長時間比對 / 下載 | `tmux new -s align`，執行後 detach |
| 一邊看 log 一邊下指令 | 分割窗格：一格 `tail -f run.log`，一格操作 |
| 監看資源 | 一個視窗放 `htop`，一個放 `watch -n 5 squeue -u $USER` |
| 互動式 R / Python | 在 tmux 中開 R / IPython，斷線不會遺失變數 |

| 注意 | 說明 |
| --- | --- |
| 伺服器重開機 | session 會消失；tmux 不是持久化工具 |
| 登入到不同節點 | session 在哪台機器建立就只在那台；叢集有多個登入節點時要記得是哪一台（`hostname`） |
| 結束後清理 | 不用的 session 用 `kill-session` 關掉，避免佔資源 |
