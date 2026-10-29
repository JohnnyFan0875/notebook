[基因體學](../README.md) › [檔案格式](README.md) › VCF

# VCF (Variant Call Format)

儲存變異（SNV、indel、結構變異）與每個樣本基因型的標準格式，是變異呼叫的輸出、註解與判讀的輸入。BCF 是它的二進位版本。

## 結構

```text
##fileformat=VCFv4.2
##reference=GRCh38
##contig=<ID=chr1,length=248956422>
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">
##FILTER=<ID=LowQual,Description="QUAL < 30">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for ref and alt">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype quality">
#CHROM  POS        ID         REF  ALT    QUAL  FILTER  INFO          FORMAT       S1             S2
chr1    123456     rs1234567  G    A      812   PASS    DP=62;AF=0.25       GT:AD:DP:GQ  0/1:18,14:32:99     0/0:30,0:30:90
chr7    140753336  .          A    T,G    55    LowQual DP=40;AF=0.5,0.5    GT:AD:DP:GQ  1/2:2,20,18:40:60   ./.:.:.:.
```

| 欄位 | 意義 |
| --- | --- |
| CHROM / POS | 染色體與位置（**1-based**；indel 的 POS 是前一個錨定鹼基） |
| ID | 已知變異 ID（dbSNP rsID），未知為 `.` |
| REF / ALT | 參考 / 替代等位基因；多個 ALT 以逗號分隔（多等位位點） |
| QUAL | 「此位點有變異」的 Phred 分數 |
| FILTER | `PASS`、過濾名稱，或 `.`（未過濾） |
| INFO | 位點層級註解，`key=value` 以 `;` 分隔（定義在 `##INFO`） |
| FORMAT + 樣本欄 | 每個樣本的資料，欄位順序由 FORMAT 決定 |

## 常見 FORMAT 欄位

| 欄位 | 意義 | 例 |
| --- | --- | --- |
| GT | 基因型：`0` = REF、`1` = 第一個 ALT、`2` = 第二個 ALT；`/` 未定相、`\|` 已定相 | `0/1`、`1\|0`、`./.`（無資料） |
| AD | 各等位基因的支持 reads 數（REF, ALT…） | `18,14` |
| DP | 該樣本的深度 | `32` |
| GQ | 基因型品質（Phred） | `99` |
| PL | 各基因型的相對機率（Phred，最可能者為 0） | `450,0,600` |
| AF（體細胞 caller） | 變異等位基因比例 (VAF) | `0.12` |

由 AD 計算 S1 的 VAF：14 / (18 + 14) ≈ 0.44，符合異型合子。INFO 的 `AF` 則是「這批樣本中」ALT 等位基因的比例（第一列：S1 一個 ALT、兩個樣本共 4 個等位基因 → 0.25；第二列 S2 無資料，只計 S1 的 2 個等位基因 → 各 0.5），兩者意義不同；VAF 與族群頻率的差別見 [變異等位基因頻率](../../genetics/foundations/variant-allele-frequency.md)。

## 同一個變異的不同寫法

| 問題 | 例 | 解法 |
| --- | --- | --- |
| 多等位位點 | `ALT=T,G` | `bcftools norm -m -any` 拆成兩列 |
| indel 位置不唯一 | 重複序列中的缺失可左移或右移 | `bcftools norm -f ref.fa` 左對齊 |
| 染色體命名 / 版本 | `chr7` vs `7`；hg19 vs hg38 | 統一後再比對資料庫 |

比對資料庫（ClinVar、gnomAD）前**一定要正規化**，否則同一個變異會被當成不同變異。

## gVCF

gVCF 除了變異位點，也記錄「非變異區段」的信心（`<NON_REF>` 區塊），讓多樣本聯合基因分型 (joint genotyping) 能區分「確定是參考型」與「沒有資料」。GATK HaplotypeCaller 用 `-ERC GVCF` 產生，再以 GenomicsDBImport + GenotypeGVCFs 合併。

## 工具

| 工具 | 用途 |
| --- | --- |
| [bcftools](../../bioinformatics-tools/ngs-tools/bcftools.md) | 檢視、過濾、正規化、合併、查詢 |
| [tabix](../../bioinformatics-tools/ngs-tools/tabix.md) | bgzip 壓縮後建索引、依區域查詢 |
| GATK | 變異呼叫、VQSR、過濾 |
| VEP、SnpEff、ANNOVAR | 功能註解（見 [Ensembl VEP](../../genetics/databases/variant/ensembl-vep.md)） |
| [IGV](../../bioinformatics-tools/visualization/igv.md) | 目視檢查 |
| cyvcf2 / pysam（Python）、VariantAnnotation（R） | 程式化讀取 |

規格：[VCF v4.3 specification](https://samtools.github.io/hts-specs/VCFv4.3.pdf)。
