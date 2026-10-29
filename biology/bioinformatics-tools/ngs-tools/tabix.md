[生資工具](../README.md) › [NGS 工具](README.md) › tabix

# tabix

替**依座標排序、BGZF 壓縮**的 tab 分隔檔（VCF、BED、GFF、SAM）建 `.tbi` 索引，之後可以直接用座標查詢，不必解壓整個檔案。屬於 HTSlib，與 `bgzip` 一起安裝。

## 建索引

```bash
# 1. VCF：bgzip 壓縮 → 排序 → 索引
bgzip in.vcf                                       # 產生 in.vcf.gz（不是 gzip！）
bcftools sort in.vcf.gz -Oz -o in.sorted.vcf.gz
tabix -p vcf in.sorted.vcf.gz                      # 產生 .tbi

# 2. BED / GFF：先用 sort 排序
sort -k1,1 -k2,2n regions.bed | bgzip > regions.bed.gz
tabix -p bed regions.bed.gz
(grep '^#' genes.gff3; grep -v '^#' genes.gff3 | sort -k1,1 -k4,4n) | bgzip > genes.gff3.gz
tabix -p gff genes.gff3.gz
```

| 參數 | 意義 |
| --- | --- |
| `-p vcf / bed / gff / sam` | 預設格式（決定哪幾欄是染色體、起點、終點） |
| `-s -b -e` | 自訂欄位（任意 tab 檔）：染色體 / 起點 / 終點欄 |
| `-0` | 起點欄為 0-based（`-p bed` 已自動處理） |
| `-C` | 建 `.csi` 索引：染色體長度超過 2²⁹（約 512 Mb，例如某些植物基因體）時必須用 |
| `-f` | 覆寫既有索引 |

VCF 也可以用 `bcftools index -t`（等同 tabix）或 `bcftools index`（預設建 `.csi`）。

## 查詢

```bash
tabix in.vcf.gz chr11                       # 整條染色體
tabix in.vcf.gz chr11:123456                # 單一位置
tabix in.vcf.gz chr11:123456-124000         # 區間（1-based、含頭尾）
tabix -h in.vcf.gz chr11:123456-124000      # 連 header 一起輸出（才是合法 VCF）
tabix -R targets.bed in.vcf.gz              # 用 BED 檔指定多個區域
tabix -l in.vcf.gz                          # 列出索引中的染色體名稱
```

| 注意 | 說明 |
| --- | --- |
| 染色體名稱要完全一致 | `chr11` 與 `11` 不同；先 `tabix -l` 確認 |
| `.tbi` 要和檔案放在一起 | 檔名為 `<file>.gz.tbi` |
| 輸出到 stdout | 存檔要自己導向；沒加 `-h` 的輸出缺 header |
| 未排序會報錯 | `[E::hts_idx_push] Unsorted positions`；先排序再壓縮 |

相關：[bcftools 的建索引流程](bcftools.md#指令速查)、[samtools index](samtools.md)（BAM / CRAM）、[座標系統 0-based vs 1-based](../../genomics/file-formats/zero-one-based.md)。官方文件：[HTSlib tabix](https://www.htslib.org/doc/tabix.html)。
