[生資工具](../README.md) › [NGS 工具](README.md) › FastQC

# FastQC

對原始 [FASTQ](../../genomics/file-formats/fastq.md)（或 BAM）產生品質報告，決定是否需要修剪或過濾。多個樣本用 MultiQC 彙整成一份報告。

## 用法

```bash
conda install -c bioconda fastqc multiqc

mkdir -p qc                                  # -o 的資料夾必須先存在
fastqc -t 8 -o qc/ *.fastq.gz                # 每個檔案產生 .html + .zip
multiqc qc/ -o qc/                           # 彙整所有樣本（也能吃 fastp、STAR、samtools 的輸出）
```

## 各模組怎麼看

| 模組 | 看什麼 | 常見警告的原因 |
| --- | --- | --- |
| Per base sequence quality | 每個 cycle 的品質分布 | 尾端下降是正常的；整體偏低要修剪或重做（見 [鹼基品質分數](../../genomics/ngs-qc/base-quality.md)） |
| Per sequence quality scores | 每條 read 的平均品質 | 出現低品質的小峰：部分 tile 或 cluster 有問題 |
| Per base sequence content | 每個 cycle 的 A/C/G/T 比例 | RNA-seq 前 10–15 bp 因隨機引子偏好必定 FAIL，屬正常 |
| Per sequence GC content | GC 分布是否接近理論常態 | 雙峰：污染（細菌、adapter dimer）或高表現基因 |
| Per base N content | N 的比例 | 某個 cycle 突增：儀器問題 |
| Sequence length distribution | 長度分布 | 修剪後本來就不一致 |
| Sequence duplication levels | 重複序列比例 | RNA-seq、amplicon 本來就高（見 [重複率](../../genomics/ngs-qc/duplication-rate.md)） |
| Overrepresented sequences | 出現過多的序列 | adapter、rRNA、primer dimer |
| Adapter content | adapter 從哪個位置開始出現 | 插入片段比 read 短；用 [fastp](fastp.md) 修剪 |

> FastQC 的 PASS / WARN / FAIL 閾值是以「隨機、多樣的 WGS library」為基準設計的。RNA-seq、amplicon、bisulfite、small RNA 等 library 有些模組必然 FAIL，要對照實驗類型判讀，不是看到紅色就重做。

## 輸出

| 檔案 | 用途 |
| --- | --- |
| `*_fastqc.html` | 互動報告 |
| `*_fastqc.zip` | 原始數據（`fastqc_data.txt`、`summary.txt`），可程式化讀取或交給 MultiQC |

修剪前後各跑一次 FastQC（或直接看 fastp 報告）比較效果。官方：[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)、[GitHub](https://github.com/s-andrews/FastQC)；中文說明：[CSDN FastQC 詳解](https://blog.csdn.net/qq_44520665/article/details/113779792)。
