[Notebook](../README.md) › Biology

# 生物學 (Biology)

生物資訊需要的生物與醫學背景：定序資料怎麼產生、檔案與參考資料怎麼用、變異與基因怎麼查、結果怎麼回到臨床與實驗驗證。分析方法本身（統計、ML、程式）放在 [Data Science](../data-science/README.md)，執行環境與工作流放在 [Computing](../computing/README.md)，這裡以連結對應。

> 生資分析的錯誤常不是出在演算法，而是出在**對資料來源的誤解**：用錯基因組版本、把 VAF 當族群頻率、忽略定序平台的錯誤型態、把資料庫的一筆紀錄當成定論。先懂資料怎麼來，再選方法。

**找入口**：拿到某種檔案、想查某個基因 / 變異、或想回答某個生物問題時，先看 [生資速查](quick-reference.md)。

## 模組

### 資料分析核心

| 模組 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [基因體學](genomics/README.md) | 檔案格式、參考資料、NGS QC、定序技術、RNA-seq / 變異呼叫流程、GWAS / QTL、癌症基因體、檢測確效 | 定序資料怎麼從 FASTQ 走到生物學結論？品質夠不夠？ |
| [遺傳學](genetics/README.md) | VAF 與族群頻率、基因 / 變異 / 疾病 / 藥物資料庫、HGVS、in-silico 預測、ACMG/AMP | 這個基因或變異是什麼、多常見、是否致病？ |
| [生資工具](bioinformatics-tools/README.md) | samtools、bcftools、bedtools、fastp、Picard、Bioconductor、引子設計、IGV | 處理 FASTQ / BAM / VCF / BED 要用哪個指令？ |

### 生物醫學背景

| 模組 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [分子生物學](molecular-biology/README.md) | 電泳、blot、qPCR、ELISA、寡核苷酸合成；UniProt、InterPro、HPA | 怎麼用濕實驗驗證 NGS 結果？蛋白質有什麼功能？ |
| [免疫學](immunology/README.md) | T / B 細胞亞群、細胞激素、免疫標記、PBMC、TIL | 單細胞資料裡這群細胞是什麼？免疫反應偏哪一型？ |
| [微生物體](microbiome-and-metagenomics/README.md) | 16S vs shotgun、DADA2 / QIIME 2、MAG、分類資料庫、FMT | 群落裡有誰、有多少、能做什麼？組成資料怎麼分析？ |

### 臨床與檢驗

| 模組 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [臨床資訊與標準](clinical-informatics-and-standards/README.md) | SNOMED CT、ICD、LOINC、FHIR、OMOP-CDM；MIMIC-IV、UK Biobank；FDA / EMA | 病歷欄位用哪套代碼？哪裡有可申請的臨床資料？ |
| [檢驗醫學](laboratory-medicine/README.md) | 血清 vs 血漿、分析前變因、血庫輸血、SDS / COA | 檢體怎麼收、放太久會影響什麼？ |
| [醫學影像](medical-imaging/README.md) | X 光 / CT、MRI、PET、超音波；HU、SUV、DICOM | 影像的強度值代表什麼物理量？ |

## 建議路線

| 讀者 | 路線 |
| --- | --- |
| **生資入門（bulk RNA-seq）** | [檔案格式](genomics/file-formats/README.md) → [參考資料](genomics/reference-data/README.md) → [NGS 品質指標](genomics/ngs-qc/README.md) → [RNA-seq 分析](genomics/workflows/rna-seq/README.md) → [GLM 與計數模型](../data-science/statistics/regression-analysis/glm-count-models.md) → [多重檢定](../data-science/statistics/inferential-statistics/multiple-testing.md) |
| **臨床基因體 / 變異判讀** | [定序平台](genomics/sequencing-techniques/sequencing-platforms.md) → [標靶定序](genomics/sequencing-techniques/targeted-panels.md) → [變異呼叫](genomics/workflows/variant-calling.md) → [VCF](genomics/file-formats/vcf.md) → [資料庫查詢流程](genetics/databases/README.md#查詢流程) → [HGVS](genetics/variant-interpretation/hgvs-nomenclature.md) → [ACMG/AMP](genetics/variant-interpretation/acmg-amp.md) → [檢測確效](genomics/assay-validation/README.md) |
| **癌症基因體** | [VAF](genetics/foundations/variant-allele-frequency.md) → [液態切片](genomics/sequencing-techniques/liquid-biopsy.md) → [變異呼叫（Mutect2）](genomics/workflows/variant-calling.md) → [變異資料庫（COSMIC、CIViC）](genetics/databases/variant/README.md) → [突變特徵](genomics/cancer-genomics/mutational-signatures.md) → [TCGA / GDC](genomics/cancer-genomics/tcga-gdc.md) → [NCCN](genomics/cancer-genomics/nccn.md) |
| **單細胞 / 免疫** | [免疫學](immunology/README.md) → [單細胞 RNA-seq](genomics/sequencing-techniques/single-cell-rna-seq/README.md) → [AnnData / scanpy](../data-science/python-foundations/anndata-and-scanpy.md) → [網路分析](../data-science/network-analysis/README.md) → [單細胞深度學習](../data-science/deep-learning/bio-applications/single-cell-deep-learning.md) |
| **群體遺傳 / GWAS** | [族群頻率資料庫](genetics/databases/population-frequency/README.md) → [GWAS](genomics/genome-wide-analysis/gwas-fundamental.md) → [eQTL](genomics/genome-wide-analysis/eqtl.md) → [Colocalization](genomics/genome-wide-analysis/colocalization.md) → [資料偏誤與代表性](../data-science/responsible-ai/data-bias-and-representativeness.md) |
| **真實世界資料 / 醫療 AI** | [臨床術語](clinical-informatics-and-standards/clinical-terminology/README.md) → [OMOP-CDM](clinical-informatics-and-standards/clinical-terminology/omop-cdm.md) → [臨床資料庫](clinical-informatics-and-standards/clinical-databases/README.md) → [隱私與法規](../data-science/responsible-ai/privacy-and-regulation.md) → [醫學影像](medical-imaging/README.md) → [影像分析](../data-science/image-analysis/README.md) |

## 一個定序專案的資料流

```
檢體（血液 / 組織 / 糞便）──檢體類型、分析前變因──► 核酸萃取、建庫
  ──定序平台、panel / WGS / RNA-seq / 單細胞──► FASTQ
  ──FastQC / fastp，NGS 品質指標──► 比對（參考基因組 + 基因註解）──► BAM
  ├─ DNA：變異呼叫 ──► VCF ──► 註解（VEP）──► 資料庫查詢 ──► ACMG/AMP 判讀 ──► 報告
  └─ RNA：定量 ──► count matrix ──► 標準化 / 差異表現 / 富集 ──► 濕實驗驗證（qPCR、Western）
          全程：版本記錄、工作流引擎、容器 ──► 可重現
```

| 階段 | 本領域 | 跨領域 |
| --- | --- | --- |
| 檢體與實驗 | [檢體類型](laboratory-medicine/sample-types/README.md)、[實驗方法](molecular-biology/experimental-methods/README.md) | [實驗設計](../data-science/statistics/experimental-design/README.md)（生物 vs 技術重複、批次） |
| 定序與 QC | [定序技術](genomics/sequencing-techniques/README.md)、[NGS 品質指標](genomics/ngs-qc/README.md) | — |
| 比對與檔案處理 | [檔案格式](genomics/file-formats/README.md)、[NGS 工具](bioinformatics-tools/ngs-tools/README.md) | [命令列資料處理](../computing/operating-system/command-line-data-processing.md)、[rsync](../computing/file-tools/file-transfer/rsync.md)、[MD5](../computing/file-tools/checksums/md5.md) |
| 統計分析 | [RNA-seq 分析](genomics/workflows/rna-seq/README.md)、[全基因體分析](genomics/genome-wide-analysis/README.md) | [統計（生資路線）](../data-science/statistics/README.md#建議路線)、[干擾與批次效應](../data-science/statistics/experimental-design/confounding-bias.md) |
| 判讀 | [遺傳學資料庫](genetics/databases/README.md)、[變異判讀](genetics/variant-interpretation/README.md) | [生醫 LLM](../data-science/llm/bio-and-medical-llm.md)（文獻探勘與限制） |
| 可重現性 | [RNA-seq：可重現性](genomics/workflows/rna-seq/10-reproducibility-and-troubleshooting.md) | [Nextflow](../computing/workflow-engines/nextflow/README.md)、[Conda](../computing/containers-and-env/conda.md)、[Docker](../computing/containers-and-env/docker/README.md)、[renv](../data-science/r-foundations/reproducible-environments-with-renv.md) |
