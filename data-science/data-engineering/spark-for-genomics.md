[Data Science](../README.md) › [Data Engineering](README.md) › Spark 處理基因體資料

# Spark 處理基因體資料 (Spark for Genomics: Glow and Hail)

biobank 規模的變異資料（數十萬樣本 × 數千萬位點）用單機的 bcftools / PLINK 會變慢或吃不下，這時可以用建立在 Spark 上的兩個工具：**Glow** 把 VCF 讀成 Spark DataFrame，與一般 SQL / ETL 流程整合；**Hail** 用專門的 MatrixTable 結構做 QC、GWAS 與族群遺傳分析（gnomAD、All of Us 的分析即以 Hail 為主）。VCF 格式見 [VCF](../../biology/genomics/sequencing-and-analysis/file-format/vcf.md)，GWAS 原理見 [GWAS](../../biology/genomics/sequencing-and-analysis/genome-wide-analysis/gwas-fundamental.md)，Spark 觀念見 [Spark 與 PySpark](spark.md)。

## 先選工具

| 情況 | 工具 |
| --- | --- |
| 數千樣本以內、單機跑得動 | `bcftools`、PLINK 2、REGENIE：最快、文件最多 |
| 只需篩選位點、轉成表格與臨床資料 join | Glow 讀 VCF → Delta / Parquet → Spark SQL；或 VCF 轉 Parquet 後用 [DuckDB](../databases/duckdb-and-parquet.md) |
| biobank 規模的 sample / variant QC、GWAS、PCA、親緣分析 | Hail |
| 平台是 Databricks、要與其他資料管線整合 | Glow（Databricks 與 Regeneron 開發） |

| | Glow | Hail |
| --- | --- | --- |
| 資料結構 | Spark DataFrame：一列一個位點，`genotypes` 是陣列欄 | MatrixTable：rows = 位點、cols = 樣本、entries = 基因型 |
| 介面 | PySpark / Scala / SQL | Python（自己的 expression 語言，底層是 Spark） |
| 強項 | 與 ETL、Delta、SQL 整合；pipe transformer 平行跑既有命令列工具 | 遺傳統計函式完整；QC、GWAS、PCA、LD pruning |
| 座標 | `start` 是 0-based、半開區間（VCF `POS` − 1） | `locus` 使用 1-based，與 VCF 相同 |

> Glow 的 `start` 比 VCF 的 `POS` 小 1，與其他表 join 前要換算，否則全部錯位一個鹼基。

## Glow

```python
import glow
from pyspark.sql import functions as F

spark = glow.register(spark)                          # 註冊 vcf / bgen / plink 讀寫器與函式

vcf = spark.read.format("vcf").load("cohort/*.vcf.gz")
vcf.printSchema()   # contigName, start, end, names, referenceAllele, alternateAlleles,
                    # qual, filters, INFO_*, genotypes: array<struct<sampleId, calls, ...>>

# 1. 拆多等位位點、左對齊標準化（比對不同來源的位點前必做）
split = glow.transform("split_multiallelics", vcf)
norm = glow.transform("normalize_variants", split, reference_genome_path="GRCh38.fa")

# 2. 位點層級統計與篩選
qc = (norm
      .withColumn("stats", glow.call_summary_stats("genotypes"))   # callRate、alleleFrequencies 等
      .withColumn("hwe", glow.hardy_weinberg("genotypes"))
      .where((F.col("stats.callRate") >= 0.95) & (F.col("hwe.pValueHwe") > 1e-6)))

# 3. 存成 Delta / Parquet，之後用 SQL 與臨床資料 join
qc.write.format("delta").mode("overwrite").save("variants_qc.delta")
```

| 功能 | Glow 寫法 |
| --- | --- |
| 讀 BGEN / PLINK | `spark.read.format("bgen")`、`format("plink")` |
| 基因型轉劑量 | `glow.genotype_states("genotypes")`（每樣本的 alt allele 數） |
| 線性 / 邏輯迴歸 GWAS | `glow.gwas.linear_regression(...)`、`glow.gwas.logistic_regression(...)` |
| 平行跑命令列工具 | `glow.transform("pipe", df, cmd=[...], input_formatter="vcf", ...)`：把每個 partition 餵給 `bcftools` 等 |
| 全基因體迴歸 | GloWGR（REGENIE 演算法的實作） |

Glow 的版本與 Spark / Databricks runtime 綁定，安裝前查 [Glow 文件](https://glow.readthedocs.io/) 的相容表。

## Hail

```python
import hail as hl

hl.init(default_reference="GRCh38")                   # 底層會啟動 Spark（本機或叢集）

# 1. 匯入一次、存成 MatrixTable，之後都讀 .mt（比每次解析 VCF 快很多）
hl.import_vcf("cohort.vcf.gz", force_bgz=True).write("cohort.mt", overwrite=True)  # .gz 實為 bgzip 時需 force_bgz
mt = hl.read_matrix_table("cohort.mt")
mt.count()                                            # (n_variants, n_samples)
mt.describe()                                         # row / col / entry 欄位

# 2. 樣本 QC：call rate、平均深度、het/hom 比
mt = hl.sample_qc(mt)
mt = mt.filter_cols((mt.sample_qc.call_rate >= 0.97) & (mt.sample_qc.dp_stats.mean >= 20))

# 3. 位點 QC：call rate、MAF、HWE
mt = hl.variant_qc(mt)
mt = mt.filter_rows((mt.variant_qc.call_rate >= 0.95)
                    & (hl.min(mt.variant_qc.AF) > 0.01)
                    & (mt.variant_qc.p_value_hwe > 1e-6))

# 4. 加入表型與共變數
pheno = hl.import_table("pheno.tsv", impute=True, key="s")
mt = mt.annotate_cols(pheno=pheno[mt.s])

# 5. 族群結構：常見位點 LD pruning 後做 PCA
common = mt.filter_rows(hl.min(mt.variant_qc.AF) > 0.05)
pruned = hl.ld_prune(common.GT, r2=0.2)
_, pcs, _ = hl.hwe_normalized_pca(common.filter_rows(hl.is_defined(pruned[common.row_key])).GT, k=10)
mt = mt.annotate_cols(pc=pcs[mt.s].scores)

# 6. GWAS：線性迴歸，截距要自己放進 covariates
gwas = hl.linear_regression_rows(
    y=mt.pheno.height,
    x=mt.GT.n_alt_alleles(),
    covariates=[1.0, mt.pheno.is_female, *[mt.pc[i] for i in range(5)]],
)
gwas.order_by(gwas.p_value).show(5)
gwas.export("gwas_height.tsv.bgz")
```

| 功能 | Hail 寫法 |
| --- | --- |
| 二元表型 | `hl.logistic_regression_rows(test="wald", ...)`（或 `"firth"` 處理罕見變異 / 不平衡） |
| 親緣與重複樣本 | `hl.pc_relate(...)`、`hl.identity_by_descent(...)` |
| 性別檢查 | `hl.impute_sex(mt.GT)`（X 染色體 F 係數） |
| 註解 | `hl.vep(...)`、與 gnomAD 等 Hail Table 依 `locus, alleles` join |
| 視覺化 | `hl.plot.manhattan(gwas.p_value)`、`hl.plot.qq(gwas.p_value)` |

> 截距常被忘記：Hail 的 `covariates` 不會自動加常數項，必須寫 `1.0`。

## 陷阱

| 陷阱 | 後果 | 做法 |
| --- | --- | --- |
| 參考基因體版本混用 | 位點對不上、註解錯 | 匯入時指定 GRCh37 / GRCh38，混合來源先 liftover |
| 多等位位點沒拆 | AF、迴歸對 alt allele 定義不一致 | Glow `split_multiallelics`；Hail `hl.split_multi_hts()` |
| 未標準化 indel 表示法 | 同一變異在兩個來源被視為不同 | 左對齊標準化（`normalize_variants`、`bcftools norm`） |
| 每次都重新解析 VCF | 大部分時間花在解析 | 匯入一次存成 MatrixTable / Delta |
| 族群分層沒校正 | GWAS 假陽性 | 共變數放入 PC；必要時用混合模型（REGENIE、SAIGE） |
| p 值門檻沿用 0.05 | 數百萬次檢定 | 全基因體顯著門檻 5×10⁻⁸，見 [多重檢定](../statistics/inferential-statistics/multiple-testing.md) |
| 雲端費用失控 | 叢集閒置也在計費 | 自動縮放、用完關閉；先在一條染色體上測試 |
| 個人層級基因型外流 | 隱私與合規問題 | 在受控環境分析、只匯出彙總結果，見 [隱私與法規](../responsible-ai/privacy-and-regulation.md) |
