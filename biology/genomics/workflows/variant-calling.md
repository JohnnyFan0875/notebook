[基因體學](../README.md) › [分析流程](README.md) › 變異呼叫

# 變異呼叫流程 (Variant Calling)

從比對好的 reads 找出樣本與參考基因組的差異（SNV、indel），輸出 [VCF](../file-formats/vcf.md)。germline（遺傳性，所有細胞都有）與 somatic（腫瘤後天獲得，只在部分細胞）的假設不同，流程也不同。

## Germline 流程（GATK Best Practices）

```
FASTQ ──BWA-MEM──► BAM ──MarkDuplicates──► BQSR ──HaplotypeCaller（-ERC GVCF）──► gVCF（每個樣本）
   ──GenomicsDBImport + GenotypeGVCFs（多樣本聯合基因分型）──► VCF
   ──VQSR 或硬過濾──► 過濾後 VCF ──bcftools norm──► VEP / ANNOVAR 註解 ──► 判讀
```

```bash
# 1. 比對（-R 寫入 read group，GATK 必需）
bwa mem -t 16 -R '@RG\tID:S1.L1\tSM:S1\tPL:ILLUMINA\tLB:lib1' GRCh38.fa R1.fq.gz R2.fq.gz \
  | samtools sort -@ 8 -o S1.sorted.bam -
# 2. 標記重複
gatk MarkDuplicates -I S1.sorted.bam -O S1.dedup.bam -M S1.dup_metrics.txt --CREATE_INDEX true
# 3. 鹼基品質校正（以已知變異位點以外的錯配估計系統性誤差）
gatk BaseRecalibrator -I S1.dedup.bam -R GRCh38.fa --known-sites dbsnp.vcf.gz --known-sites Mills_indels.vcf.gz -O S1.recal.table
gatk ApplyBQSR -I S1.dedup.bam -R GRCh38.fa --bqsr-recal-file S1.recal.table -O S1.bqsr.bam
# 4. 每個樣本產生 gVCF（WES / panel 加 -L targets.interval_list）
gatk HaplotypeCaller -R GRCh38.fa -I S1.bqsr.bam -O S1.g.vcf.gz -ERC GVCF
# 5. 多樣本聯合基因分型
gatk GenomicsDBImport -V S1.g.vcf.gz -V S2.g.vcf.gz -L chr1 --genomicsdb-workspace-path gdb_chr1
gatk GenotypeGVCFs -R GRCh38.fa -V gendb://gdb_chr1 -O cohort.chr1.vcf.gz
```

| 步驟 | 目的 | 細節 |
| --- | --- | --- |
| MarkDuplicates | PCR 重複不提供獨立證據 | 見 [Picard MarkDuplicates](../../bioinformatics-tools/ngs-tools/picard-markduplicates.md)；amplicon 不做 |
| BQSR | 校正儀器回報的品質分數 | 見 [鹼基品質分數](../ngs-qc/base-quality-scores.md) |
| HaplotypeCaller | 在活躍區域做局部重新組裝，同時呼叫 SNV 與 indel | 假設二倍體（`-ploidy` 可改） |
| gVCF + 聯合基因分型 | 多樣本時能區分「確定是參考型」與「沒資料」，並共享資訊 | 見 [VCF：gVCF](../file-formats/vcf.md#gvcf) |

## 變異過濾：VQSR vs 硬過濾

| | VQSR | 硬過濾 (hard filtering) |
| --- | --- | --- |
| 原理 | 以已知高信心變異（HapMap、1000G、Mills）訓練模型，學習真變異在 QD、MQ、FS、SOR 等註解上的分布，為每個變異打分 | 對每個註解設固定閾值 |
| 需要 | 大量變異：WGS，或約 30 個以上的 WES 樣本 | 不需要訓練資料 |
| 適合 | 大型 germline 世代研究 | 單一樣本、小 panel、非模式生物 |
| 優缺點 | 自適應、較準；樣本少時不穩定 | 透明、易解釋；閾值通用但不夠彈性 |

GATK 建議的硬過濾起點：

```bash
gatk VariantFiltration -V snps.vcf.gz -O snps.filtered.vcf.gz \
  -filter "QD < 2.0" --filter-name QD2 -filter "QUAL < 30.0" --filter-name QUAL30 \
  -filter "SOR > 3.0" --filter-name SOR3 -filter "FS > 60.0" --filter-name FS60 \
  -filter "MQ < 40.0" --filter-name MQ40 -filter "MQRankSum < -12.5" --filter-name MQRankSum-12.5 \
  -filter "ReadPosRankSum < -8.0" --filter-name ReadPosRankSum-8
# indel：QD < 2.0、QUAL < 30、FS > 200、ReadPosRankSum < -20
```

| 註解 | 意義 | 偽陽性的樣子 |
| --- | --- | --- |
| QD | 品質除以深度 | 低：深度高但證據弱 |
| FS / SOR | 鏈偏差 (strand bias) | 高：變異只出現在單一方向的 reads |
| MQ | 支持 reads 的比對品質（見 [比對品質](../ngs-qc/mapping-quality.md)） | 低：重複區、假基因 |
| MQRankSum | ALT 與 REF reads 的 MAPQ 差異 | 負值大：ALT reads 比對較差 |
| ReadPosRankSum | 變異在 read 中的位置 | 負值大：集中在 read 末端 |

新版 GATK 另提供以機器學習打分的工具（如 VETS / `ScoreVariantAnnotations`、單樣本的 `CNNScoreVariants`）；DeepVariant 以影像化的 pileup 訓練深度學習模型，單樣本準確度高，是常用的替代 caller。參考：[VQSR 與硬過濾說明（黃樹嘉）](https://huangshujia.com/2018/03/2018-03-23-wgs-best-practics-2/)。

## Somatic 流程（Mutect2）

```
腫瘤 BAM + 正常 BAM ──Mutect2（+ panel of normals、gnomAD germline resource）──► 原始呼叫
   ──GetPileupSummaries + CalculateContamination（樣本污染）
   ──LearnReadOrientationModel（FFPE / 氧化造成的方向性假象）
   ──FilterMutectCalls──► 過濾後 somatic VCF ──► 註解、判讀
```

| 與 germline 的差別 | 說明 |
| --- | --- |
| VAF 不是 50% / 100% | 受腫瘤純度、拷貝數、次選殖影響；低頻變異要靠深度 |
| 需要正常樣本 | 排除 germline 變異；只有腫瘤時要靠 gnomAD 與 panel of normals，偽陽性較多 |
| FFPE 假象 | C>T / G>A 去胺基假象；方向性模型與 UDG 處理 |
| 克隆性造血 | 血液正常樣本也可能帶 *DNMT3A*、*TET2* 等體細胞突變 |
| 低頻 / cfDNA | UMI 一致序列，見 [液態切片](../sequencing-techniques/liquid-biopsy.md) |

## 正規化與註解

```bash
bcftools norm -m -any -f GRCh38.fa filtered.vcf.gz -Oz -o norm.vcf.gz      # 拆多等位、左對齊
vep -i norm.vcf.gz -o annotated.vcf --vcf --cache --assembly GRCh38 --everything --mane --pick
```

正規化的原因見 [VCF：同一個變異的不同寫法](../file-formats/vcf.md#同一個變異的不同寫法)；註解工具見 [Ensembl VEP](../../genetics/databases/variant/ensembl-vep.md)；轉錄本選擇見 [MANE](../reference-data/gene-annotations.md#mane臨床報告的預設轉錄本)；臨床判讀見 [變異判讀](../../genetics/variant-interpretation/README.md)。

## 其他 caller 與變異類型

| 工具 | 用途 |
| --- | --- |
| DeepVariant | germline SNV / indel，短讀與長讀皆有模型 |
| Strelka2 | germline / somatic，速度快 |
| bcftools mpileup + call | 輕量 germline 呼叫 |
| VarDict、LoFreq | 低頻 / amplicon 變異 |
| Manta、DELLY、GRIDSS | 結構變異 (SV) |
| CNVkit、GATK gCNV | 拷貝數變異 (CNV)，見 [GC 偏差](../ngs-qc/gc-bias.md) |
| Clair3、Sniffles2 | 長讀定序的小變異 / SV |

流程的評估（敏感度、PPV、分層）用 GIAB 基準集，見 [參考標準品](../assay-validation/reference-standard.md#genome-in-a-bottle-giab)。
