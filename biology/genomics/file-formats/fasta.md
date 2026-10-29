[基因體學](../README.md) › [檔案格式](README.md) › FASTA

# FASTA

最簡單的序列格式：一行 `>` 開頭的名稱，接著一或多行序列。參考基因組、轉錄體、蛋白質序列、引子清單都用 FASTA。

```text
>chr1 AC:CM000663.2 gi:568336023 LN:248956422 rl:Chromosome M5:6aef897c3d6ff0c78aff06ac189178dd AS:GRCh38
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
...taaccctaaccctaaccctaACCCTAACCCTAACCC...
>KRAS_ex2F
GGCCTGCTGAAAATGACTGAA
```

| 部分 | 說明 |
| --- | --- |
| `>` 名稱行 | 第一個空白之前是序列 ID（工具只認這段，例如 `chr1`），之後是描述 |
| 序列 | 可單行或固定寬度（常見 60 或 80 字元）換行 |
| `N` | 未知鹼基（gap、著絲點） |
| 小寫 | **軟遮蔽 (soft-masked)** 的重複序列（見 [RepeatMasker](../../bioinformatics-tools/ngs-tools/repeatmasker.md)） |
| 其他 IUPAC 碼 | `R`（A/G）、`Y`（C/T）等，參考基因組中少量出現 |

## 索引與取序列

```bash
samtools faidx GRCh38.fa                       # 產生 GRCh38.fa.fai
samtools faidx GRCh38.fa chr7:140753330-140753340
cut -f1,2 GRCh38.fa.fai > GRCh38.genome        # bedtools 需要的「染色體 長度」表
samtools dict GRCh38.fa -o GRCh38.dict         # GATK / Picard 需要的序列字典
bwa index GRCh38.fa                            # 各比對器各有自己的索引格式

seqkit stats *.fa                              # 序列數、總長、N50
seqkit grep -p chr7 GRCh38.fa > chr7.fa        # 取出一條序列
```

| 索引 / 附檔 | 誰需要 |
| --- | --- |
| `.fai`（samtools faidx） | samtools、bcftools norm、IGV、GATK |
| `.dict`（序列字典） | GATK、Picard |
| `.gzi` | bgzip 壓縮的 FASTA 需要（gzip 壓縮的不能建索引） |
| 比對器索引 | BWA（`.bwt` 等）、STAR（資料夾）、Bowtie2（`.bt2`）、minimap2（`.mmi`） |

> FASTA、`.fai`、`.dict`、比對器索引、GTF 必須來自**同一個版本、同一套染色體命名**；不同來源的 hg38（UCSC / Ensembl / NCBI）不能混用，見 [參考基因組](../reference-data/reference-genomes.md)。

R 中用 `Biostrings::readDNAStringSet()` 讀取，見 [Bioconductor](../../bioinformatics-tools/bioconductor.md)。
