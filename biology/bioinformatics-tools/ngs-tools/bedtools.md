[生資工具](../README.md) › [NGS 工具](README.md) › bedtools

# bedtools

基因體區間運算 (genome arithmetic) 工具：交集、合併、差集、覆蓋度、取序列。可吃 BED、GFF/GTF、VCF、BAM。格式與 0-based 座標見 [BED](../../genomics/file-formats/bed.md)。

## 想做 X → 指令

| 想做 | 指令 |
| --- | --- |
| 排序（多數指令的前提） | `bedtools sort -i in.bed`（或 `sort -k1,1 -k2,2n`） |
| 合併重疊 / 相鄰區間 | `bedtools merge -i sorted.bed` |
| 合併並收集名稱欄 | `bedtools merge -i sorted.bed -c 4 -o distinct`（`collapse` 保留重複） |
| A 中與 B 重疊的部分 | `bedtools intersect -a A.bed -b B.bed` |
| A 中「有」重疊的完整區間（各一次） | `bedtools intersect -a A.bed -b B.bed -u` |
| A 中「沒有」重疊的區間 | `bedtools intersect -a A.bed -b B.bed -v` |
| 同時輸出 A 與 B 的欄位 | `bedtools intersect -a A.bed -b B.bed -wa -wb` |
| 變異落在哪個基因 | `bedtools intersect -a variants.vcf.gz -b genes.bed -wa -wb` |
| 至少重疊 A 的 50% | `bedtools intersect -a A.bed -b B.bed -f 0.5`（`-r` 雙向） |
| 從 A 扣掉 B | `bedtools subtract -a A.bed -b B.bed` |
| 每個區域往外延伸 100 bp | `bedtools slop -i in.bed -g genome.txt -b 100` |
| 基因體中沒被覆蓋的區域 | `bedtools complement -i in.bed -g genome.txt` |
| 最近的基因與距離 | `bedtools closest -a peaks.bed -b genes.bed -d` |
| 目標區域的覆蓋度 | `bedtools coverage -a targets.bed -b sample.bam` |
| 取區域序列 | `bedtools getfasta -fi ref.fa -bed in.bed -name` |
| 切成固定大小的視窗 | `bedtools makewindows -g genome.txt -w 1000` |

`genome.txt` 是兩欄的「染色體 長度」，可從 `samtools faidx ref.fa` 產生的 `ref.fa.fai` 取前兩欄。

## 範例：panel 目標區域整理

```bash
# 1. 合併重疊的 amplicon，保留基因名稱（不重複）
bedtools sort -i amplicons.bed | bedtools merge -c 4 -o distinct > targets.bed
# chr12  25245274  25245395  KRAS

# 2. 每個目標區域往外加 10 bp padding
bedtools slop -i targets.bed -g GRCh38.genome -b 10 > targets.pad10.bed

# 3. 每個區域的覆蓋度：reads 數、有覆蓋的鹼基數、區域長度、覆蓋比例
bedtools coverage -a targets.pad10.bed -b sample.bam -sorted -g GRCh38.genome
```

`-sorted` 搭配排序過的輸入可大幅節省記憶體；此時兩個檔案的染色體順序必須和 `-g` 一致。

## 常見錯誤

| 錯誤 | 原因 / 修正 |
| --- | --- |
| 交集結果比預期多一行一行重複 | 預設每個重疊對輸出一次；只要 A 的區間各一次用 `-u` |
| 差 1 個鹼基 | BED 是 0-based、半開區間；VCF / GFF 是 1-based（bedtools 會自動轉換，手動轉檔時常出錯） |
| `merge` 結果怪 | 輸入沒排序 |
| `-sorted` 報錯 | 檔案間染色體順序不同（`chr10` 排在 `chr2` 前後的差異） |
| 某些染色體完全沒有結果 | 命名不一致（`chr1` vs `1`） |

R 的對應是 `GenomicRanges::findOverlaps()`（見 [Bioconductor](../bioconductor.md)）；Python 可用 pybedtools / pyranges。官方文件：[bedtools](https://bedtools.readthedocs.io/en/latest/)。
