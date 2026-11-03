[Computing](../README.md) › [作業系統](README.md) › Windows 與 WSL

# Windows 與 WSL (Windows and WSL)

生資工具（samtools、bcftools、STAR、多數 bioconda 套件）幾乎都只支援 Linux / macOS。在 Windows 上最好的做法是 **WSL 2**（Windows Subsystem for Linux）：在 Windows 裡跑一個真正的 Linux 核心，與 Windows 檔案、VS Code、Docker Desktop 整合。本篇涵蓋 WSL 安裝與檔案互通、bash 與 PowerShell 對照，以及常用的 Windows 設定。

## WSL 安裝與基本操作

```powershell
# PowerShell（系統管理員）
wsl --install                      # 安裝 WSL 2 與預設的 Ubuntu，完成後重新開機
wsl --list --online                # 可安裝的發行版
wsl --install -d Ubuntu-24.04      # 指定發行版
wsl -l -v                          # 已安裝的發行版與 WSL 版本
wsl --update                       # 更新 WSL
wsl --shutdown                     # 關閉所有 WSL（改完設定後要重啟）
wsl                                # 進入預設發行版的 shell
```

首次進入 Ubuntu 會要求建立 Linux 使用者帳號（與 Windows 帳號無關），接著：

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl unzip
# 之後安裝 conda / mamba、uv、Docker 等見各自筆記
```

## 檔案系統互通

| 從 | 存取 | 路徑 |
| --- | --- | --- |
| WSL | Windows 的 C 槽 | `/mnt/c/Users/<name>/Documents` |
| Windows | WSL 的家目錄 | 檔案總管輸入 `\\wsl$\Ubuntu\home\<user>`（或 `\\wsl.localhost\...`） |
| WSL | 用 Windows 檔案總管開目前目錄 | `explorer.exe .` |
| WSL | 用 VS Code 開目前目錄 | `code .`（需安裝 WSL 擴充套件，見 [編輯器](../developer-tools/editors.md)） |

> **專案檔案放在 WSL 的檔案系統**（`~/projects`），不要放在 `/mnt/c`：跨檔案系統存取慢很多（大量小檔、`git status`、編譯尤其明顯），權限與換行符號也容易出問題。只有需要用 Windows 程式開啟的成果才放到 `/mnt/c`。

| 問題 | 原因 | 處理 |
| --- | --- | --- |
| 腳本出現 `$'\r': command not found` | 檔案是 Windows 換行 CRLF | `dos2unix script.sh`；編輯器設定 LF；`git config --global core.autocrlf input` |
| `/mnt/c` 下的檔案權限全是 777 | Windows 檔案系統沒有 Linux 權限 | 把專案放在 WSL 內 |
| WSL 吃掉太多記憶體 | 預設最多可用主機記憶體的一半 | 在 `%UserProfile%\.wslconfig` 設定 `[wsl2]` 區段的 `memory=8GB`、`processors=4`，再 `wsl --shutdown` |
| Docker 指令找不到 | — | Docker Desktop → Settings → Resources → WSL integration 勾選發行版 |

## bash vs PowerShell 對照

PowerShell 的管線傳遞的是**物件**而不是文字，所以許多文字處理指令沒有一對一對應；處理文字資料時在 WSL 用 bash 比較順手。

| 任務 | bash（Linux / WSL / macOS） | PowerShell |
| --- | --- | --- |
| 列出檔案 | `ls -lh` | `Get-ChildItem`（別名 `ls`、`dir`） |
| 切換目錄 | `cd /data` | `Set-Location C:\data`（`cd`） |
| 看檔案內容 | `cat file` | `Get-Content file`（`cat`） |
| 前 / 後 10 行 | `head -n 10 file`、`tail -n 10 file` | `Get-Content file -TotalCount 10`、`-Tail 10` |
| 搜尋文字 | `grep -i error log.txt` | `Select-String -Pattern error log.txt` |
| 遞迴找檔案 | `find . -name "*.csv"` | `Get-ChildItem -Recurse -Filter *.csv` |
| 計數行數 | `wc -l file` | `(Get-Content file \| Measure-Object -Line).Lines` |
| 複製 / 移動 / 刪除 | `cp`、`mv`、`rm -r` | `Copy-Item`、`Move-Item`、`Remove-Item -Recurse` |
| 建立目錄（多層） | `mkdir -p a/b` | `New-Item -ItemType Directory -Force a\b` |
| 環境變數 | `export VAR=x`；`echo $VAR` | `$env:VAR = "x"`；`$env:VAR` |
| 指令位置 | `which python` | `(Get-Command python).Source` |
| 串接指令 | `cmd1 && cmd2` | PowerShell 7：`cmd1 && cmd2`；5.1：`cmd1; if ($?) { cmd2 }` |
| 丟棄輸出 | `> /dev/null` | `> $null` |
| 下載 | `curl -L -O url` | `Invoke-WebRequest url -OutFile f`（5.1 的 `curl` 是它的別名，加 `.exe` 才是真的 curl） |
| 檔案雜湊 | `sha256sum file` | `Get-FileHash file -Algorithm SHA256` |

| 注意 | 說明 |
| --- | --- |
| 路徑分隔 | Windows `\`，Linux `/`；PowerShell 兩者都接受 |
| 大小寫 | Linux 檔名區分大小寫，Windows 不區分 |
| 執行腳本被擋 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| 版本 | Windows 內建 PowerShell 5.1；PowerShell 7（`pwsh`）需另外安裝，跨平台、語法較新 |

## Windows 設定

### Windows 11 右鍵選單改回傳統樣式

在命令提示字元或 PowerShell 執行（注意要用**半形**引號；從網頁複製來的全形 `“ ”` 會讓指令失敗）：

```powershell
# 改為傳統右鍵選單
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve

# 還原為 Windows 11 預設
reg.exe delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" /f
```

執行後重新啟動檔案總管（工作管理員 → Windows 檔案總管 → 重新啟動）或登出再登入。不改登錄檔時，也可以在新選單按 `Shift + F10` 或「顯示其他選項」叫出傳統選單。

### 其他實用設定

| 設定 | 位置 / 指令 |
| --- | --- |
| 顯示副檔名與隱藏檔 | 檔案總管 → 檢視 → 顯示 → 副檔名、隱藏的項目 |
| 長路徑支援（超過 260 字元） | `reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f`（系統管理員）；Git 另設 `git config --global core.longpaths true` |
| 套件管理器 | `winget install Git.Git`、`winget install astral-sh.uv`、`winget upgrade --all` |
| 終端機 | Windows Terminal：同一視窗開 PowerShell、WSL、cmd 分頁 |
