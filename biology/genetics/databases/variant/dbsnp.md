[資料庫](../README.md) › [變異](README.md) › dbSNP

# dbSNP

NCBI 的短變異資料庫（SNV、小 indel、MNV），為每個位置的變異給一個 rsID（如 `rs113488022`）。rsID 只是**識別碼**，不代表常見或良性。

| 項目 | 內容 |
| --- | --- |
| 網站 | [ncbi.nlm.nih.gov/snp](https://www.ncbi.nlm.nih.gov/snp/) |
| 下載 | [FTP latest_release/VCF](https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/)（染色體名稱為 RefSeq accession，如 `NC_000007.14`） |
| 何時用 | rsID ↔ 座標轉換；補 VCF 的 ID 欄；連到 ClinVar、gnomAD、文獻 |

| 注意 | 說明 |
| --- | --- |
| 一個 rsID 可能有多個等位基因 | 例：同一位置 A>G 與 A>T 共用 rsID；比對時要同時看 REF / ALT |
| rsID 會合併 / 撤銷 | 舊 rsID 被合併到新的，查詢時用最新版本 |
| 版本座標 | 同一 rsID 在 GRCh37 / GRCh38 位置不同 |
| 不是頻率資料庫 | 頻率看 [gnomAD](../population-frequency/gnomad.md)；dbSNP 收錄的也包含致病變異 |

補 rsID 的實作見 [bcftools：補上 dbSNP rsID](../../../bioinformatics-tools/ngs-tools/bcftools.md#範例補上-dbsnp-rsid)。
