[生資工具](../README.md) › [NGS 工具](README.md) › bcftools

# bcftools

處理 [VCF](../../genomics/file-formats/vcf.md) / BCF 的標準工具：檢視、過濾、正規化、合併、加註解、查詢。多數指令要求輸入已 **bgzip 壓縮並建索引**（見 [tabix](tabix.md)）。

## 指令速查

| 想做 | 指令 |
| --- | --- |
| 壓縮 + 排序 + 索引 | `bgzip in.vcf` → `bcftools sort in.vcf.gz -Oz -o s.vcf.gz` → `bcftools index -t s.vcf.gz` |
| 只看 header / 樣本名 | `bcftools view -h in.vcf.gz`、`bcftools query -l in.vcf.gz` |
| 取區域 | `bcftools view -r chr1:10000-20000 in.vcf.gz`（`-R regions.bed` 用檔案） |
| 取樣本 | `bcftools view -s S1,S2 in.vcf.gz -Oz -o sub.vcf.gz` |
| 只留 PASS / SNV / indel | `bcftools view -f PASS`、`-v snps`、`-v indels` |
| 依條件保留 / 排除 | `bcftools view -i 'QUAL>=30 && INFO/DP>=10'`、`-e '...'` |
| 不刪、只標記 FILTER | `bcftools filter -s LowQual -e 'QUAL<20 \|\| INFO/DP<10'` |
| 拆多等位、左對齊 | `bcftools norm -m -any -f ref.fa in.vcf.gz -Oz -o norm.vcf.gz` |
| 多個樣本合成一個 VCF | `bcftools merge a.vcf.gz b.vcf.gz -Oz -o merged.vcf.gz` |
| 同樣本不同區段接起來 | `bcftools concat chr1.vcf.gz chr2.vcf.gz -Oz -o all.vcf.gz` |
| 兩個 VCF 的交集 / 差集 | `bcftools isec -p out_dir a.vcf.gz b.vcf.gz` |
| 轉成表格 | `bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL[\t%GT]\n' in.vcf.gz` |
| 統計（Ts/Tv、各類變異數） | `bcftools stats in.vcf.gz > stats.txt` |
| 改染色體名稱 | `bcftools annotate --rename-chrs map.txt` |
| 從另一個 VCF 補 ID / INFO | `bcftools annotate -a dbsnp.vcf.gz -c ID` |
| 拆 VEP 的 CSQ 欄位 | `bcftools +split-vep -f '%CHROM\t%POS\t%SYMBOL\t%Consequence\n' in.vcf.gz` |

| 參數 | 意義 |
| --- | --- |
| `-O z / b / v / u` | 輸出 bgzip VCF / BCF / 純文字 VCF / 未壓縮 BCF（管線中間步驟用 `u` 最快） |
| `-o FILE` | 輸出檔 |
| `-W` | 輸出時順便建索引（1.17 起；`-W=tbi` 產生 `.tbi`） |
| `--threads N` | 壓縮 / 解壓用的執行緒 |
| `-i` / `-e` | include / exclude 表達式；`INFO/DP` 與 `FORMAT/DP` 要寫清楚來源 |

> **`merge` vs `concat`**：`merge` 合併「不同樣本」（欄變多）；`concat` 接起「同一批樣本的不同區段」（列變多）。用錯會得到重複或缺漏。

## 範例：補上 dbSNP rsID

dbSNP 的 VCF（[NCBI FTP](https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/)）用 RefSeq accession 當染色體名（`NC_000011.10`），使用者 VCF 多為 `chr11`，要先統一名稱。

```bash
# 1. 確認兩邊的染色體命名
bcftools view -h GCF_000001405.40.gz | grep '^##contig' | head
bcftools view -h sample.vcf.gz | grep '^##contig' | head

# 2. 對照表（兩欄、tab 分隔）：舊名 新名
#    chr1   NC_000001.11
#    chr11  NC_000011.10
bcftools annotate --rename-chrs chrom_map.txt sample.vcf.gz -Oz -o sample.renamed.vcf.gz
bcftools index -t sample.renamed.vcf.gz

# 3. 從 dbSNP 補 ID 欄
bcftools annotate -a GCF_000001405.40.gz -c ID sample.renamed.vcf.gz -Oz -o sample.rsid.vcf.gz
```

> 注意版本：`NC_000011.10` 是 GRCh38、`NC_000011.9` 是 GRCh37。dbSNP 檔名中的 `GCF_000001405.40` 對應 GRCh38.p14、`.25` 對應 GRCh37.p13，必須與樣本的參考基因體一致，見 [參考基因組](../../genomics/reference-data/README.md)。

## 範例：過濾與正規化

```bash
# 1. 拆多等位 + 左對齊（比對資料庫前一定要做，否則同一個 indel 有多種寫法）
bcftools norm -m -any -f GRCh38.fa raw.vcf.gz -Ou \
  | bcftools filter -s LowQual -e 'QUAL<30 || FORMAT/DP<10' -Oz -o filtered.vcf.gz
bcftools index -t filtered.vcf.gz

# 2. 只取通過的 SNV，轉成表格
bcftools view -f PASS -v snps filtered.vcf.gz \
  | bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%GT:%AD]\n' > pass_snvs.tsv
```

硬過濾的閾值與 VQSR 的取捨見 [VQSR vs Hard Filtering](../../genomics/workflows/variant-calling.md#變異過濾vqsr-vs-硬過濾)。

## 常見錯誤

| 錯誤訊息 / 現象 | 原因 / 修正 |
| --- | --- |
| `the file is not BGZF compressed` | 用了 `gzip`；改用 `bgzip` |
| `could not load index` | 沒建索引，或索引比 VCF 舊；重跑 `bcftools index -t` |
| `annotate` 補不到 ID | 染色體名稱或基因體版本不一致；或 indel 沒有先 `norm` |
| `merge` 報 header 衝突 | INFO / FORMAT 定義不同；加 `--force-samples` 前先確認是否真的是不同樣本 |
| 條件 `DP<10` 結果怪 | 同時有 `INFO/DP` 與 `FORMAT/DP`；明確寫出來源 |
