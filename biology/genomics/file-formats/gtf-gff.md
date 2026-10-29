[基因體學](../README.md) › [檔案格式](README.md) › GTF / GFF3

# GTF / GFF3

描述基因結構（gene → transcript → exon / CDS / UTR）的註解格式，是 RNA-seq 計數、比對索引、變異註解的必要輸入。兩者都是 9 欄 tab 分隔、**1-based 閉區間**；差別在第 9 欄的寫法與階層表示。

## 9 個欄位

```text
chr17  HAVANA  gene        7661779  7687538  .  -  .  gene_id "ENSG00000141510.18"; gene_name "TP53"; gene_type "protein_coding";
chr17  HAVANA  transcript  7661779  7687538  .  -  .  gene_id "ENSG00000141510.18"; transcript_id "ENST00000269305.9"; gene_name "TP53"; tag "MANE_Select";
chr17  HAVANA  exon        7687377  7687538  .  -  .  gene_id "ENSG00000141510.18"; transcript_id "ENST00000269305.9"; exon_number 1;
```

| # | 欄位 | 意義 |
| --- | --- | --- |
| 1 | seqname | 染色體（GENCODE / UCSC 用 `chr17`，Ensembl 用 `17`） |
| 2 | source | 註解來源（HAVANA、ENSEMBL、BestRefSeq…） |
| 3 | feature | `gene`、`transcript`、`exon`、`CDS`、`UTR`、`start_codon`… |
| 4–5 | start / end | 1-based、含頭尾 |
| 6 | score | 多為 `.` |
| 7 | strand | `+` / `-`（TP53 在負股，exon 1 位置數字最大） |
| 8 | frame | CDS 的讀框相位 0 / 1 / 2 |
| 9 | attributes | 鍵值對（見下） |

## GTF vs GFF3

| | GTF（GFF2.5） | GFF3 |
| --- | --- | --- |
| 第 9 欄 | `gene_id "X"; transcript_id "Y";` | `ID=X;Parent=Y;Name=TP53` |
| 階層 | 每列都重複帶 `gene_id`、`transcript_id` | 用 `ID` / `Parent` 連結 |
| 誰在用 | STAR、featureCounts、HTSeq、Salmon（tximport 對照表） | Ensembl / NCBI 原生、IGV、gffread、AGAT |
| 轉換 | `gffread in.gff3 -T -o out.gtf`、AGAT | `gffread in.gtf -o out.gff3` |

## 常用操作

```bash
# 某基因的所有 exon
zcat gencode.v4x.annotation.gtf.gz | awk '$3=="exon"' | grep 'gene_name "TP53";'

# 所有基因 → BED（注意 start - 1）
zcat genes.gtf.gz | awk -F'\t' '$3=="gene" {match($9,/gene_name "[^"]+"/); n=substr($9,RSTART+11,RLENGTH-12); print $1"\t"$4-1"\t"$5"\t"n"\t.\t"$7}' > genes.bed

# 轉錄本對基因的對照表（tximport 用）
zcat genes.gtf.gz | awk -F'\t' '$3=="transcript"' | grep -o 'transcript_id "[^"]*"\|gene_id "[^"]*"' | paste - - > tx2gene.txt

# 從 GTF + FASTA 取出轉錄本序列（Salmon / kallisto 索引用）
gffread -w transcripts.fa -g GRCh38.fa genes.gtf
```

R 可用 `rtracklayer::import("x.gtf")` 讀成 GRanges；Python 可用 `pyranges` / `gtfparse`。

## 注意

| 注意 | 說明 |
| --- | --- |
| 與 FASTA 同版本、同命名 | STAR 索引用 GENCODE GTF 就要配 GENCODE / UCSC 風格的 FASTA（`chr1`） |
| ID 版本號 | `ENSG00000141510.18` 的 `.18` 是版本；與其他資料合併時常要去掉版本號 |
| 選哪個註解 | GENCODE / Ensembl vs RefSeq、comprehensive vs basic、MANE，見 [基因註解](../reference-data/gene-annotations.md) |
| 轉 BED 時 | start − 1（見 [座標系統](zero-one-based.md)） |

規格：[Ensembl GFF/GTF 格式說明](https://www.ensembl.org/info/website/upload/gff.html)、[GFF3 specification](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)。
