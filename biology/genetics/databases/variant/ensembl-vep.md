[資料庫](../README.md) › [變異](README.md) › Ensembl VEP

# Ensembl VEP (Variant Effect Predictor)

把變異對到基因、轉錄本、蛋白與調控區，預測後果（missense、frameshift、splice 等），並可同時加上 ClinVar、gnomAD、in-silico 分數等註解。VEP 給的是**預測的分子後果**，不是臨床分類。

| 存取 | 用途 |
| --- | --- |
| [網頁版](https://www.ensembl.org/Tools/VEP) | 少量變異 |
| 命令列 + 離線 cache | 批次、可重現（[文件](https://www.ensembl.org/info/docs/tools/vep/index.html)） |
| REST API | 程式化查詢 |

```bash
vep -i in.vcf.gz -o out.vcf --vcf --offline --cache --assembly GRCh38 \
    --everything --mane --pick_allele_gene \
    --plugin SpliceAI,snv=spliceai_snv.vcf.gz,indel=spliceai_indel.vcf.gz \
    --plugin REVEL,file=revel.tsv.gz --plugin LoF,loftee_path:...
# --everything：SIFT、PolyPhen、gnomAD 頻率、HGVS、canonical / MANE 標記…
# --pick / --pick_allele_gene：每個變異（或每個基因）只輸出一個最具代表性的轉錄本
```

## 輸出

| 欄位 | 意義 |
| --- | --- |
| Consequence | Sequence Ontology 術語（`missense_variant`、`stop_gained`、`splice_donor_variant`…） |
| IMPACT | HIGH（LoF 類）、MODERATE（missense、框內 indel）、LOW（同義）、MODIFIER（非編碼） |
| HGVSc / HGVSp | `c.` / `p.` 命名 |
| MANE_SELECT | 是否為 MANE 轉錄本 |
| 外掛分數 | SpliceAI、REVEL、CADD、AlphaMissense、LOFTEE 等（見 [in-silico 預測](../../variant-interpretation/in-silico-prediction.md)） |

> 一個變異對每個重疊的轉錄本都有一列結果；在 exon 邊界或多 isoform 的基因上，不同轉錄本的後果可能不同（missense vs intron）。報告時固定使用 MANE Select 並記錄 VEP 版本、cache 版本、基因組版本與外掛版本。輸出可用 `bcftools +split-vep` 拆成表格（見 [bcftools](../../../bioinformatics-tools/ngs-tools/bcftools.md)）。

替代工具：ANNOVAR（表格輸出、資料庫多，學術免費需註冊）、SnpEff / SnpSift。
