[Computing](../README.md) › [作業系統](README.md) › Shell 腳本

# Shell 腳本 (Shell Scripting)

把一串命令列操作寫成可重複執行的 bash 腳本：變數、參數、條件、迴圈、函式與錯誤處理。適合串接命令列工具的「膠水」程式；步驟多、要平行與重跑時改用 [工作流引擎](../workflow-engines/README.md)，邏輯複雜時改用 Python。

## 腳本範本

```bash
#!/usr/bin/env bash
# qc.sh：對資料夾中每個樣本的 FASTQ 跑 fastp
set -euo pipefail                         # 出錯即停、未定義變數報錯、管線中任一段失敗即失敗

usage() { echo "Usage: $0 <fastq_dir> <out_dir> [threads]" >&2; exit 1; }
[[ $# -ge 2 ]] || usage

in_dir=$1
out_dir=$2
threads=${3:-4}                           # 第 3 個參數，預設 4
mkdir -p "$out_dir"

for r1 in "$in_dir"/*_R1.fastq.gz; do
    [[ -e "$r1" ]] || { echo "no FASTQ in $in_dir" >&2; exit 1; }
    sample=$(basename "$r1" _R1.fastq.gz)
    r2=${r1/_R1/_R2}
    echo "[$(date +%T)] $sample"
    fastp -i "$r1" -I "$r2" \
          -o "$out_dir/${sample}_R1.fq.gz" -O "$out_dir/${sample}_R2.fq.gz" \
          -j "$out_dir/${sample}.json" -w "$threads"
done
```

```bash
chmod +x qc.sh
./qc.sh raw/ trimmed/ 8
bash -n qc.sh          # 只檢查語法
bash -x qc.sh ...      # 印出每一行執行的指令（除錯）
shellcheck qc.sh       # 靜態檢查常見錯誤（強烈建議安裝）
```

| `set` 選項 | 作用 | 沒設時的風險 |
| --- | --- | --- |
| `-e` | 任何指令失敗就結束 | 前一步失敗，後面用不完整的檔案繼續跑 |
| `-u` | 使用未定義變數時報錯 | `rm -rf "$dir/"` 在 `dir` 未設定時變成 `rm -rf /` |
| `-o pipefail` | 管線中任一段失敗，整條管線就失敗 | `zcat broken.gz \| wc -l` 會「成功」並回傳 0 |

## 變數與引號

```bash
name="Alice"                      # = 兩邊不能有空格
echo "Hello, $name"               # 雙引號：展開變數
echo 'Hello, $name'               # 單引號：原樣輸出
echo "${name}_R1.fastq"           # 變數名後接字元時用 {} 分隔
today=$(date +%F)                 # 指令替換；比反引號 `date` 好讀、可巢狀
n=$((3 + 4))                      # 整數運算；bash 不支援小數，用 awk 或 bc
```

> **變數展開一律加雙引號**：`"$file"`。檔名有空白時，`$file` 會被拆成多個參數。

| 參數展開 | 結果（`f=/data/S1_R1.fastq.gz`） |
| --- | --- |
| `${f##*/}` | `S1_R1.fastq.gz`（去掉路徑，同 `basename`） |
| `${f%/*}` | `/data`（目錄，同 `dirname`） |
| `${f%.fastq.gz}` | `/data/S1_R1`（去掉結尾） |
| `${f/_R1/_R2}` | `/data/S1_R2.fastq.gz`（取代第一個） |
| `${var:-default}` | 未設定或空時用預設值 |
| `${#var}` | 字串長度 |

## 腳本參數

| 變數 | 意義 |
| --- | --- |
| `$0` | 腳本名稱 |
| `$1`、`$2`… | 位置參數 |
| `"$@"` | 所有參數，各自保持為獨立字串（傳遞參數時用這個） |
| `$#` | 參數個數 |
| `$?` | 上一個指令的結束狀態（0 = 成功） |
| `$$` | 目前程序的 PID |

## 陣列

```bash
samples=("S1" "S2" "S3")
echo "${samples[0]}"              # S1
echo "${samples[@]}"              # 全部
echo "${#samples[@]}"             # 3
for s in "${samples[@]}"; do echo "$s"; done

mapfile -t ids < ids.txt          # 檔案每行讀成陣列元素

declare -A ref=([hg38]=/ref/hg38.fa [mm39]=/ref/mm39.fa)   # 關聯陣列需 declare -A（bash 4+）
echo "${ref[hg38]}"
```

## 條件

```bash
if [[ -f "$file" && "$name" != "tmp" ]]; then
    echo "process"
elif [[ -d "$file" ]]; then
    echo "is a directory"
else
    echo "missing"
fi

if grep -q "ERROR" run.log; then  # 直接用指令的結束狀態當條件
    echo "error found"
fi

mkdir -p out && cd out || exit 1  # && 成功才執行；|| 失敗才執行
```

| 測試 | 意義 |
| --- | --- |
| `-f` / `-d` / `-e` | 是一般檔案 / 是目錄 / 存在 |
| `-s` | 存在且非空（檢查輸出檔是否真的有內容） |
| `-r` / `-w` / `-x` | 可讀 / 可寫 / 可執行 |
| `=` / `!=` | 字串相等 / 不等（`[[ ]]` 中也可用 `==`、樣式比對 `== *.gz`） |
| `-eq -ne -gt -lt -ge -le` | 整數比較；或用 `(( count > 10 ))` |
| `-z` / `-n` | 字串為空 / 非空 |

> `[[ ]]` 是 bash 的擴充，比 `[ ]` 安全（不會因變數為空或含空白而出錯）並支援 `&&`、`||`、`=~` 正規表達式；寫 bash 腳本時優先用它。

```bash
case "$1" in                      # 多個離散選項時比 if/elif 清楚
    start) echo "Starting" ;;
    stop)  echo "Stopping" ;;
    *.gz)  echo "gzip file" ;;    # 可用萬用字元
    *)     echo "Usage: $0 {start|stop}" ;;
esac
```

## 迴圈

```bash
for i in {1..5}; do echo "$i"; done
for f in ./*.csv; do
    [[ -e "$f" ]] || continue     # 沒有符合的檔案時，樣式本身會被當成字串
    echo "$f"
done

while IFS= read -r line; do       # 逐行讀檔：IFS= 保留前後空白，-r 不解讀反斜線
    echo "Line: $line"
done < samples.txt

while IFS=$'\t' read -r sample r1 r2; do   # 讀 TSV 的多個欄位
    echo "$sample: $r1 $r2"
done < sheet.tsv

count=1
until (( count > 5 )); do (( count++ )); done
```

> 用萬用字元走訪檔案，**不要解析 `ls` 的輸出**（`for f in $(ls)` 遇到空白檔名就壞）。

## 函式

```bash
log() { echo "[$(date +%F' '%T)] $*" >&2; }   # 訊息寫到 stderr，不污染 stdout 的資料

count_reads() {
    local fq=$1                    # local：避免污染全域變數
    echo $(( $(zcat "$fq" | wc -l) / 4 ))
}

n=$(count_reads S1_R1.fastq.gz)    # 函式的「回傳值」是它輸出到 stdout 的內容
log "S1 has $n reads"
```

## 錯誤處理與清理

```bash
tmp=$(mktemp -d)                         # 安全的暫存目錄
trap 'rm -rf "$tmp"' EXIT                # 不論成功或失敗，結束時都清理

if ! samtools index "$bam"; then         # 處理特定指令的失敗
    log "index failed for $bam"
    exit 2
fi

cmd > out.txt 2> err.log                 # stdout、stderr 分開寫入
cmd > all.log 2>&1                       # 合併寫入同一檔
```

## 平行執行

```bash
# xargs -P：同時跑 4 個
ls *.bam | xargs -P 4 -I{} samtools index {}

# GNU parallel：更多功能（需安裝）
parallel -j 8 'fastqc {} -o qc/' ::: *.fastq.gz
```

> 在 HPC 上不要用 `xargs -P` 在登入節點平行跑重運算；用 Slurm array job 或工作流引擎分派到計算節點。

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 開頭 `set -euo pipefail` | 出錯就停，不默默產出錯誤結果 |
| 變數加雙引號 | 檔名空白、空變數 |
| 用 `shellcheck` 檢查 | 抓出大多數常見錯誤 |
| 訊息寫 stderr，資料寫 stdout | 管線可以安全串接 |
| 輸出先寫暫存檔，成功後再 `mv` | 中斷時不留下看似完整的半成品 |
| 腳本超過約 100 行、需要資料結構或測試 | 改寫成 Python |
