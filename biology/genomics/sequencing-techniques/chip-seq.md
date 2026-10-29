[基因體學](../README.md) › [定序技術](README.md) › ChIP-seq

# ChIP-seq (Chromatin Immunoprecipitation Sequencing)

用抗體把目標蛋白（轉錄因子、組蛋白修飾）連同結合的 DNA 一起拉下來定序，找出它在基因組上的結合位置。分析的重點不只是「找 peak」，而是**比較條件間的結合差異**並連回基因與調控區域。

## 流程

```
FASTQ ──比對（Bowtie2 / BWA）──► BAM ──過濾（MAPQ、重複、blacklist）
  ──► peak calling（MACS3，ChIP vs input）──► peak（BED / narrowPeak）
  ──► QC（FRiP、重複一致性、指紋圖）
  ──► 共識 peak 集合 ──► 計數 ──► 差異結合（DiffBind：DESeq2 / edgeR）
  ──► 註解（最近基因、啟動子 / 遠端）、motif、富集分析
```

## 實驗設計

| 項目 | 建議 |
| --- | --- |
| 對照 | **Input**（未經免疫沉澱的同一樣本 DNA）必備；IgG 對照為輔 |
| 生物重複 | 每個條件至少 2 個，差異分析建議 ≥ 3 |
| 定序深度 | 轉錄因子約 20 M reads；廣域組蛋白修飾（H3K27me3、H3K36me3）40 M 以上 |
| 抗體 | 品質決定一切；用已驗證的 ChIP 級抗體 |
| peak 類型 | 轉錄因子、H3K4me3：窄峰 (narrow)；H3K27me3、H3K36me3：廣域 (broad) |
| 替代方法 | CUT&RUN / CUT&Tag（低起始量、背景低）；ATAC-seq（開放染色質，不需抗體） |

## Peak calling 與 QC

```bash
# 過濾：MAPQ ≥ 30、移除重複與 ENCODE blacklist 區
samtools view -b -q 30 -F 0x404 chip.bam | bedtools intersect -v -abam stdin -b hg38-blacklist.v2.bed > chip.filt.bam

# MACS3：成對資料用 BAMPE；廣域修飾加 --broad
macs3 callpeak -t chip.filt.bam -c input.filt.bam -f BAMPE -g hs -n sample1 -q 0.01 --outdir peaks/

# deepTools：訊號軌與 TSS 周邊熱圖
bamCoverage -b chip.filt.bam -o chip.bw --normalizeUsing CPM --binSize 10
computeMatrix reference-point -S chip.bw -R genes.bed -a 3000 -b 3000 -o tss.mat.gz
plotHeatmap -m tss.mat.gz -o tss_heatmap.png
plotFingerprint -b chip.filt.bam input.filt.bam -o fingerprint.png
```

| QC 指標 | 意義 | 參考值 |
| --- | --- | --- |
| FRiP（reads in peaks 比例） | 訊號 / 雜訊 | 轉錄因子 > 1%；組蛋白修飾通常更高（ENCODE 建議） |
| NSC / RSC（交叉相關，phantompeakqualtools） | 片段長度訊號強度 | NSC > 1.05、RSC > 0.8 |
| IDR（重複間一致性） | 重複間可再現的 peak | 轉錄因子取 IDR < 0.05 的 peak |
| Fingerprint 曲線 | ChIP 與 input 的區分度 | ChIP 曲線越偏離對角線越好 |
| 重複率、PBC | library complexity | 見 [重複率](../ngs-qc/duplication-rate.md) |

## 在 R 中：peak 就是 GRanges

```r
library(GenomicAlignments); library(rtracklayer)
reads <- readGAlignments("chip.filt.bam")
cov <- coverage(reads)                           # RleList：全基因組訊號
peaks <- import("peaks/sample1_peaks.narrowPeak") # GRanges（自動轉成 1-based）
peaks[order(-peaks$signalValue)][1:5]

# 比較多個樣本的 peak 集合
library(UpSetR)
upset(fromList(lapply(peak_sets, \(p) paste(seqnames(p), start(p)))))   # 粗略：完全相同的區間
```

peak 不是表格，是有座標的區間；重疊、延伸、計數都用 GRanges 操作，見 [Bioconductor](../../bioinformatics-tools/bioconductor.md#區間irangesrlegranges)。

## 差異結合分析 (DiffBind)

比較條件（例：原發腫瘤 vs 抗藥腫瘤）前，**先建立所有樣本共用的共識 peak 集合**，再計算每個樣本在這些區域的 reads 數；否則各樣本是在不同區域上量測，無法比較。

```r
library(DiffBind)
db <- dba(sampleSheet = "samples.csv")     # 欄位：SampleID、Condition、Replicate、bamReads、bamControl、Peaks
db <- dba.count(db, summits = 250)         # 以 summit ± 250 bp 建共識區域並計數
db <- dba.normalize(db)
db <- dba.contrast(db, categories = DBA_CONDITION, minMembers = 2)
db <- dba.analyze(db)                      # 預設 DESeq2
res <- dba.report(db, th = 0.05)           # 顯著的差異結合區域（GRanges）

dba.plotPCA(db, DBA_CONDITION); dba.plotMA(db); dba.plotVolcano(db)
dba.plotHeatmap(db, correlations = FALSE)
```

`dba.analyze()` 預設用 DESeq2 對共識 peak 的 read 數做負二項 GLM，所以 RNA-seq 的統計觀念直接適用：[GLM 計數模型](../../../data-science/statistics/regression-analysis/glm-count-models.md#過度離散與負二項迴歸)、[多重檢定（FDR）](../../../data-science/statistics/inferential-statistics/multiple-testing.md)、[批次效應](../../../data-science/statistics/experimental-design/confounding-bias.md#生資最常見的干擾批次效應-batch-effect)。

| 圖 | 回答的問題 |
| --- | --- |
| 相關熱圖 / [PCA](../../../data-science/statistics/multivariate-analysis/pca.md) | 同條件的重複是否比不同條件更相似？ |
| MA plot | 效果量與平均訊號強度的關係 |
| Volcano plot | 效果量與顯著性 |
| 區域熱圖 | 特定位點的訊號型態 |

> 先看重複間是否一致，再看差異結果。任何單一張圖都不能證明生物學結論。

## 註解與解讀

| 步驟 | 工具 |
| --- | --- |
| peak → 最近基因、啟動子 / exon / intron / 基因間 | ChIPseeker `annotatePeak()`、HOMER `annotatePeaks.pl` |
| motif 富集（轉錄因子是否真的結合自己的 motif） | HOMER `findMotifsGenome.pl`、MEME-ChIP |
| 基因集富集 | GREAT（以調控區域指派基因）、clusterProfiler |
| 整合表現量 | 與 RNA-seq 差異表現基因交集 |

> 「peak 最靠近某基因」不等於「調控該基因」：遠端增強子可以跨越數十 kb，甚至跳過最近的基因。需要 Hi-C、eQTL 或擾動實驗支持。

## 常見錯誤

| 錯誤 | 修正 |
| --- | --- |
| 沒有 input 對照 | peak calling 無法區分開放染色質 / 定序偏差與真實訊號 |
| 沒過濾 blacklist | 重複區、著絲點附近出現大量假 peak |
| 各樣本 peak 直接比較 | 先建共識 peak 再計數 |
| 跳過重複一致性檢查 | 先看相關性 / PCA |
| 把 peak 檔當一般表格處理 | 用 GRanges / bedtools 的區間運算 |
| 只看顯著性 | 同時看效果量與重複間一致性 |
| 正規化方式未考慮全域性改變 | 若處理造成全基因組結合量改變，預設正規化會抹平差異；考慮 spike-in |

> 本筆記的 R 程式碼依 DiffBind / rtracklayer 官方文件整理，未在本機實跑。
