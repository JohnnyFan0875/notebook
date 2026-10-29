[Biology](../../README.md) › [遺傳學](../README.md) › 資料庫

# 遺傳學資料庫 (Genetics Databases)

不同資料庫回答不同問題。查一個基因或變異時，通常依序：確認正確的 ID → 疾病證據 → 族群頻率 → 功能預測與表現 → 特定領域（癌症、藥物）。

## 模組

| 模組 | 主要資料庫 | 回答的問題 |
| --- | --- | --- |
| [基因](gene/README.md) | HGNC、NCBI Gene、Ensembl、UCSC、GeneCards | 這個基因的正式名稱、位置、轉錄本是什麼？ |
| [基因–疾病關聯](gene-disease-association/README.md) | OMIM、ClinGen、GenCC、HPO、GeneReviews、PanelApp、HGMD | 這個基因與哪些疾病有關？證據多強？ |
| [變異](variant/README.md) | ClinVar、dbSNP、VEP、COSMIC、CIViC、GWAS Catalog、VarSome | 這個變異被怎麼判讀過？預測影響是什麼？ |
| [族群頻率](population-frequency/README.md) | gnomAD、1000 Genomes、TaiwanGenomes、HGVD、DGV | 這個變異在族群中多常見？ |
| [藥物基因體](pharmacogenomics/README.md) | ClinPGx（PharmGKB）、CPIC | 這個變異影響用藥嗎？ |
| [功能與表現](functional-expression/README.md) | GTEx、KEGG；蛋白質見 [分子生物學資料庫](../../molecular-biology/molecular-databases/README.md) | 基因在哪個組織表現？屬於哪條通路？蛋白質做什麼？ |

## 查詢流程

| 步驟 | 用 | 為什麼 |
| --- | --- | --- |
| 1. 確認基因 / 變異 | HGNC、NCBI Gene、Ensembl、dbSNP | 避免別名、過時符號、基因組版本錯誤 |
| 2. 統一變異寫法 | HGVS + MANE 轉錄本，見 [HGVS 命名](../variant-interpretation/hgvs-nomenclature.md) | 不同轉錄本的 `c.` 位置不同 |
| 3. 臨床證據 | ClinVar、OMIM、ClinGen、GenCC、GeneReviews | 區分經審閱的關聯與只是被提及 |
| 4. 族群頻率 | gnomAD、族群專屬資料庫（台灣、日本） | 太常見的變異不可能造成罕見孟德爾疾病 |
| 5. 功能證據 | VEP、in-silico 預測、UniProt、GTEx | 連到轉錄本、蛋白質結構、組織表現 |
| 6. 特定領域 | COSMIC、CIViC、ClinPGx、GWAS Catalog | 癌症、藥物反應、複雜疾病各有獨立的證據體系 |
| 7. 綜合判讀 | ACMG/AMP 準則 | 見 [ACMG/AMP 變異分級](../variant-interpretation/acmg-amp.md) |

> 不要把單一資料庫當最終證據：交叉核對 ID、基因組版本、轉錄本版本、表型用語與證據等級。需付費的資料庫（如 HGMD Professional）要在流程中註明版本與授權。查詢結果附上**查詢日期**，因為資料庫持續更新，同一變異的分類可能改變。

整合多個資料庫的工具（VarSome、MARRVEL、OpenCRAVAT）可快速瀏覽，但正式判讀仍應回到原始資料庫，見 [變異資料庫](variant/README.md)。
