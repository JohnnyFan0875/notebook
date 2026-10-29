[Biology](README.md) › 生資速查

# 生資速查 (Bioinformatics Quick Reference)

依「手上有什麼」或「想知道什麼」找到對應筆記。每列只給入口，細節點連結看。

## 1. 拿到這個檔案 → 怎麼處理

| 檔案 | 內容 | 常做的事 → 工具 | 格式說明 |
| --- | --- | --- | --- |
| `.fastq.gz` | reads + 每個鹼基的品質分數 | 品質報告 → [FastQC](bioinformatics-tools/ngs-tools/fastqc.md)；修剪 adapter / polyG → [fastp](bioinformatics-tools/ngs-tools/fastp.md) | [FASTQ](genomics/file-formats/fastq.md) |
| `.fa` / `.fasta` | 參考序列或引子 / 蛋白質序列 | 建索引、取區域 → [samtools](bioinformatics-tools/ngs-tools/samtools.md) `faidx`；選版本 → [參考基因組](genomics/reference-data/reference-genomes.md) | [FASTA](genomics/file-formats/fasta.md) |
| `.bam` / `.cram` | 比對結果 | 排序 / 索引 / 統計 → [samtools](bioinformatics-tools/ngs-tools/samtools.md)；標記重複 → [Picard](bioinformatics-tools/ngs-tools/picard-markduplicates.md) / [sambamba](bioinformatics-tools/ngs-tools/sambamba.md)；目視 → [IGV](bioinformatics-tools/visualization/igv.md) | [BAM](genomics/file-formats/bam.md) |
| `.vcf.gz` | 變異 | 過濾 / 正規化 / 合併 → [bcftools](bioinformatics-tools/ngs-tools/bcftools.md)；索引與區域查詢 → [tabix](bioinformatics-tools/ngs-tools/tabix.md)；註解 → [VEP](genetics/databases/variant/ensembl-vep.md) | [VCF](genomics/file-formats/vcf.md) |
| `.bed` | 區間（panel 目標區、peak） | 交集 / 覆蓋度 / 合併 → [bedtools](bioinformatics-tools/ngs-tools/bedtools.md) | [BED](genomics/file-formats/bed.md) |
| `.gtf` / `.gff3` | 基因 / 轉錄本 / exon 註解 | 比對與定量的註解輸入 → [RNA-seq 比對](genomics/workflows/rna-seq/03-reference-alignment-and-bam-qc.md)；選哪套 → [基因註解](genomics/reference-data/gene-annotations.md) | [GTF / GFF](genomics/file-formats/gtf-gff.md) |
| count matrix（基因 × 樣本） | bulk RNA-seq 計數 | 過濾 / 標準化 → [RNA-seq 05](genomics/workflows/rna-seq/05-count-matrix-filtering-normalization.md)；差異表現 → [RNA-seq 07](genomics/workflows/rna-seq/07-differential-expression.md) | — |
| `.h5ad` / 10x `filtered_feature_bc_matrix` | 單細胞計數（稀疏） | QC / 分群 / marker → [AnnData / scanpy](../data-science/python-foundations/anndata-and-scanpy.md) | [單細胞 RNA-seq](genomics/sequencing-techniques/single-cell-rna-seq/README.md) |
| DICOM / NIfTI | 醫學影像 | 讀取、spacing、mask → [生醫影像分析](../data-science/image-analysis/biomedical-image-analysis.md) | [醫學影像](medical-imaging/README.md) |

> 座標系統不同是最常見的 off-by-one 來源：BED 是 0-based 半開區間，VCF / GTF / SAM 是 1-based，見 [0-based vs 1-based](genomics/file-formats/zero-one-based.md)。

## 2. 想查這個 → 去哪個資料庫

| 想知道 | 首選 | 補充 |
| --- | --- | --- |
| 基因的正式名稱、別名 | [HGNC](genetics/databases/gene/hgnc.md) | [NCBI Gene](genetics/databases/gene/ncbi-gene.md)、[GeneCards](genetics/databases/gene/genecards.md) |
| 基因位置、轉錄本、外顯子 | [Ensembl](genetics/databases/gene/ensembl.md)、[UCSC Genome Browser](genetics/databases/gene/ucsc-genome-browser.md) | 臨床報告用的轉錄本 → [MANE（基因註解）](genomics/reference-data/gene-annotations.md) |
| 變異的寫法是否正確 | [HGVS 命名](genetics/variant-interpretation/hgvs-nomenclature.md) | — |
| 變異的 rsID | [dbSNP](genetics/databases/variant/dbsnp.md) | — |
| 變異是否被判讀為致病 | [ClinVar](genetics/databases/variant/clinvar.md) | [VarSome](genetics/databases/variant/varsome.md)（整合瀏覽）、[BRCA Exchange](genetics/databases/variant/brca-exchange.md) |
| 變異在族群中多常見 | [gnomAD](genetics/databases/population-frequency/gnomad.md) | 東亞 / 台灣 → [TaiwanGenomes](genetics/databases/population-frequency/taiwangenomes.md)、[HGVD](genetics/databases/population-frequency/hgvd.md)；結構變異 → [DGV](genetics/databases/population-frequency/dgv.md) |
| 變異對蛋白質 / 剪接的預測影響 | [VEP](genetics/databases/variant/ensembl-vep.md) | 分數怎麼用 → [in-silico 預測](genetics/variant-interpretation/in-silico-prediction.md) |
| 基因與哪些疾病有關、證據多強 | [OMIM](genetics/databases/gene-disease-association/omim.md)、[ClinGen 基因有效性](genetics/databases/gene-disease-association/clingen-validity.md)、[GenCC](genetics/databases/gene-disease-association/gencc.md) | [GeneReviews](genetics/databases/gene-disease-association/gene-reviews.md)、[PanelApp](genetics/databases/gene-disease-association/genomics-england-panelapp.md) |
| 病人表型 → 候選基因 | [HPO](genetics/databases/gene-disease-association/hpo.md) | 罕病 → [Orphanet](genetics/databases/gene-disease-association/orphanet.md)、[台灣罕病](genetics/databases/gene-disease-association/rare-disease-taiwan.md) |
| 癌症體細胞變異的意義 | [COSMIC](genetics/databases/variant/cosmic.md)、[CIViC](genetics/databases/variant/civic.md) | 治療指引 → [NCCN](genomics/cancer-genomics/nccn.md)；公開腫瘤資料 → [TCGA / GDC](genomics/cancer-genomics/tcga-gdc.md) |
| 變異 / 基因型影響用藥 | [CPIC](genetics/databases/pharmacogenomics/cpic.md) | [ClinPGx（PharmGKB）](genetics/databases/pharmacogenomics/pharmgkb.md)；伴隨診斷 → [FDA](clinical-informatics-and-standards/regulatory-databases/fda-drug-database.md) |
| 變異與複雜性狀的關聯 | [GWAS Catalog](genetics/databases/variant/gwas-catalog.md) | 調控機制 → [eQTL](genomics/genome-wide-analysis/eqtl.md)（GTEx） |
| 基因在哪個組織 / 細胞表現 | [GTEx](genetics/databases/functional-expression/gtex.md) | 蛋白層級 → [Human Protein Atlas](molecular-biology/molecular-databases/human-proteome-atlas.md) |
| 蛋白質功能、結構域 | [UniProt](molecular-biology/molecular-databases/uniprot.md) | [InterPro](molecular-biology/molecular-databases/interpro.md) |
| 基因屬於哪條通路 | [KEGG](genetics/databases/functional-expression/kegg.md) | 富集分析 → [RNA-seq 09](genomics/workflows/rna-seq/09-annotation-and-functional-enrichment.md) |
| 公開的原始定序資料 | [SRA / ENA / GEO](genomics/reference-data/raw-data-repositories.md) | — |
| 微生物分類參考 | [微生物體資料庫](microbiome-and-metagenomics/microbiome-databases.md) | — |
| 臨床代碼（診斷、檢驗、藥物） | [臨床術語總表](clinical-informatics-and-standards/clinical-terminology/README.md) | 查 ontology 用語 → [OLS](clinical-informatics-and-standards/clinical-terminology/ontology-lookup-service.md) |

完整的變異查詢順序（ID → 臨床證據 → 頻率 → 功能 → ACMG/AMP）見 [遺傳學資料庫：查詢流程](genetics/databases/README.md#查詢流程)。

## 3. 想回答這個問題 → 用什麼技術與流程

| 生物問題 | 技術 | 分析流程 / 方法 |
| --- | --- | --- |
| 病人帶有哪些致病變異（罕病、遺傳性癌症） | [WES / panel](genomics/sequencing-techniques/targeted-panels.md) | [變異呼叫（germline）](genomics/workflows/variant-calling.md) → [ACMG/AMP](genetics/variant-interpretation/acmg-amp.md) |
| 腫瘤帶有哪些體細胞突變 | 腫瘤 / 正常配對定序 | [變異呼叫（Mutect2）](genomics/workflows/variant-calling.md) → [突變特徵](genomics/cancer-genomics/mutational-signatures.md) |
| 能不能從血液追蹤腫瘤 / MRD | [液態切片（cfDNA / ctDNA）](genomics/sequencing-techniques/liquid-biopsy.md) | 低 VAF 偵測 → [VAF](genetics/foundations/variant-allele-frequency.md)、[UMI 與重複率](genomics/ngs-qc/duplication-rate.md) |
| 結構變異、重複區、單倍型 | [長讀定序（PacBio / ONT）](genomics/sequencing-techniques/sequencing-platforms.md) | [其他 caller 與變異類型](genomics/workflows/variant-calling.md#其他-caller-與變異類型) |
| 哪些基因在不同條件下表現改變 | bulk RNA-seq | [RNA-seq 分析](genomics/workflows/rna-seq/README.md)；microarray / 複雜設計 → [limma](genomics/workflows/limma-differential-expression.md) |
| 樣本裡有哪些細胞類型 / 狀態 | [單細胞 RNA-seq](genomics/sequencing-techniques/single-cell-rna-seq/README.md) | [scanpy 流程](../data-science/python-foundations/anndata-and-scanpy.md)、[軌跡分析](genomics/sequencing-techniques/single-cell-rna-seq/trajectory.md) |
| 轉錄因子 / 組蛋白修飾結合在哪 | [ChIP-seq](genomics/sequencing-techniques/chip-seq.md) | peak calling → 差異結合 |
| 哪些變異與性狀有關、透過哪個基因 | 基因分型晶片 / WGS | [GWAS](genomics/genome-wide-analysis/gwas-fundamental.md) → [QTL](genomics/genome-wide-analysis/qtl-analysis-and-mapping.md) → [Colocalization](genomics/genome-wide-analysis/colocalization.md) |
| 微生物群落組成與功能 | [16S vs shotgun](microbiome-and-metagenomics/README.md#16s-vs-shotgun) | [16S 分析](microbiome-and-metagenomics/16s-analysis.md)、[Shotgun 宏基因體](microbiome-and-metagenomics/shotgun-metagenomics.md) |
| 驗證 NGS 找到的變異 / 表現差異 | [qPCR、Western blot、ELISA](molecular-biology/experimental-methods/README.md#依目標分子選方法) | 設計引子 → [引子設計](bioinformatics-tools/primer-design/README.md) |
| 檢測方法是否可靠、可上線 | [檢測確效](genomics/assay-validation/README.md) | 標準品 → [GIAB 等參考標準](genomics/assay-validation/reference-standard.md) |
| 影像中的病灶或組織結構 | [CT / MRI / PET / 超音波](medical-imaging/README.md#模態比較) | [影像分析](../data-science/image-analysis/README.md)、[電腦視覺](../data-science/deep-learning/computer-vision/README.md) |
| 用病歷資料做世代研究 | [OMOP-CDM](clinical-informatics-and-standards/clinical-terminology/omop-cdm.md) | [臨床資料庫](clinical-informatics-and-standards/clinical-databases/README.md)、[存活分析](../data-science/statistics/survival-analysis/README.md) |

## 4. 分析步驟 → 統計 / ML 方法

| 生資步驟 | 背後的方法 | 見 |
| --- | --- | --- |
| RNA-seq 差異表現（DESeq2 / edgeR） | 負二項 GLM、過度離散、經驗貝氏收縮 | [GLM 與計數模型](../data-science/statistics/regression-analysis/glm-count-models.md)、[RNA-seq 06](genomics/workflows/rna-seq/06-exploratory-design-and-count-models.md) |
| 數萬個基因同時檢定 | FDR（Benjamini–Hochberg） | [多重檢定](../data-science/statistics/inferential-statistics/multiple-testing.md) |
| 樣本分群、找異常樣本 | PCA、階層分群 | [PCA](../data-science/statistics/multivariate-analysis/pca.md)、[分群](../data-science/statistics/multivariate-analysis/clustering.md) |
| 批次效應、配對 / 重複量測設計 | 設計矩陣加入批次、混合效應模型 | [干擾與批次效應](../data-science/statistics/experimental-design/confounding-bias.md)、[混合效應模型](../data-science/statistics/regression-analysis/mixed-effects-models.md)、[limma](genomics/workflows/limma-differential-expression.md) |
| 單細胞降維與分群 | PCA → kNN 圖 → Leiden、UMAP | [UMAP](../data-science/machine-learning/unsupervised-learning/dimensionality-reduction/umap.md)、[網路分析](../data-science/network-analysis/README.md) |
| 單細胞批次整合 | VAE（scVI）、負二項似然 | [單細胞深度學習](../data-science/deep-learning/bio-applications/single-cell-deep-learning.md) |
| 用表現量 / 變異預測表型 | 高維小樣本（p ≫ n）、正則化、資料洩漏 | [高維資料](../data-science/machine-learning/foundations/high-dimensional-data.md)、[資料洩漏](../data-science/machine-learning/foundations/data-leakage.md) |
| 序列 → 功能 / 結構 | CNN、蛋白質語言模型 | [序列與蛋白模型](../data-science/deep-learning/bio-applications/sequence-and-protein-models.md) |
| 微生物差異豐度 | 組成資料、稀疏計數 | [雙變數相關（組成資料的假相關）](../data-science/statistics/descriptive-statistics/bivariate.md)、[16S 分析](microbiome-and-metagenomics/16s-analysis.md) |
| 大型基因體資料（數十萬樣本） | 分散式運算、欄式儲存 | [Glow / Hail](../data-science/data-engineering/spark-for-genomics.md)、[DuckDB / Parquet](../data-science/databases/duckdb-and-parquet.md) |

## 5. 常被混淆的概念

| 容易混為一談 | 差別 | 見 |
| --- | --- | --- |
| VAF vs 族群等位基因頻率 | VAF 是**一個樣本內**支持變異的 reads 比例；AF 是變異在**族群**中的頻率 | [變異等位基因頻率](genetics/foundations/variant-allele-frequency.md) |
| de novo vs novel | de novo 是父母都沒有、在子代新發生；novel 只是資料庫裡沒看過 | [新生變異](genetics/foundations/de-novo-variant.md) |
| GRCh37 vs GRCh38、`chr1` vs `1` | 座標不同；同版本也有 UCSC / Ensembl 兩種染色體命名，混用會整批對不上 | [參考基因組](genomics/reference-data/reference-genomes.md) |
| 鹼基品質 vs 比對品質 | Phred 分數評估**單一鹼基**定錯的機率；MAPQ 評估 **read 放錯位置**的機率 | [鹼基品質分數](genomics/ngs-qc/base-quality-scores.md)、[MAPQ](genomics/ngs-qc/mapping-quality.md) |
| 深度 vs 均勻度 | 平均深度高不代表每個目標區都夠；要看達到某深度的比例 | [深度與覆蓋度](genomics/ngs-qc/sequencing-depth-coverage.md)、[均勻度](genomics/ngs-qc/uniformity.md) |
| TPM vs counts | TPM 適合樣本內比較與作圖；DESeq2 / edgeR 要吃**原始 counts** | [RNA-seq 05：標準化方法比較](genomics/workflows/rna-seq/05-count-matrix-filtering-normalization.md#標準化方法比較) |
| 生物重複 vs 技術重複 | 推論要靠生物重複；技術重複只量測量誤差，當成獨立樣本會變成假重複 | [實驗設計](../data-science/statistics/experimental-design/README.md) |
| Validation vs verification | validation 是自建 / 修改的方法要證明可用；verification 是確認已核准的方法在自家實驗室表現一致 | [檢測確效](genomics/assay-validation/README.md#validation-vs-verification) |
| 血清 vs 血漿 | 血清已凝血、不含凝血因子；cfDNA 分析要用血漿，避免白血球破裂釋出 DNA | [血清 vs 血漿](laboratory-medicine/sample-types/serum-plasma.md) |
| 資料庫有紀錄 vs 已確認致病 | ClinVar 有衝突分類、HGMD 收錄文獻提及；要看審閱等級與證據 | [ACMG/AMP](genetics/variant-interpretation/acmg-amp.md)、[ClinVar](genetics/databases/variant/clinvar.md) |
