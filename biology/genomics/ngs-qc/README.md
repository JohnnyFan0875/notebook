[Biology](../../README.md) › [基因體學](../README.md) › NGS 品質指標

# NGS 品質指標 (NGS QC Metrics)

定序資料能不能用、結果能信多少，靠這些指標判斷。依流程順序：FASTQ 的鹼基品質 → 比對品質 → 重複率 → 深度、覆蓋度與均勻度 → GC 偏差 → 變異品質。

## 建議順序

```
鹼基品質 (FASTQ) → 比對品質 MAPQ (BAM) → 重複率 → 深度 / 覆蓋度 → 均勻度 → GC 偏差 → 變異過濾 (VCF)
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [鹼基品質分數](base-quality-scores.md) | Phred、ASCII 編碼、Q30、品質分箱 | 這個鹼基讀錯的機率多大？ |
| [比對品質](mapping-quality.md) | MAPQ 定義、各比對器的數值意義、過濾閾值 | 這條 read 放對位置了嗎？ |
| [重複率](duplication-rate.md) | PCR / 光學重複、library complexity、各實驗類型的合理範圍 | 有效的獨立 reads 有多少？ |
| [定序深度與覆蓋度](sequencing-depth-coverage.md) | 深度 vs 覆蓋度、需要多少 reads、各應用的建議深度 | 夠不夠深？有沒有漏掉的區域？ |
| [均勻度](uniformity.md) | fold-80、≥0.2× mean 比例 | 深度是不是平均分布？ |
| [GC 偏差](gc-bias.md) | 成因、指標、對 CNV 與表現量的影響 | 高 / 低 GC 區域是否被低估？ |
| [VQSR vs 硬過濾](vqsr.md) | 變異品質過濾的兩種策略 | 哪些變異呼叫是真的？ |

## 指標速查

| 階段 | 指標 | 工具 | 常見合格標準（依實驗而異） |
| --- | --- | --- | --- |
| FASTQ | % ≥ Q30 | FastQC、fastp | > 80%（Illumina 短讀） |
| BAM | 比對率 | `samtools flagstat` | WGS / WES > 95%；RNA-seq 唯一比對 > 70% |
| BAM | 重複率 | Picard、`samtools markdup` | 見 [重複率](duplication-rate.md) |
| BAM | 平均深度、≥ X× 比例 | mosdepth、Picard `CollectHsMetrics` | 見 [深度](sequencing-depth-coverage.md) |
| BAM | fold-80 base penalty | Picard `CollectHsMetrics` | < 2（capture panel / WES） |
| BAM | on-target 比例 | Picard `CollectHsMetrics` | capture > 60–70%、amplicon > 90% |
| BAM | GC dropout | Picard `CollectGcBiasMetrics` | AT / GC dropout 越接近 0 越好 |
| BAM | 插入片段長度 | Picard `CollectInsertSizeMetrics` | 與 library 製備預期相符 |
| VCF | Ts/Tv | `bcftools stats` | WGS ≈ 2.0–2.1、WES ≈ 2.8–3.3；明顯偏低代表偽陽性多 |
| VCF | 已知變異比例 | 對照 dbSNP | germline > 95% 在 dbSNP 中 |

工具用法見 [NGS 工具](../../bioinformatics-tools/ngs-tools/README.md)；多樣本彙整用 MultiQC。
