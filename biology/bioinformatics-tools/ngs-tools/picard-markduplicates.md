[生資工具](../README.md) › [NGS 工具](README.md) › Picard MarkDuplicates

# Picard MarkDuplicates

找出比對位置與方向完全相同、推測來自同一個原始 DNA 片段的 reads（PCR 重複或光學重複），在 FLAG 加上 `0x400`。預設**只標記不刪除**，下游工具（GATK、`samtools view -F 0x400`）再決定是否忽略。

## 用法

```bash
picard MarkDuplicates \
  -I sorted.bam \
  -O dedup.bam \
  -M dup_metrics.txt \
  --CREATE_INDEX true \
  --OPTICAL_DUPLICATE_PIXEL_DISTANCE 2500     # 圖案化 flow cell（NovaSeq / HiSeq X）建議值；預設 100
# 同一工具也可用 gatk MarkDuplicates 執行
# 舊語法 I=sorted.bam O=dedup.bam M=metrics.txt 已列為 legacy
```

| 參數 | 意義 |
| --- | --- |
| `-I` / `-O` / `-M` | 輸入 BAM（需依座標排序）/ 輸出 BAM / 指標檔 |
| `--REMOVE_DUPLICATES true` | 直接刪除重複（通常不建議，保留標記較有彈性） |
| `--OPTICAL_DUPLICATE_PIXEL_DISTANCE` | 判定光學重複的像素距離 |
| `--CREATE_INDEX true` | 輸出時建 `.bai` |
| `--ASSUME_SORT_ORDER coordinate` | header 未標排序狀態但實際已排序時使用 |

## 讀指標檔

| 欄位 | 意義 |
| --- | --- |
| `READ_PAIR_DUPLICATES` | 被標記為重複的 read pair 數 |
| `READ_PAIR_OPTICAL_DUPLICATES` | 其中屬於光學重複的數量 |
| `PERCENT_DUPLICATION` | 重複比例（0–1，不是百分比） |
| `ESTIMATED_LIBRARY_SIZE` | 估計 library 中不重複片段的數量（library complexity） |

重複率的合理範圍與成因見 [重複率](../../genomics/ngs-qc/duplication-rate.md)。

## 什麼時候不要（或要特別處理）去重複

| 情境 | 做法 |
| --- | --- |
| 擴增子 (amplicon) panel | 所有 reads 起點相同，去重複會把真實 reads 幾乎刪光；**不要做** |
| 有 UMI 的 library | 依 UMI 分組再判斷（fgbio、`umi_tools dedup`、Picard `UmiAwareMarkDuplicatesWithMateCigar`） |
| RNA-seq 差異表現 | 高表現基因的「重複」多半是真的；通常不去重複，只拿重複率當 QC 參考 |
| WGS / WES 變異呼叫 | 標準流程，必做 |
| cfDNA 低頻變異 | 用 UMI 建一致序列 (consensus)，不只是標記 |

## 替代工具

| 工具 | 特點 |
| --- | --- |
| `samtools markdup` | 需先 `collate` → `fixmate -m` → `sort`，見 [samtools](samtools.md#重複標記samtools-版本) |
| `sambamba markdup` | 多執行緒、快，見 [sambamba](sambamba.md) |
| GATK `MarkDuplicatesSpark` | 可吃 queryname 排序的 BAM，平行化 |

官方文件：[GATK / Picard MarkDuplicates](https://gatk.broadinstitute.org/hc/en-us/articles/360037052812-MarkDuplicates-Picard)。
