[Computing](../README.md) › 開發者工具

# 開發者工具 (Developer Tools)

日常開發與遠端工作的工具：編輯器、連線到伺服器、保持長時間工作不中斷、傳輸與驗證檔案。生資工作的典型組合是：VS Code（Remote-SSH）+ SSH 金鑰 + tmux + rsync + md5sum。

```text
本機 ──SSH（金鑰、config、ProxyJump）──► 伺服器 / HPC
 │  VS Code Remote-SSH 編輯         │  tmux 保持 session
 └─ rsync / scp 傳檔 ──────────────►│  md5sum 驗證、tar / gzip 打包
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [SSH](ssh.md) | 金鑰登入、`~/.ssh/config`、跳板機、`scp`、port forwarding、VS Code Remote | 怎麼安全方便地連到伺服器？怎麼開遠端的 Jupyter？ |
| [tmux 與 screen](tmux-and-screen.md) | detach / attach、視窗與窗格、對照表 | 斷線後程序怎麼繼續跑？ |
| [rsync](rsync.md) | 常用選項、結尾斜線、排除、鏡像、情境 | 大量資料怎麼傳、怎麼接續？ |
| [檢查碼](checksums.md) | MD5 vs SHA-256、`md5sum -c`、PowerShell `Get-FileHash` | 檔案傳完是否完整？ |
| [壓縮與封存](archiving.md) | 格式選擇、`tar`、gzip vs bgzip、zstd、7z 分割 | 用什麼格式壓縮？為什麼 VCF 要 bgzip？ |
| [編輯器](editors.md) | CRLF / LF、NBSP、VS Code 快捷鍵 / 設定 / 擴充、Notepad++、nano / vim | 換行符號怎麼處理？編輯器怎麼設定？ |

| 相關 | 筆記 |
| --- | --- |
| 命令列基本功 | [Linux 基礎](../operating-system/linux-basics.md) |
| Windows 上的 Linux 環境 | [Windows 與 WSL](../operating-system/windows-and-wsl.md) |
| 版本控制 | [Git](../version-control/git.md) |
