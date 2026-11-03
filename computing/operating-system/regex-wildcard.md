[Computing](../README.md) › [作業系統](README.md) › 正規表達式與萬用字元

# 正規表達式與萬用字元 (Regex and Wildcards)

兩者都用特殊符號描述「一群字串」，但由不同的程式解讀、用在不同地方：**萬用字元 (wildcard / glob)** 由 shell 展開成檔名；**正規表達式 (regular expression, regex)** 由 `grep`、`sed`、`awk`、Python 等工具用來比對檔案內容。Python / R 的 regex 寫法見 [文字清理與正規表達式](../../data-science/python-foundations/text-cleaning-and-regex.md)、[R 正規表達式](../../data-science/r-foundations/regular-expressions.md)。

| | 萬用字元 (globbing) | 正規表達式 (regex) |
| --- | --- | --- |
| 誰解讀 | **shell**，在指令執行前 | **工具本身**（`grep`、`sed`、`awk`） |
| 比對對象 | 檔名、路徑 | 檔案或串流中的文字 |
| 時機 | `ls *.txt` 先被展開成 `ls a.txt b.txt` 再執行 | 樣式原封不動傳給程式 |
| 「任意字元」 | `*` 任意長度、`?` 一個字元 | `.` 一個字元、`.*` 任意長度 |
| 能力 | 簡單 | 強大：錨點、重複次數、分組、或 |
| 例子 | `ls *.fastq.gz` | `grep '^ATG' genes.txt` |

> 傳給 `grep` / `find -name` 的樣式要加引號：`find . -name "*.txt"`。不加引號時 shell 會先把 `*.txt` 展開成目前目錄的檔名，結果出乎意料。

## 萬用字元

| 符號 | 意義 | 例子 |
| --- | --- | --- |
| `*` | 零或多個任意字元 | `*.bam` |
| `?` | 剛好一個字元 | `file?.txt` 符合 `file1.txt`、`fileA.txt`，不符合 `file10.txt` |
| `[abc]`、`[0-9]` | 括號中的任一字元 | `sample[1-3].vcf` |
| `[!abc]` | 不在括號中的字元 | `[!_]*` |
| `{a,b}` | 大括號展開（產生字串，不檢查檔案是否存在） | `cp file.{txt,bak}` → `cp file.txt file.bak` |
| `{1..10}` | 數列展開 | `mkdir run{1..10}`；`{01..10}` 補零 |
| `**` | 遞迴所有子目錄（bash 需 `shopt -s globstar`） | `ls **/*.log` |

```bash
ls *_R1.fastq.gz                    # 所有 read 1
for f in *_R1.fastq.gz; do          # 由 R1 推出 R2 的檔名
    r2=${f/_R1/_R2}
    echo "$f $r2"
done
```

## 正規表達式

| 符號 | 意義 | 例子 |
| --- | --- | --- |
| `.` | 任意一個字元 | `A.G` 符合 AAG、ACG |
| `^` / `$` | 行首 / 行尾 | `^>`：FASTA 標題行；`\.gz$` |
| `*` / `+` / `?` | 前一項 0 次以上 / 1 次以上 / 0 或 1 次 | `AT+G` |
| `{n}`、`{n,m}` | 重複 n 次 / n 到 m 次 | `[ACGT]{6}`：6-mer |
| `[ACGT]`、`[^N]` | 字元集合 / 排除 | `[^ACGTN]`：非法鹼基 |
| `a\|b` | 或 | `error\|warn` |
| `( )` | 分組、擷取 | `(chr[0-9XY]+):([0-9]+)` |
| `\` | 跳脫特殊字元 | `\.`：真正的句點 |
| `\b` | 單字邊界 | `\bchr1\b` 不符合 `chr10` |
| `\d`、`\w`、`\s` | 數字、單字字元、空白（Perl / Python / `grep -P`） | POSIX 寫法：`[0-9]`、`[[:alnum:]_]`、`[[:space:]]` |

| 方言 | 工具 | 差異 |
| --- | --- | --- |
| 基本 (BRE) | `grep`、`sed` 預設 | `+ ? \| ( ) { }` 要加反斜線才有特殊意義 |
| 延伸 (ERE) | `grep -E`、`sed -E`、`awk` | `+ ? \| ( ) { }` 直接使用；**建議預設用這個** |
| Perl 相容 (PCRE) | `grep -P`、Python `re`、R `perl = TRUE` | 支援 `\d`、`\s`、lookahead |

## 在指令中使用

```bash
# grep：搜尋
grep -E 'error|warning' run.log          # 或
grep -c '^>' seqs.fa                     # FASTA 序列數
grep -v '^#' calls.vcf | head            # 去掉 VCF 標頭
grep -E -o 'chr[0-9XY]+:[0-9]+' notes.txt   # -o：只輸出符合的部分
grep -iv -E 'conflict|error|fail' run.log   # 排除多個樣式（不分大小寫）

# sed：取代（s/樣式/取代/旗標）
sed 's/chr//' in.bed > out.bed           # 每行第一個 chr 刪除
sed -E 's/[0-9]+/N/g' file.txt           # g：全部取代
sed -E 's/^(chr[0-9]+)_([0-9]+)/\1:\2/' ids.txt   # \1 \2 引用分組：chr1_100 → chr1:100
sed -i.bak 's/old/new/g' file.txt        # 原地修改並留備份（macOS 的 sed -i 語法不同）
sed 's/\x1b\[[0-9;]*m//g' color.log      # 移除 ANSI 顏色碼（log 中的亂碼）

# awk：依欄位比對
awk '$2 ~ /^rs/' variants.tsv            # 第 2 欄以 rs 開頭
awk -F'\t' '$1 !~ /^chr(X|Y|M)$/' in.bed # 排除性染色體與粒線體

# find：-name 用萬用字元，-regex 用正規表達式（比對完整路徑）
find . -type f -name "*.txt"
find . -regextype posix-extended -regex '.*/sample[0-9]+\.vcf\.gz'
```

| 常見錯誤 | 說明 |
| --- | --- |
| `.` 忘了跳脫 | `file.txt` 也會符合 `fileXtxt`；寫 `file\.txt` |
| 沒有錨點 | `grep chr1` 也會符合 `chr10`、`chr11`；用 `-w` 或 `^chr1\b` |
| 貪婪比對 | `<.*>` 會從第一個 `<` 吃到最後一個 `>`；用 `[^>]*` 或非貪婪 `.*?`（PCRE） |
| 用 regex 解析巢狀結構 | 括號、HTML 的巢狀深度無法用正規表達式正確處理，見 [可計算性](../computer-science-foundations/computability-and-turing-machines.md) |
