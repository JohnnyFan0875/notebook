[分子生物學](../README.md) › [分子資料庫](README.md) › UniProt

# UniProt

全球蛋白質序列與功能註解的中心資料庫，由 EMBL-EBI、SIB、PIR 共同維護。基因 → 蛋白的功能、結構域、轉譯後修飾、疾病關聯，多數工具（VEP、AlphaFold DB、InterPro）都以 UniProt accession 為索引。

| 項目 | 內容 |
| --- | --- |
| 入口 | [uniprot.org](https://www.uniprot.org/)；REST API `rest.uniprot.org` |
| 組成 | UniProtKB（Swiss-Prot + TrEMBL）、UniRef（序列聚類）、UniParc（所有序列的非冗餘存檔）、Proteomes |
| 規模 | release 2026_01：Swiss-Prot 約 57 萬筆、TrEMBL 約 2 億筆（每約 8 週更新，以官網為準） |
| 授權 | CC BY 4.0 |
| 替代 / 互補 | [InterPro](interpro.md)（結構域）、RefSeq Protein、neXtProt（人類蛋白） |

## Swiss-Prot vs TrEMBL

| | Swiss-Prot（reviewed） | TrEMBL（unreviewed） |
| --- | --- | --- |
| 註解 | 人工審閱文獻 | 自動註解 |
| 冗餘 | 每個基因一筆，isoform 併在同一筆 | 可能多筆 |
| 用法 | 分析與解讀優先選 | 涵蓋 Swiss-Prot 沒有的物種與序列 |

## 常用欄位與用途

| 想知道 | 看哪裡 |
| --- | --- |
| 標準序列 / isoform | Sequence：canonical isoform 與其他 isoform（與 Ensembl / RefSeq 轉錄本的對應見 Cross-references） |
| 變異落在哪個區域 | Family & Domains、Features：domain、motif、active site、binding site |
| PTM 位點 | PTM / Processing：磷酸化、糖基化、訊號肽、雙硫鍵 |
| 疾病關聯 | Disease & Variants：OMIM 疾病、已知自然變異 |
| 結構 | Structure：PDB 與 AlphaFold 模型連結 |

```python
import requests

# 依基因名查人類 reviewed 條目，取 accession 與序列長度
r = requests.get("https://rest.uniprot.org/uniprotkb/search", params={
    "query": "gene_exact:TP53 AND organism_id:9606 AND reviewed:true",
    "fields": "accession,gene_names,length", "format": "tsv"})
print(r.text)          # P04637  TP53  393

fasta = requests.get("https://rest.uniprot.org/uniprotkb/P04637.fasta").text
```

> UniProt 的蛋白座標以 canonical isoform 為準，HGVS 的 `p.` 註解可能依另一個轉錄本，比對前先確認 isoform。蛋白語言模型（ESM 等）多以 UniRef 為訓練資料，見[序列與蛋白質模型](../../../data-science/deep-learning/bio-applications/sequence-and-protein-models.md)。
