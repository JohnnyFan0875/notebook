[生資工具](../README.md) › [NGS 工具](README.md) › sambamba

# sambamba

多執行緒的 BAM 處理工具，功能與 [samtools](samtools.md) 重疊（排序、索引、篩選、標記重複），最常用的是 `depth`：深度計算可附**各鹼基計數**，並預設排除低品質與重複 reads。

## 指令速查

| 想做 | 指令 |
| --- | --- |
| 排序 / 索引 | `sambamba sort -t 8 -o sorted.bam in.bam`、`sambamba index sorted.bam` |
| 標記重複 | `sambamba markdup -t 8 sorted.bam dedup.bam`（`-r` 移除） |
| 篩選 | `sambamba view -F "mapping_quality >= 20 and not duplicate" -f bam -o out.bam in.bam` |
| 每個鹼基的深度 | `sambamba depth base -L regions.bed in.bam` |
| 每個區域的平均深度 | `sambamba depth region -L regions.bed -T 20 -T 100 in.bam` |
| 固定視窗深度 | `sambamba depth window -w 1000 in.bam` |

## 每個鹼基的深度

```bash
# VCF 位置 chr7:150652580（1-based）= BED 的 chr7  150652579  150652580
sambamba depth base -L chr7:150652580-150652581 -c 0 -q 20 sample.bam
sambamba depth base -L targets.bed -c 0 -q 20 -m sample.bam
```

```text
REF   POS        COV  A  C  G   T   DEL  REFSKIP  SAMPLE
chr7  150652579  21   0  0  0   21  0    0        sample
chr7  150652580  22   0  0  22  0   0    0        sample
```

| 參數 / 欄位 | 意義 |
| --- | --- |
| `-L` | BED 檔或單一區域 `chr:beg-end` |
| `-c` | 輸出的最低深度（base 模式預設 1，`-c 0` 連 0 深度也輸出） |
| `-q` | 不計入鹼基品質低於此值的鹼基 |
| `-F` | 自訂 read 篩選；預設 `mapping_quality > 0 and not duplicate and not failed_quality_control` |
| `-m` | 成對 reads 重疊時逐鹼基處理，避免同一片段算兩次 |
| `-T`（region） | 輸出達到該深度的鹼基比例，例如 `-T 20` → 「≥20× 的比例」 |
| `POS` | **0-based** 座標（與 samtools depth 的 1-based 不同） |
| `A/C/G/T`、`DEL` | 各鹼基與缺失的計數，可直接估算 VAF（例：ALT 數 ÷ COV） |
| `REFSKIP` | 跨越該位置的剪接（RNA-seq 的 `N` CIGAR） |

> 上例的 `POS` 是 0-based：`150652579` 對應 1-based 的 150652580。與 VCF 對照時要加 1，見 [座標系統](../../genomics/file-formats/zero-one-based.md)。

## sambamba vs samtools depth

| | sambamba depth | samtools depth |
| --- | --- | --- |
| 預設排除重複 / MAPQ 0 | 是 | 否（需自行過濾） |
| 鹼基組成 | 有 | 無 |
| 區域摘要（≥X× 比例） | `depth region -T` | 需另外計算（或用 `samtools coverage`、mosdepth） |
| 座標 | 0-based | 1-based |

兩者預設的過濾條件不同，**同一個 BAM 算出的深度可能不一樣**；報告時要寫明工具與參數。官方：[sambamba GitHub](https://github.com/biod/sambamba)。
