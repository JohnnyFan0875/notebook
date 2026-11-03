[Computing](../README.md) › [開發者工具](README.md) › SSH

# SSH 與遠端伺服器 (SSH)

SSH (Secure Shell) 是登入遠端 Linux 伺服器、HPC 叢集、雲端 VM 的標準方式：加密的命令列連線，另外提供檔案傳輸（`scp`、`rsync`、`sftp`）與連接埠轉發（在本機瀏覽器開遠端的 Jupyter / RStudio）。Linux、macOS、Windows 10+（PowerShell / WSL）都內建 `ssh` 指令。

## 連線

```bash
ssh alice@hpc.example.edu                 # 使用者@主機
ssh -p 2222 alice@hpc.example.edu         # 非預設 port（預設 22）
ssh alice@hpc.example.edu 'df -h ~'       # 只執行一個指令就離開
exit                                      # 登出（或 Ctrl + D）
```

第一次連線會詢問主機指紋 (host key fingerprint)，確認後存進 `~/.ssh/known_hosts`；之後若指紋改變會出現 `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED`，可能是伺服器重灌，也可能是中間人攻擊，先向管理者確認，再用 `ssh-keygen -R <host>` 移除舊紀錄。

## 金鑰登入

密碼登入每次都要輸入，且容易被暴力破解；金鑰登入更安全也更方便，很多 HPC 與雲端 VM 只允許金鑰。

```
本機：私鑰 ~/.ssh/id_ed25519（絕不外流）  ──簽章──►  伺服器：~/.ssh/authorized_keys 中的公鑰驗證
      公鑰 ~/.ssh/id_ed25519.pub（可公開）
```

```bash
# 1. 產生金鑰對（建議設定 passphrase 保護私鑰）
ssh-keygen -t ed25519 -C "alice@laptop"

# 2. 把公鑰放到伺服器
ssh-copy-id alice@hpc.example.edu                  # Linux / macOS / WSL
```

```powershell
# Windows PowerShell 沒有 ssh-copy-id，改用：
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh alice@hpc.example.edu "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

| 檔案 | 權限 | 說明 |
| --- | --- | --- |
| `~/.ssh/` | `700` | 權限太寬鬆時 SSH 會拒絕使用金鑰 |
| `~/.ssh/id_ed25519`（私鑰） | `600` | 只有自己可讀 |
| `~/.ssh/authorized_keys`（伺服器端） | `600` | 每行一把允許登入的公鑰 |
| `~/.ssh/config` | `600` | 連線設定 |

> GitHub 也用同樣的金鑰：把 `id_ed25519.pub` 貼到 GitHub → Settings → SSH and GPG keys，就能用 `git@github.com:user/repo.git` 推送，見 [Git](../version-control/git.md)。PDF 數位簽章也是同樣的公開金鑰原理，見 [Acrobat 數位簽章](../../productivity/documents/acrobat-digital-signature.md)。

### ssh-agent：passphrase 只輸入一次

```bash
eval "$(ssh-agent -s)"           # Linux / WSL：啟動 agent
ssh-add ~/.ssh/id_ed25519        # 輸入一次 passphrase，之後這個 session 不再詢問
ssh-add -l                       # 列出已載入的金鑰
```

Windows 用內建的 OpenSSH Authentication Agent 服務（服務中設為自動啟動後執行 `ssh-add`）；macOS 在 config 加 `UseKeychain yes`。

## `~/.ssh/config`：連線設定

把常用主機寫成別名，之後 `ssh hpc`、`rsync data/ hpc:/scratch/`、VS Code Remote 都能直接用。

```text
Host hpc
    HostName hpc.example.edu
    User alice
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60          # 每 60 秒送 keepalive，避免閒置斷線

Host compute
    HostName node042                # 只能從登入節點連到的計算節點 / 內網主機
    User alice
    ProxyJump hpc                   # 經由 hpc 跳板

Host github.com
    IdentityFile ~/.ssh/id_ed25519_github
```

| 設定 | 作用 |
| --- | --- |
| `HostName` / `User` / `Port` | 實際主機、使用者、port |
| `IdentityFile` | 使用哪把私鑰 |
| `ProxyJump` | 經由跳板機 (bastion / jump host) 連線；指令列寫法 `ssh -J hpc node042` |
| `ServerAliveInterval` | 防止閒置被防火牆切斷 |
| `LocalForward 8888 localhost:8888` | 連線時自動建立 port 轉發 |
| `ControlMaster auto` + `ControlPath` + `ControlPersist` | 共用連線：第二個 ssh 不必重新驗證（需要 2FA 的 HPC 很有用；Windows OpenSSH 不支援） |

## 傳輸檔案

```bash
scp results.tsv hpc:/project/                    # 上傳單一檔案
scp hpc:/project/report.html .                   # 下載
scp -r hpc:/project/figures ./                   # 目錄
rsync -avhP data/ hpc:/scratch/data/             # 大量 / 可接續的傳輸（優先）
sftp hpc                                         # 互動式：ls、get、put
```

大量資料用 [rsync](rsync.md)，傳完用 [檢查碼](checksums.md) 驗證。

## 連接埠轉發 (Port Forwarding)

伺服器上跑的 Jupyter、RStudio Server、Shiny、TensorBoard 只聽 `localhost`，外部連不到；SSH 通道把本機的 port 轉到遠端。

```bash
# 遠端：在 tmux 中啟動 Jupyter（不開瀏覽器、指定 port）
jupyter lab --no-browser --port 8888

# 本機：把本機 8888 轉到遠端的 localhost:8888
ssh -N -L 8888:localhost:8888 hpc
# 然後在本機瀏覽器開 http://localhost:8888（token 見遠端輸出）

# Jupyter 跑在計算節點 node042 上：經由登入節點轉發
ssh -N -L 8888:node042:8888 hpc
```

| 選項 | 意義 |
| --- | --- |
| `-L 本機port:目標主機:目標port` | 本機轉發；「目標主機」是從**伺服器**角度看的位址 |
| `-N` | 不開 shell，只建立通道 |
| `-f` | 背景執行 |
| `-R` | 反向轉發（讓遠端連回本機） |
| `-D 1080` | 動態轉發 (SOCKS proxy) |

> 本機 port 已被占用時換一個（`-L 9999:localhost:8888`，開 `localhost:9999`）。在 HPC 上，Jupyter 應透過排程器在計算節點啟動，或使用叢集提供的 Open OnDemand 入口。

## VS Code Remote-SSH

安裝 Remote - SSH 擴充後：命令選擇區 → Remote-SSH: Connect to Host → 選 `~/.ssh/config` 中的別名。之後編輯器、終端機、Python / R 擴充都在遠端執行，本機只負責介面。詳見 [編輯器](editors.md)。

| 注意 | 說明 |
| --- | --- |
| 會在遠端家目錄安裝 `~/.vscode-server` | 家目錄配額小的 HPC 要留意 |
| 擴充在遠端執行 | 會佔用登入節點資源；重運算仍交給排程器 |

## 疑難排解

| 症狀 | 檢查 |
| --- | --- |
| `Permission denied (publickey)` | 公鑰是否在 `authorized_keys`；`~/.ssh` 與私鑰權限；config 的 `IdentityFile` 是否正確 |
| 仍然要求輸入密碼 | 同上；伺服器可能不允許金鑰登入 |
| `Connection timed out` | 主機名、port、VPN、防火牆 |
| 閒置後斷線 | `ServerAliveInterval 60`；長工作放在 [tmux](tmux-and-screen.md) |
| 不知道哪裡出錯 | `ssh -v hpc`（`-vvv` 更詳細）看驗證過程 |
| `UNPROTECTED PRIVATE KEY FILE` | `chmod 600 ~/.ssh/id_ed25519`；Windows 上私鑰權限只能有自己的帳號 |
