[生資工具](../README.md) › [NGS 工具](README.md) › samtools

# samtools

處理 SAM / BAM / CRAM 比對檔的標準工具：排序、索引、篩選、統計、計算深度。格式說明見 [BAM](../../genomics/file-formats/bam.md)。

## 指令速查

| 想做 | 指令 |
| --- | --- |
| 依座標排序 | `samtools sort -@ 8 -o sorted.bam in.bam` |
| 建索引（`.bai`） | `samtools index sorted.bam` |
| 每條染色體的 reads 數 | `samtools idxstats sorted.bam` |
| 快速比對摘要 | `samtools flagstat sorted.bam` |
| 完整統計 + 圖 | `samtools stats sorted.bam > s.stats && plot-bamstats -p plots/ s.stats` |
| 取某區域（需索引） | `samtools view -b -o sub.bam sorted.bam chr12:25200000-25300000` |
| 依 BED 取區域 | `samtools view -b -L targets.bed -o sub.bam sorted.bam` |
| 過濾低 MAPQ、未比對、次要比對 | `samtools view -b -q 20 -F 0x904 -o filt.bam sorted.bam` |
| BAM → SAM（含 header） | `samtools view -h -o out.sam in.bam` |
| BAM → FASTQ | `samtools fastq -1 R1.fq.gz -2 R2.fq.gz -n in.bam`（先 `samtools collate`） |
| BAM ↔ CRAM | `samtools view -C -T ref.fa -o out.cram in.bam` |
| 每個區域的深度總和 | `samtools bedcov regions.bed sorted.bam` |
| 每個鹼基的深度 | `samtools depth -a -b regions.bed sorted.bam` |
| 每條染色體的覆蓋率摘要 | `samtools coverage sorted.bam` |
| 參考序列索引、取序列 | `samtools faidx ref.fa`、`samtools faidx ref.fa chr1:100-200` |
| 標記重複 | 見下方 `markdup` 流程 |

| 常用參數 | 意義 |
| --- | --- |
| `-@ N` | 額外執行緒數 |
| `-b` / `-C` / `-h` | 輸出 BAM / 輸出 CRAM / 輸出含 header |
| `-q INT` | 最低 MAPQ（見 [Mapping Quality](../../genomics/ngs-qc/mapping-quality.md)） |
| `-f` / `-F FLAG` | 只留 / 排除含該 FLAG 的 reads；FLAG 意義可查 [Explain SAM Flags](https://broadinstitute.github.io/picard/explain-flags.html) |
| `-a`（depth） | 連深度為 0 的位置也輸出；否則 0 深度位置被略過，平均深度會高估 |

## 重複標記（samtools 版本）

```bash
samtools collate -@ 8 -O -u in.bam \
  | samtools fixmate -m -u - - \
  | samtools sort -@ 8 -u - \
  | samtools markdup -@ 8 -f dup_stats.txt - dedup.bam   # -r 直接移除重複
samtools index dedup.bam
```

`fixmate -m` 補上 mate score，`markdup` 才能判斷重複；也可以改用 [Picard MarkDuplicates](picard-markduplicates.md)。

## 讀懂 `flagstat`

```text
363458 + 0 in total (QC-passed reads + QC-failed reads)
363458 + 0 primary
     0 + 0 secondary
     0 + 0 supplementary
     0 + 0 duplicates
362756 + 0 mapped (99.81% : N/A)
362756 + 0 primary mapped (99.81% : N/A)
     0 + 0 paired in sequencing
     0 + 0 properly paired (N/A : N/A)
     0 + 0 singletons (N/A : N/A)
     0 + 0 with mate mapped to a different chr
```

| 欄位 | 意義 | 判讀 |
| --- | --- | --- |
| `+` 前 / 後 | 通過 / 未通過 QC 的 reads | 後者通常是 0 |
| primary | 每條輸入 read 的主要比對 | ≈ 輸入 reads 數 |
| secondary | multi-mapper 的其他候選位置 | STAR / HISAT2 會輸出；BWA 預設不輸出 |
| supplementary | 嵌合比對（chimeric）的其他片段 | 融合基因、結構變異的線索 |
| duplicates | 被標記為重複的 reads | 比對器不會標，要先跑 markdup |
| mapped | 比對到的 reads（**含 supplementary**） | 比對率看 primary mapped 較準 |
| properly paired | 兩端方向與距離都合理 | 最保守的「好 reads」數 |
| singletons | 自己有比對、mate 沒有 | 偏高時檢查 adapter / 污染 |
| mate mapped to a different chr | 兩端在不同染色體 | 少量正常；過多可能是嵌合 library 或易位 |

上例是單端資料（paired 為 0），primary mapped 99.81% 屬正常。解讀參考：[Biostars](https://www.biostars.org/p/268550/)。

## 深度輸出

```text
# samtools bedcov：BED 欄位 + 該區域所有鹼基深度的「總和」（不是 reads 數）
chr12   25378547   25378707   KRAS   1   709757     # ÷ 160 bp ≈ 平均深度 4436×

# samtools depth：每個位置一列（1-based）
chr12   25378548   4909
```

平均深度 = `bedcov` 總和 ÷ 區域長度。要附鹼基組成（A/C/G/T 計數）用 [sambamba depth base](sambamba.md#每個鹼基的深度)；大量樣本求速度可用 mosdepth。深度與均勻度的指標見 [定序深度與覆蓋度](../../genomics/ngs-qc/sequencing-depth-coverage.md)。

## 常見錯誤

| 錯誤 | 原因 / 修正 |
| --- | --- |
| `view` 取區域報錯 | 沒有 `.bai`，或 BAM 未排序；先 `sort` 再 `index` |
| 區域查不到 reads | 染色體名稱不同（`chr12` vs `12`）；用 `samtools view -H in.bam \| grep @SQ` 確認 |
| `flagstat` 的 mapped 比例看起來偏高 | 包含 supplementary；看 primary mapped |
| `depth` 平均深度偏高 | 沒加 `-a`，0 深度位置被略過 |
| `samtools flagstats` 找不到指令 | 正確名稱是 `flagstat`（無 s） |
