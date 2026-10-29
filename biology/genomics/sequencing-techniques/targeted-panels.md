[基因體學](../README.md) › [定序技術](README.md) › 標靶定序

# 標靶定序與基因 panel (Targeted Sequencing & Gene Panels)

只定序感興趣的區域，用同樣成本換到更高深度。選擇的範圍（panel、全外顯子、全基因組）與捕捉方式決定能偵測哪些變異、會漏掉哪些。

## WGS vs WES vs panel

| | Panel | WES（全外顯子） | WGS（全基因組） |
| --- | --- | --- | --- |
| 範圍 | 數個到數百個基因 | 約 2 萬個基因的 exon（~1–2% 基因組，30–60 Mb） | 全部 |
| 常見深度 | 200–1,000×（腫瘤 / cfDNA 更高） | 100× | 30× |
| 偵測 SNV / 小 indel | ✓（深度最高，可抓低頻） | ✓ | ✓ |
| CNV | 有限（依設計） | 中等（受捕捉不均勻影響） | ✓（最均勻） |
| 結構變異、intron / 調控區 | ✗ | ✗ | ✓（短讀仍有盲區） |
| 偶然發現 (incidental findings) | 少 | 多 | 最多 |
| 再分析 | 只能看 panel 內 | 可隨新知重新分析 | 可 |
| 適用 | 症狀明確、已知基因；腫瘤熱點；成本敏感 | 罕病診斷首選之一 | 罕病、研究、需要 SV / CNV |

## 捕捉方式

| | Amplicon（擴增子） | Hybrid capture（雜交捕捉） |
| --- | --- | --- |
| 原理 | 多重 PCR 擴增目標 | 生物素化 probe 拉下目標片段 |
| 適合規模 | 小到中型 panel（數十至數百 amplicon） | 中大型 panel、WES |
| 起始量 / 時間 | 低、快 | 較高、較慢 |
| 均勻度 | 較差（各 amplicon 效率不同） | 較好 |
| 重複標記 | **不能做**（所有 reads 起點相同） | 可以 |
| 限制 | 引子下的 SNP 造成 allele dropout；大缺失、融合基因難偵測 | off-target reads；GC 極端區覆蓋差 |
| 品質指標 | amplicon 覆蓋均勻度、primer dimer 比例 | on-target 比例、fold-80、重複率 |

> Amplicon panel 要在分析時修掉 primer 序列；否則 primer 區的真實變異會被 primer 序列「蓋掉」。多重引子的設計與分組見 [引子設計](../../bioinformatics-tools/primer-design/README.md)、[PrimerPooler](../../bioinformatics-tools/primer-design/primerpooler.md)。

## 設計 panel 時要考慮

| 項目 | 說明 |
| --- | --- |
| 基因清單 | 依疾病證據挑選，參考下方公共資源；避免納入證據薄弱的基因（增加 VUS） |
| 目標區域 | exon ± 10–20 bp（含剪接位點）、已知致病的深層 intron 變異、熱點 |
| 轉錄本 | 以 [MANE Select](../reference-data/gene-annotations.md#mane臨床報告的預設轉錄本) 定義 exon |
| 難區域 | 假基因、片段重複、高 GC 區，需另外驗證或註明限制 |
| 品質要求 | 最低深度（如 ≥ 20×）的目標比例，見 [深度與覆蓋度](../ngs-qc/sequencing-depth-coverage.md) |
| 確效 | 用參考標準品評估敏感度、精確度，見 [檢測確效](../assay-validation/README.md) |

## 查 panel 內容的資源

| 資源 | 內容 | 何時用 |
| --- | --- | --- |
| [Genomics England PanelApp](https://panelapp.genomicsengland.co.uk/) | 專家審閱的疾病 panel，基因以綠 / 黃 / 紅標示證據等級 | 決定 panel 應包含哪些基因 |
| [ClinGen Gene-Disease Validity](https://search.clinicalgenome.org/kb/gene-validity) | 基因–疾病關聯的證據分級（Definitive → Refuted） | 判斷某基因是否該納入 |
| [NCBI GTR](https://www.ncbi.nlm.nih.gov/gtr/) | 全球實驗室登錄的基因檢測（含 panel 基因清單） | 比較各實驗室的 panel |
| [Mayo Clinic Laboratories 檢驗目錄](https://www.mayocliniclabs.com/test-catalog) | 臨床檢驗項目與方法說明 | 參考大型臨床實驗室的設計 |

## 商業檢測服務（參考）

| 公司 | 主要領域 |
| --- | --- |
| [GeneDx](https://providers.genedx.com/tests)、[Invitae](https://www.invitae.com/us/providers/test-catalog)、[Ambry Genetics](https://www.ambrygen.com/)、[Prevention Genetics](https://www.preventiongenetics.com/tests/all)、[Fulgent Genetics](https://www.fulgentgenetics.com/products/disease/raredisease.html) | 美國：遺傳疾病、遺傳性癌症 panel、WES |
| [Blueprint Genetics](https://blueprintgenetics.com/)、[CeGaT](https://cegat.com/diagnostics/diagnostic-methods/panel-diagnostics/)、[Centogene](https://www.centogene.com/diagnostics/ngs-panels/)、[Breda Genetics](https://bredagenetics.com/product-category/panels/)、[Igenomix](https://www.igenomix.eu/genomics-precision-diagnostic/panels-specialities/) | 歐洲：罕病 panel；Igenomix 偏生殖醫學 |
| [Knight Diagnostic Laboratories](https://knightdxlabs.ohsu.edu/)、[LabCorp](https://www.labcorp.com/test-menu/new-updated) | 學術 / 大型臨床實驗室 |
| [Natera](https://www.natera.com/) | 產前 (NIPT)、移植、腫瘤 MRD |
| [Sophia Genetics](https://www.sophiagenetics.com/sophia-ddm-for-genomics/)、[Paragon Genomics](https://www.paragongenomics.com/custom-ngs-amplicon-panels/) | 分析平台 / 客製化 amplicon panel 試劑 |
| [訊聯基因數位](https://www.gga.asia/tc/index) | 台灣 |

> 商業 panel 的基因清單會隨時間更新；引用時記錄查詢日期與版本。

相關：[定序平台](sequencing-platforms.md)、[基因–疾病關聯資料庫](../../genetics/databases/gene-disease-association/README.md)。
