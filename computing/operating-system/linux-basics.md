[Computing](../README.md) › [作業系統](README.md) › Linux 基礎指令

# Linux 基礎指令 (Linux Basics)

在伺服器、HPC 與容器裡做事的基本功：瀏覽檔案、查看內容、搜尋、權限、程序、磁碟與網路。依任務分節；文字資料的切欄、排序、統計見 [命令列資料處理](command-line-data-processing.md)，寫成腳本見 [Shell 腳本](shell-scripting.md)。Windows 上用 [WSL](windows-and-wsl.md) 取得同樣的環境。

## 檔案系統與路徑

| 路徑 | 意義 |
| --- | --- |
| `/` | 根目錄 |
| `~` | 家目錄（`/home/<user>`） |
| `.` / `..` | 目前目錄 / 上一層 |
| `/tmp` | 暫存；HPC 上常用節點本機的 `$TMPDIR` 或 scratch |
| 絕對 vs 相對路徑 | `/data/a.bam` vs `data/a.bam`（相對於目前目錄） |

```bash
pwd                          # 目前位置
ls -lh                       # 詳細列表，檔案大小以 K / M / G 顯示
ls -lhtr                     # 依修改時間排序，最新的在最後
cd /data/project; cd -       # 切換目錄；cd - 回到上一個目錄
mkdir -p results/qc          # 一次建立多層
cp -r src/ backup/           # 複製目錄
mv old.txt new.txt           # 移動 / 改名
rm file; rm -r dir/          # 刪除；沒有資源回收筒，rm -rf 前再確認一次路徑
ln -s /ref/hg38.fa hg38.fa   # 符號連結：不複製大檔
realpath hg38.fa             # 解析出實際的絕對路徑
```

## 查看檔案內容

| 想做的事 | 指令 |
| --- | --- |
| 看開頭 / 結尾 | `head -n 10 file`、`tail -n 10 file` |
| 持續追蹤增長中的 log | `tail -f run.log` |
| 分頁瀏覽、不折行（寬表格） | `less -S file`（`/` 搜尋、`q` 離開） |
| 看壓縮檔 | `zless -S file.gz`、`zcat file.gz \| head` |
| 數行數 | `wc -l file`；壓縮檔 `zcat file.gz \| wc -l` |
| 合併多檔 | `cat a.txt b.txt > all.txt` |
| 對齊欄位顯示 | `column -t -s $'\t' file.tsv \| less -S` |
| 檔案類型、編碼 | `file data.csv` |

> FASTQ 每 4 行一筆 read：`echo $(( $(zcat r1.fastq.gz | wc -l) / 4 ))` 計算 read 數。

## 搜尋

```bash
# grep：在檔案內容中找文字
grep 'keyword' file                     # 符合的行
grep -v 'keyword' file                  # 排除
grep -i -n -c 'error' run.log           # 不分大小寫、顯示行號、只計數
grep -E 'error|warn|fail' run.log       # 多個關鍵字（延伸正規表達式；egrep 已不建議）
grep -e 'kw1' -e 'kw2' file             # 同上，另一種寫法
grep -r 'TODO' src/                     # 遞迴搜尋目錄
grep -w 'chr1' file                     # 完整單字（不會匹配 chr10）
grep -F -f ids.txt big.tsv              # 用一個檔案中的多個固定字串搜尋（快）
zgrep 'pattern' file.gz                 # 搜尋壓縮檔

# find：依名稱、類型、時間、大小找檔案
find /path -type f -name "*.bam"        # 檔案
find /path -type d -name "results"      # 目錄
find . -name "*.log" -mtime -1          # 1 天內修改過
find . -size +1G                        # 大於 1 GB
find . -name "*.bam" -exec ls -lh {} \; # 對每個結果執行指令
find . -name "*.tsv" -print0 | xargs -0 wc -l   # 交給 xargs；-print0 / -0 處理檔名中的空白
```

正規表達式與萬用字元的差別見 [正規表達式與萬用字元](regex-wildcard.md)。

## 權限

```
-rwxr-x---  1 alice  lab  2.1K  run.sh
 │└┬┘└┬┘└┬┘
 │ │  │  └─ others：無權限
 │ │  └──── group：讀、執行
 │ └─────── owner：讀、寫、執行
 └───────── 類型：- 檔案、d 目錄、l 連結
```

| 數字 | 權限 | 常用 |
| --- | --- | --- |
| 7 | rwx | `chmod 755 script.sh`：自己可改，他人可讀可執行 |
| 6 | rw- | `chmod 644 data.tsv`：自己可改，他人唯讀 |
| 5 | r-x | — |
| 4 | r-- | `chmod 600 ~/.ssh/id_ed25519`：只有自己可讀寫（私鑰必須如此） |

```bash
chmod +x script.sh && ./script.sh      # 加上執行權限後執行
chmod -R g+rX shared/                  # 遞迴給群組讀取（X：只對目錄與已可執行檔加 x）
chown user:group file                  # 改擁有者（需權限）
```

## 程序與資源

```bash
top / htop                    # 即時程序監看（htop 需安裝）
ps aux | grep samtools        # 找特定程序
kill <PID>; kill -9 <PID>     # 結束；-9 強制
nohup ./run.sh > run.log 2>&1 &   # 背景執行，登出後繼續（更好的做法是 tmux）
jobs; fg; bg                  # 管理目前 shell 的背景工作
nproc                         # CPU 核心數
free -h                       # 記憶體
df -h                         # 各磁碟 / 掛載點的剩餘空間
du -sh *                      # 目前目錄下各項目大小
du -sh * | sort -h            # 依大小排序
```

> 長時間的工作用 [tmux](../developer-tools/tmux-and-screen.md) 而不是 `nohup`；在 HPC 上則交給排程器（[Slurm](../workflow-engines/README.md)），不要在登入節點跑重運算。

## 使用者與群組（需 sudo）

```bash
whoami; id                         # 目前使用者、所屬群組
sudo useradd -m username           # -m 建立家目錄
sudo passwd username
sudo usermod -aG groupname user    # 加入群組；-a 是附加，少了會覆蓋原有群組
getent group groupname             # 查群組成員（等同查看 /etc/group）
```

## 網路與下載

```bash
ping -c 4 example.com
curl -I https://example.com                 # 只看回應標頭
curl -L -O https://example.com/file.zip     # 下載，跟隨重新導向
wget -c https://example.com/big.tar.gz      # -c：斷線後續傳
```

遠端登入與傳檔見 [SSH](../developer-tools/ssh.md)、[rsync](../developer-tools/rsync.md)；壓縮與解壓見 [壓縮與封存](../developer-tools/archiving.md)。

## 套件管理

| 發行版 | 指令 |
| --- | --- |
| Debian / Ubuntu | `sudo apt update && sudo apt install <pkg>` |
| RHEL / Rocky / CentOS | `sudo dnf install <pkg>` |
| macOS | `brew install <pkg>` |
| 沒有 sudo（HPC、共用伺服器） | [conda / mamba](../containers-and-env/conda.md)（bioconda）、`module load <tool>`（環境模組） |

## Shell 操作技巧

| 按鍵 / 指令 | 作用 |
| --- | --- |
| `Tab` | 自動補完路徑與指令 |
| `Ctrl + C` | 中斷目前指令 |
| `Ctrl + L` | 清除畫面（同 `clear`） |
| `Ctrl + R` | 反向搜尋歷史指令 |
| `Ctrl + A` / `Ctrl + E` | 游標移到行首 / 行尾 |
| `history \| tail` | 最近的指令 |
| `!2010` | 重新執行歷史第 2010 號指令 |
| `!!` / `sudo !!` | 重複上一個指令 / 以 sudo 重跑 |
| `man <cmd>`、`<cmd> --help` | 說明文件 |
| `which <cmd>`、`type <cmd>` | 指令實際位置 |
