# Biology 重整計畫與 Checklist

## Context

`biology/` 共 219 篇 `.md`（另有 `rna-seq/` 的 24 張圖、15 個腳本、5 個 CSV），**沒有任何一篇用過 `/rewrite-notes`**：全部沒有麵包屑、標題純英文、內文多為英文。主要問題：

1. **空殼**：約 70 篇只有 1–6 行（一句說明 + 網址，或只有一個連結，常沒有 H1），例如 OMIM、gnomAD、HGVS、Ensembl GTF、SNPNexus、blood-bank。
2. **重複**：`base-quality` vs `quality-score`；`liquid-biopsy/` 兩篇重疊；cytokines 散在 3 篇；`rnaseq-differential-expression-with-deseq2.md` 與 `rna-seq/06`、`07` 重疊；UniProt / InterPro / HPA 同時列在 genetics 與 molecular-biology；validation 散在 3 處。
3. **位置不對**：CIViC（癌症變異）放在 pharmacogenomics；NCCN（癌症治療指引）放在 PGx guidelines；GIAB 放在 genome-annotations；`de-novo-variant`、`vqsr` 放在 ngs-fundamentals；HGVS（命名規則）放在 variant databases；MSDS / COA 放在 regulatory-databases；`primer-design.md` 放在 sequencing-techniques、primer 工具卻在 bioinformatics-tools。
4. **層級過深 / 過碎**：`genomics/sequencing-and-analysis/` 多一層；`bioinformatics-tools/bioinformatics/`、`cancer-genomics/tcga/`、`sequencing-techniques/illumina/`、`molecular-biology/experimental-tools/`（1 篇）等單篇資料夾；三個 README 只有 `# 資料夾名`。
5. **缺口**（對生資讀者重要卻沒有）：ACMG/AMP 變異判讀、germline / somatic 變異呼叫流程、定序平台比較（短讀 vs 長讀、錯誤型態）、參考基因組版本與座標（GRCh37/38、chr 命名、GENCODE vs RefSeq）、in-silico 預測工具、scRNA-seq 流程概觀。
6. **錯誤 / 殘留**：`variant-allele-frequency.md` 把 VAF（樣本內）與族群等位基因頻率混用；`genetics/databases/README.md` 留有 `~/project/source.txt` 的工作筆記；`rna-seq/README.md` 寫死 `/home/johnny_fan/...` 路徑、目錄圖列了不存在的 `index.md`、註明「缺少 Rscript」（現在已有 R 4.6.1）。

目標：先做**結構整理（搬 → 併 → 修連結）**，讓每個主題只有一個家；再用 `/rewrite-notes` 分批改寫並補內容。

### 已決定（2026-10-29）

| 項目 | 決定 |
| --- | --- |
| 空殼資源檔 | **不刪**，逐篇補充成精簡資源卡或筆記；放錯位置的搬移或整合 |
| 純連結 / 低價值檔 | **不刪**；評估是否值得展開，值得就補充；只有連結的先看網站，整理相關資訊並附上連結 |
| `genomics/sequencing-and-analysis/` | 攤平到 `genomics/` 下 |
| 資料庫位置 | 依領域保留、去重：蛋白質資料庫只放 `molecular-biology/molecular-databases/`，`genetics/databases/README.md` 當總查詢流程頁 |

## 通用規則

- 搬移一律 `git mv`；合併時把被併檔的獨特內容貼進目標檔，再 `git rm` 被併檔。
- 每搬 / 併一個檔，`Grep` 整個 notebook 找舊路徑並修正連入（含 `#anchor`）；已知外部連入見附錄。
- 改寫一律用 `/rewrite-notes`；資源卡型保持短（標題 + 一句用途 + `| 項目 | 內容 |` 小表），同類多個時在 README 放比較表。
- 只有連結的檔：用 WebFetch 看網站，整理「是什麼、收錄什麼、何時用」，附上連結；網站無法存取就保留連結並在回報中列出。
- 版本號、收錄數量、網址等時效資訊以官方網站為準，不憑記憶。
- 每階段 / 每批結束跑連結檢查，零錯誤才 commit（分支 `bio-rewrite`，完成後 `--no-ff` 合併回 master）：
  ```bash
  uv run --no-project ".claude/skills/rewrite-notes/check_links.py" biology
  uv run --no-project ".claude/skills/rewrite-notes/check_links.py" .
  ```

---

## Phase 0：準備

- [x] `git status` 乾淨，從 master 開分支 `bio-rewrite`

## Phase 1：結構搬移（只搬不改內容）

**攤平 genomics**
- [x] `genomics/sequencing-and-analysis/*` → `genomics/`（`file-format/` 改名 `file-formats/`、`ngs-fundamentals/` 改名 `ngs-qc/`）；刪除 `sequencing-and-analysis/README.md`（內容併入 `genomics/README.md`）
- [x] `genomics/genome-annotations/` + `genomics/sequencing-repositories/` → `genomics/reference-data/`
- [x] `genomics/cancer-genomics/tcga/tcga.md` → `genomics/cancer-genomics/tcga-gdc.md`（刪 `tcga/README.md`）
- [x] `genomics/sequencing-techniques/illumina/color-chemistry.md` → 暫放 `genomics/sequencing-techniques/`（Phase 2 併入定序平台）
- [x] `genomics/sequencing-and-analysis/commercial-panel.md` → `genomics/sequencing-techniques/targeted-panels.md`
- [x] `genomics/workflows/ngs-verification-validation.md`、`validation-verification/` → `genomics/assay-validation/`
- [x] `genomics/population-variation/database-of-genomic-variants.md` → `genetics/databases/population-frequency/dgv.md`

**bioinformatics-tools**
- [x] `bioinformatics-tools/bioinformatics/` 拆成 `ngs-tools/`（samtools、bcftools、bedtools、tabix、sambamba、picard、fastqc、fastp、repeatmasker）與 `primer-design/`（primer3、primerpooler、oligoevaluator、ucsc-in-silico-pcr）
- [x] `genomics/sequencing-techniques/primer-design.md` → `bioinformatics-tools/primer-design/README.md` 的設計準則
- [x] `genomics/workflows/bioconductor-introduction.md` → `bioinformatics-tools/bioconductor.md`
- [x] `bioinformatics-tools/bioinformatics/prediction-tools.md` → `genetics/variant-interpretation/in-silico-prediction.md`

**genetics**
- [x] `genetics/guidelines/` → `genetics/variant-interpretation/`（acgs、clingen-guidelines）；`guidelines/pharmacogenomics/cpic.md` → `genetics/databases/pharmacogenomics/`；`nccn.md` → `genomics/cancer-genomics/`
- [x] `genetics/databases/pharmacogenomics/civic.md` → `genetics/databases/variant/`（癌症變異，與 COSMIC、PMKB 同層）
- [x] `genetics/databases/variant/hgvs.md` → `genetics/variant-interpretation/hgvs-nomenclature.md`
- [x] `genetics/databases/variant/gwas.md` → `gwas-catalog.md`
- [x] `genomics/ngs-qc/de-novo-variant.md` → `genetics/foundations/`

**其他**
- [x] `clinical-informatics-and-standards/regulatory-databases/material-safety-and-quality/` → `laboratory-medicine/material-safety-and-quality/`
- [x] `molecular-biology/detection-and-assays/`、`experimental-tools/` 併入 `molecular-biology/experimental-methods/`
- [x] 全 notebook 修連入（含 data-science 約 25 個）→ 連結檢查 → commit `Restructure biology: phase 1 moves`

## Phase 2：合併重複

> 合併後的檔案都要整篇改寫，所以每項合併**在 Phase 3 對應批次內一起做**（合併 → 改寫 → 修連入），不先粗略拼接。各項標註所屬批次。

- [x] `genomics/ngs-qc/base-quality.md` + `quality-score.md` → `base-quality-scores.md`
- [x] `genomics/ngs-qc/vqsr.md` → 併入新的 `genomics/workflows/variant-calling.md`（Phase 3 批次 5 補全）
- [x] `liquid-biopsy/cfdna-ctc.md` + `cfdna-ctdna.md` → `genomics/sequencing-techniques/liquid-biopsy.md`
- [x] `color-chemistry.md`、`enseqlopedia.md` → 新的 `genomics/sequencing-techniques/sequencing-platforms.md`
- [x] `cancer-genomics/mutational-signatures/` 3 篇 → `mutational-signatures.md`
- [x] `workflows/rnaseq-differential-expression-with-deseq2.md` → 獨特內容（size factors、vst / rlog、`lfcShrink`、常見錯誤）併入 `rna-seq/06`、`07`；更新 data-science 的 2 個連入與 `#pca-for-sample-structure` anchor
- [x] `genomics/reference-data/`：7 個 annotation / FASTA 空殼 + `download-exon-from-fasta.md` → `reference-genomes.md`（UCSC / Ensembl / NCBI 版本、chr 命名、下載）與 `gene-annotations.md`（GTF / GFF、GENCODE、RefSeq、refGene）；`ncbi-reference-standard.md`（GIAB）→ `genomics/assay-validation/reference-standard.md`；`ena.md` → `raw-data-repositories.md`（SRA / ENA / GEO）
- [x] immunology：cytokine 內容統一到 `cytokines.md`（`cytokine-network-summary.md` 改寫），T / B 細胞筆記只留亞群並連過去
- [x] `genetics/databases/functional-expression/README.md`：UniProt / InterPro / HPA 只保留連結，不重複描述
- [x] `workflows/pmbio.md` → `genomics/README.md` 的學習資源表
- [x] 連結檢查 → commit `Restructure biology: phase 2 merges`

## Phase 3：`/rewrite-notes` 分批改寫與補充

每批：讀範例 → 改寫 → 補內容 / 補圖 → 連結檢查 → commit `Rewrite biology: batch N <範圍>`。

- [x] **批次 1　bioinformatics-tools**（約 18 篇）：ngs-tools 依任務整理（「想做 X → 指令」）、bioconductor、primer-design（README 放設計準則表）、visualization；空殼工具補用途與替代方案
- [x] **批次 2　genomics 基礎**（約 16 篇）：`file-formats/`（補 FASTA、GTF/GFF）、`reference-data/`、`ngs-qc/`（補圖：Phred 分數、覆蓋度分布、GC bias）
- [x] **批次 3　定序技術與驗證**（約 10 篇）：新增 `sequencing-platforms.md`（Illumina / ONT / PacBio、錯誤型態 → QC 指標）、chip-seq、liquid-biopsy、targeted-panels、single-cell（README 補 scRNA-seq 流程，連 data-science 的 AnnData / scanpy）、`assay-validation/`
- [x] **批次 4　RNA-seq**（12 篇）：`rna-seq/` 系列 + `limma-differential-expression.md`；移除寫死路徑；資料與圖保留在 `data/`、`src/`
- [x] **批次 5　變異呼叫、全基因體分析、癌症基因體**（約 12 篇）：新增 `workflows/variant-calling.md`（比對 → 去重 → BQSR → HaplotypeCaller / Mutect2 → VQSR / hard filter → VEP）；GWAS / QTL / colocalization；TCGA / GDC、mutational signatures、NCCN
- [x] **批次 6　genetics 資料庫 I**（約 17 篇）：gene、population-frequency（gnomAD、TaiwanGenomes、DGV…）、functional-expression、pharmacogenomics（PharmGKB + CPIC）
- [x] **批次 7　genetics 資料庫 II**（約 25 篇）：variant（ClinVar、dbSNP、VEP、COSMIC、CIViC、VarSome…）、gene-disease-association（OMIM、HPO、ClinGen、GenCC、PanelApp…）
- [x] **批次 8　genetics 基礎與變異判讀**（約 10 篇）：修正 VAF 與族群頻率的混用；新增 `variant-interpretation/acmg-amp.md`（criteria 表、證據組合規則、ClinGen SVI 調整）；HGVS、in-silico 預測、ACGS、ClinGen 指引
- [ ] **批次 9　clinical-informatics**（約 25 篇）：clinical-terminology（FHIR、OMOP、SNOMED、ICD、LOINC…，補比較與對應關係）、clinical-databases、regulatory-databases
- [ ] **批次 10　immunology、laboratory-medicine、medical-imaging**（約 16 篇）：細胞激素整合；影像模態比較表（連 data-science 的 image-analysis）；blood-bank 依網站內容補充
- [ ] **批次 11　molecular-biology、microbiome**（約 20 篇）：實驗方法比較（blot 類型、qPCR 定量）、蛋白質資料庫、16S vs shotgun
- [ ] **批次 12　頂層與跨領域**：`biology/README.md`（模組表、建議路線、速查頁）、各領域 README 補漏、biology ↔ data-science / computing 交叉連結

## Phase 4：程式碼實跑驗證

- [ ] 安裝 Bioconductor 套件（DESeq2、edgeR、limma、tximport、clusterProfiler、GenomicRanges、Biostrings、ShortRead），實跑 `rna-seq/scripts/*.R` 與 bioconductor、limma、chip-seq 筆記中的範例（R 4.6.1 在 `C:\Users\johnnyfan\AppData\Local\Programs\R\R-4.6.1`）
- [x] 重跑 `scripts/simulate_rnaseq_demo.py`，確認圖與文字數字一致
- [ ] Shell 腳本（STAR、salmon、fastp…）無法在本機跑，核對參數與官方文件
- [ ] 連結檢查 → commit

## 完成後

- [ ] 合併 `bio-rewrite` 回 master，刪除本檔

## 附錄：biology 外部的連入（搬檔 / 改標題時必查）

| 目標（目前路徑，`biology/` 之後） | 次數 | 含 anchor |
| --- | --- | --- |
| `genomics/sequencing-and-analysis/workflows/bioconductor-introduction.md` | 5 | |
| `genomics/sequencing-and-analysis/workflows/rna-seq/06–09` | 9 | `#experimental-design`、`#count-models`、`#multiple-testing`、`#functional-enrichment`、`05#low-expression-filtering` |
| `genomics/sequencing-and-analysis/workflows/rnaseq-differential-expression-with-deseq2.md` | 3 | `#pca-for-sample-structure` |
| `genomics/sequencing-and-analysis/workflows/limma-differential-expression.md` | 2 | |
| `genomics/sequencing-and-analysis/genome-wide-analysis/`（gwas、eqtl、qtl） | 5 | `qtl-analysis-and-mapping.md#相關統計方法` |
| `genomics/sequencing-and-analysis/sequencing-techniques/`（single-cell README、chip-seq） | 3 | `chip-seq.md#diffbind-workflow` |
| `genomics/sequencing-and-analysis/file-format/vcf.md` | 1 | |
| `genetics/databases/`（clinvar、hpo、ncbi-gene、hgnc） | 4 | |
| `molecular-biology/molecular-databases/`（uniprot、interpro） | 3 | |
| `clinical-informatics-and-standards/`（ontology-lookup-service、uk-biobank） | 2 | |
| `medical-imaging/README.md`、`README.md` | 3 | |

來源多在 `data-science/`（statistics、r-foundations、python-foundations、image-analysis、machine-learning）；改動後用 `Grep "biology/"` 全面確認。
