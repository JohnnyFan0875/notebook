[Biology](../README.md) › 基因體學

# 基因體學 (Genomics)

從定序資料到生物學結論：檔案格式、參考資料、品質指標、定序技術、分析流程、全基因體關聯與癌症基因體。變異的臨床判讀與資料庫見 [遺傳學](../genetics/README.md)；工具指令見 [生資工具](../bioinformatics-tools/README.md)。

## 建議順序

```
檔案格式 → 參考資料 → NGS 品質指標 → 定序技術 → 分析流程（RNA-seq、變異呼叫）→ 全基因體分析 / 癌症基因體
```

## 模組

| 模組 | 內容 | 回答的問題 |
| --- | --- | --- |
| [檔案格式](file-formats/README.md) | FASTA、FASTQ、BAM、VCF、BED、GTF、座標系統 | 每個檔案裝什麼？座標怎麼算？ |
| [參考資料](reference-data/README.md) | 參考基因組、基因註解、公開原始資料 | 用哪個版本？去哪裡下載？ |
| [NGS 品質指標](ngs-qc/README.md) | 鹼基品質、MAPQ、重複率、深度、均勻度、GC 偏差 | 資料品質夠嗎？ |
| [定序技術](sequencing-techniques/README.md) | 定序平台、panel、ChIP-seq、液態切片、單細胞 | 該選哪種技術？各有什麼偏差？ |
| [分析流程](workflows/README.md) | RNA-seq、變異呼叫、limma | 從原始資料到結果的步驟？ |
| [檢測確效](assay-validation/README.md) | validation vs verification、參考標準品、GIAB | 檢測方法可靠嗎？ |
| [全基因體分析](genome-wide-analysis/README.md) | GWAS、eQTL / sQTL / pQTL、colocalization | 哪些變異與性狀或表現量有關？ |
| [癌症基因體](cancer-genomics/README.md) | TCGA / GDC、突變特徵、NCCN | 腫瘤的突變型態與資料資源？ |

## 學習資源

| 資源 | 內容 |
| --- | --- |
| [Precision Medicine Bioinformatics (pmbio)](workflows/pmbio.md) | 從定序資料到臨床解讀的精準醫療生資課程 |

統計方法（多重檢定、計數模型、PCA、批次效應）見 [data-science：統計](../../data-science/statistics/README.md)。
