[Computing](../README.md) › [開發者工具](README.md) › 檢查碼

# 檢查碼：MD5 與 SHA-256 (Checksums)

雜湊函數 (hash function) 把任意大小的檔案轉成固定長度的字串；檔案只要差一個位元組，雜湊值就完全不同。比對下載前後的雜湊值，就能確認檔案在傳輸或儲存中沒有損壞。定序公司交付 FASTQ、公開資料庫（ENA、GEO、Ensembl）提供下載時，通常附上 `md5sum.txt` 或 `CHECKSUMS` 檔。

| 演算法 | 長度 | 安全性 | 用途 |
| --- | --- | --- | --- |
| MD5 | 128 位元（32 個 hex 字元） | **不安全**：可刻意製造碰撞 | 檢查意外損壞（傳輸、磁碟）；生資資料交付仍最常見 |
| SHA-1 | 160 位元 | 弱，已淘汰 | Git 物件 ID（逐步改用 SHA-256） |
| SHA-256 | 256 位元（64 個 hex 字元） | 強 | 軟體發佈、需防竄改的完整性驗證 |
| SHA-512 | 512 位元 | 強 | 更高安全需求 |
| BLAKE2 / BLAKE3 | 可變 | 強，且比 SHA-2 快 | 大量檔案的快速雜湊 |

> 只是檢查傳輸是否損壞，MD5 就夠；要防範**有人刻意竄改**（下載軟體、安裝檔），用 SHA-256 並從可信管道取得雜湊值。

## 產生與驗證

```bash
# Linux / WSL / macOS（macOS 另有 md5、shasum -a 256）
md5sum sample_R1.fastq.gz
# d41d8cd98f00b204e9800998ecf8427e  sample_R1.fastq.gz   ← 這個值是空檔案的 MD5，看到它代表檔案是空的

md5sum *.fastq.gz > md5sum.txt          # 為多個檔案建立檢查碼清單
md5sum -c md5sum.txt                    # 驗證：每行 OK / FAILED
md5sum -c --quiet md5sum.txt            # 只顯示失敗的

sha256sum installer.tar.gz
sha256sum -c SHA256SUMS --ignore-missing   # 只驗證清單中存在於本機的檔案
```

```powershell
# Windows PowerShell
Get-FileHash .\sample_R1.fastq.gz -Algorithm MD5
Get-FileHash .\installer.exe            # 預設 SHA256
```

| 輸出 | 意義 |
| --- | --- |
| `sample_R1.fastq.gz: OK` | 一致 |
| `sample_R1.fastq.gz: FAILED` | 不一致：重新下載 |
| `No such file or directory` | 清單中的路徑與本機不同（清單通常用相對路徑，在檔案所在目錄執行） |

## 實務守則

| 守則 | 說明 |
| --- | --- |
| 收到資料第一件事就驗證 | 定序資料交付、`rsync` / `scp` 傳完、從雲端下載後 |
| 清單和資料一起保存 | 之後搬移、備份時可再驗證 |
| 大檔平行計算 | `ls *.fastq.gz \| xargs -P 8 -n 1 md5sum > md5sum.txt` |
| Windows 產生的清單 | 可能是 CRLF 換行或大寫 hex；先 `dos2unix`，比對時統一大小寫 |
| 雜湊值相同 ≠ 內容正確 | 只代表與來源一致；來源本身截斷或錯誤時仍需 QC（`gzip -t`、FastQC） |

傳輸工具 [rsync](rsync.md) 本身用 checksum 判斷差異，可加 `--checksum` 強制逐檔比對內容。雜湊表的資料結構原理見 [非線性資料結構](../computer-science-foundations/non-linear-data-structures.md#雜湊表-hash-table)。
