[Computing](../README.md) › [作業系統](README.md) › 命令列資料處理

# 命令列資料處理 (Command-Line Data Processing)

Shell 擅長檔案導向、可重複的輕量資料工作：下載、檢視、篩選、切欄、排序、計數、合併。它不取代 Python / R / SQL，但常是最快的膠水層；對 GB 等級的 TSV、BED、VCF 文字檔，串流處理的命令列工具往往比載入 pandas 更省記憶體。基本指令見 [Linux 基礎](linux-basics.md)。

## 工具一覽

| 工具 | 作用 | 常用選項 |
| --- | --- | --- |
| `cut` | 取欄 | `-f 1,3`（預設 tab 分隔）、`-d ','` |
| `sort` | 排序 | `-k2,2n`（第 2 欄數值）、`-t$'\t'`、`-u`、`-V`（自然排序：chr2 < chr10） |
| `uniq` | 合併**相鄰**重複行 | `-c` 計數、`-d` 只列重複；前面通常要先 `sort` |
| `wc` | 計數 | `-l` 行數 |
| `grep` | 依樣式篩選行 | 見 [正規表達式](regex-wildcard.md) |
| `awk` | 依欄位條件篩選、計算、重組 | `-F'\t'`、`-v OFS='\t'` |
| `sed` | 串流取代 | `s/old/new/g` |
| `paste` | 並排合併檔案 | `paste a.txt b.txt` |
| `join` | 依共同欄位合併兩個**已排序**檔案 | `-t$'\t' -1 1 -2 1` |
| `comm` | 比較兩個已排序清單的交集 / 差集 | `-12` 交集、`-23` 只在第一個 |
| `tr` | 字元替換 / 刪除 | `tr ',' '\t'`、`tr -d '\r'` |
| `column` | 對齊顯示 | `column -t -s$'\t'` |
| `shuf` | 隨機抽樣 | `shuf -n 1000` |

## 常用模式

```bash
# 1. 某欄的值分布（類別計數，由多到少）
cut -f 3 samples.tsv | tail -n +2 | sort | uniq -c | sort -k1,1nr

# 2. 依條件篩選並統計：第 3 欄 > 20 的列數與比例（跳過標題）
awk -F'\t' 'NR > 1 { m++; if ($3 > 20) n++ } END { print n, m, n/m }' coverage.tsv

# 3. 依欄位加總（group by）
awk -F'\t' 'NR > 1 { sum[$1] += $4 } END { for (k in sum) print k, sum[k] }' reads.tsv

# 4. 重新排列欄位、輸出 tab 分隔
awk -F',' -v OFS='\t' '{ print $2, $1, $5 }' data.csv > data.tsv

# 5. 兩個 ID 清單的交集 / 差集
comm -12 <(sort a.txt) <(sort b.txt)       # 兩邊都有
comm -23 <(sort a.txt) <(sort b.txt)       # 只在 a

# 6. 依 ID 合併兩個表（類似 SQL JOIN）
join -t$'\t' <(sort -k1,1 a.tsv) <(sort -k1,1 b.tsv) > merged.tsv

# 7. 大檔排序：限制記憶體、平行、暫存目錄
sort -t$'\t' -k1,1V -k2,2n -S 4G --parallel=8 -T /scratch/tmp big.bed > big.sorted.bed

# 8. Windows 換行造成欄位末端多了 \r
tr -d '\r' < win.csv > unix.csv
```

> `<(...)` 是程序替換 (process substitution)：把指令輸出當成檔案傳入，不必建立暫存檔。

### 生資檔案範例

```bash
zcat reads.fastq.gz | awk 'NR % 4 == 2 { n++; len += length($0) } END { print n, len/n }'   # read 數與平均長度
grep -c '^>' proteins.fa                                         # FASTA 序列數
zgrep -v '^#' calls.vcf.gz | cut -f 1 | uniq -c                  # 每條染色體的變異數（VCF 已依座標排序）
zgrep -v '^#' calls.vcf.gz | awk -F'\t' '$7 == "PASS"' | wc -l   # 通過過濾的變異數
awk -F'\t' '{ s += $3 - $2 } END { print s }' targets.bed        # BED 區間總長度（0-based 半開區間）
cut -f 1 targets.bed | sort -V | uniq                            # 涵蓋哪些染色體
```

專門工具通常更快也更正確：VCF 用 [bcftools](../../biology/bioinformatics-tools/ngs-tools/bcftools.md)、BED 區間運算用 [bedtools](../../biology/bioinformatics-tools/ngs-tools/bedtools.md)、BAM 用 [samtools](../../biology/bioinformatics-tools/ngs-tools/samtools.md)。

## 下載

```bash
curl -L -O https://example.org/data.csv           # -O：保留遠端檔名；-L：跟隨重新導向
curl -L -o data.csv "https://example.org/dl?id=123"   # -o：指定檔名；URL 有 ? & 時加引號
curl -fsSL url | head                             # -f：HTTP 錯誤時失敗；-sS：安靜但顯示錯誤
wget -c https://example.org/big.tar.gz            # -c：續傳
wget -i urls.txt                                  # 一次下載清單中的所有網址
```

下載後務必核對 [檢查碼](../developer-tools/checksums.md)；大量或遠端到遠端的傳輸用 [rsync](../developer-tools/rsync.md)。

## CSV 與 JSON 工具

純文字工具不懂 CSV 的引號（`"Smith, John"` 會被 `cut -d,` 切成兩欄），處理真正的 CSV 用專門工具：

| 工具 | 用途 | 例子 |
| --- | --- | --- |
| `csvkit`（`uv tool install csvkit`） | 檢視、取欄、篩選、統計、SQL | `csvlook`、`csvcut -c id,score`、`csvgrep -c artist -m Adele`、`csvstat` |
| DuckDB CLI | 直接用 SQL 查 CSV / Parquet，速度快、可處理大檔 | `duckdb -c "SELECT artist, count(*) FROM 'songs.csv' GROUP BY 1"` |
| `jq` | JSON 篩選與轉換 | `curl -s api \| jq '.results[] \| .id'` |
| `xsv` / `qsv`、`mlr`（Miller） | 高效能 CSV 處理 | `mlr --icsv --opprint sort -nr score data.csv` |

```bash
csvsql --query "select artist, count(*) as n from songs group by artist" songs.csv
duckdb -c "COPY (SELECT * FROM 'big.csv' WHERE score > 0.9) TO 'filtered.parquet'"
```

DuckDB 與 Parquet 的完整介紹見 [DuckDB 與 Parquet](../../data-science/databases/duckdb-and-parquet.md)。資料需要複雜 join、索引、反覆查詢時，改放資料庫。

## 排程：cron

```bash
crontab -e                    # 編輯目前使用者的排程
crontab -l                    # 列出

# 分 時 日 月 星期  指令
  0   2  *  *  *     /home/me/bin/backup.sh >> /home/me/logs/backup.log 2>&1   # 每天 02:00
  */15 * *  *  1-5   /home/me/bin/check.sh                                      # 平日每 15 分鐘
```

| 注意 | 說明 |
| --- | --- |
| 環境變數很少 | cron 不會載入你的 `.bashrc`；腳本中用絕對路徑、自己設定 `PATH` 與 conda 環境 |
| 輸出要導向 log | 否則錯誤訊息會消失（或寄到本機信箱） |
| 適合 | 定期、非互動、穩定的工作；有依賴關係的流程用 [Airflow](../workflow-engines/airflow.md) |
| HPC | 通常不允許使用者 cron；改用排程器 |

## 何時離開 shell

| 訊號 | 改用 |
| --- | --- |
| 邏輯有很多狀態、巢狀條件 | Python / R |
| 需要 join 多張表、反覆查詢 | DuckDB、SQL |
| 需要測試、長期維護 | Python 腳本 + [測試](../../data-science/python-foundations/testing.md) |
| 多步驟、要平行、要能從中斷處重跑 | [工作流引擎](../workflow-engines/README.md) |
