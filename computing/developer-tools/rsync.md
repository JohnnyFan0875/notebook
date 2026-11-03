[Computing](../README.md) › [開發者工具](README.md) › rsync

# rsync

`rsync` 同步兩個位置的檔案，只傳送有差異的部分：第一次傳完整資料，之後只傳新增或修改的檔案，中斷後可以接續。適用本機備份、本機 ↔ 伺服器、伺服器 ↔ 伺服器（透過 [SSH](ssh.md)）。傳大量定序資料時比 `scp` 可靠得多。

## 基本用法

```bash
rsync [選項] <來源> <目的地>

rsync -avh results/ /backup/results/                         # 本機
rsync -avhP data/ user@server:/project/data/                  # 上傳到遠端
rsync -avhP user@server:/project/results/ ./results/          # 從遠端下載
rsync -avhP -e "ssh -p 2222" data/ user@server:/data/         # 指定 SSH port
rsync -avhP data/ hpc:/scratch/data/                          # 使用 ~/.ssh/config 的別名
```

| 選項 | 意義 |
| --- | --- |
| `-a` | 封存模式：遞迴、保留權限、時間戳記、符號連結 |
| `-v` | 顯示傳輸的檔案 |
| `-h` | 大小以 K / M / G 顯示 |
| `-P` | `--partial --progress`：顯示進度，中斷後保留已傳的部分，下次接續 |
| `-z` | 傳輸時壓縮（對已壓縮的 `.gz`、`.bam` 沒用，反而耗 CPU） |
| `-n` / `--dry-run` | 只列出會做什麼，不實際執行 |
| `--delete` | 刪除目的地有、來源沒有的檔案（鏡像） |
| `--exclude='*.tmp'`、`--include` | 篩選 |
| `--checksum` / `-c` | 以內容的 checksum 判斷差異（預設比較大小與修改時間；較慢） |
| `--remove-source-files` | 傳完後刪除來源檔（搬移） |
| `--bwlimit=50M` | 限制頻寬 |

## 結尾斜線

來源路徑**有沒有結尾斜線**決定傳的是「目錄本身」還是「目錄內容」：

```
rsync -avh src  dest/          rsync -avh src/ dest/
dest/                          dest/
└── src/                       ├── file1.txt
    ├── file1.txt              └── file2.txt
    └── file2.txt
```

> 不確定時先加 `-n` 看結果。`--delete` 搭配寫錯的路徑可能刪掉整個目的地，務必先 dry run。

## 常見情境

```bash
# 1. 傳定序資料到 HPC，傳完驗證
rsync -avhP fastq/ hpc:/project/raw/fastq/
ssh hpc 'cd /project/raw/fastq && md5sum -c md5sum.txt'

# 2. 只下載結果，排除大型中間檔
rsync -avhP --exclude='*.bam' --exclude='work/' hpc:/project/results/ ./results/

# 3. 鏡像備份（先 dry run 確認要刪什麼）
rsync -avhn --delete /data/project/ /backup/project/
rsync -avh  --delete /data/project/ /backup/project/

# 4. 長時間傳輸：放在 tmux 裡，斷線不影響
tmux new -s transfer
```

| 工具 | 何時用 |
| --- | --- |
| `rsync` | 大量檔案、可能中斷、會重複同步 |
| `scp` | 單一小檔、一次性 |
| `sftp` / FileZilla / WinSCP | 圖形介面、瀏覽遠端目錄 |
| `aws s3 sync`、`gsutil rsync`、`azcopy sync` | 雲端物件儲存（見 [Cloud](../cloud/README.md)） |
| Globus、Aspera | 機構之間 TB 級傳輸 |

> 傳完用 [檢查碼](checksums.md) 驗證；長時間傳輸在 [tmux](tmux-and-screen.md) 中執行。
