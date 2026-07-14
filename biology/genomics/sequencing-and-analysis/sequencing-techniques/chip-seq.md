# ChIP-seq

ChIP-seq combines chromatin immunoprecipitation with sequencing to identify where a protein of interest is associated with the genome. It is commonly used for transcription factors, histone modifications, and other chromatin-associated signals.

Key point: ChIP-seq is not just "find peaks". The practical workflow is usually:

1. aligned reads in BAM
2. coverage and peak calls as genomic intervals
3. comparison across samples or conditions
4. annotation of peaks back to genes or genomic features

## What ChIP-seq Measures

ChIP-seq asks where a target protein or chromatin mark is enriched along the genome.

Common use cases:

- transcription factor binding sites
- histone mark landscapes
- chromatin state comparison between conditions
- differential binding between sample groups

The biological question is often not only "where are the peaks?" but also:

- which sites are shared across samples
- which sites differ between conditions
- which genes or regulatory regions those peaks may affect

## Core Data Objects

### Aligned Reads

In practice, ChIP-seq reads are often stored in BAM files.

Important BAM fields include:

- read name
- flag
- reference chromosome and position
- mapping quality
- CIGAR string
- read sequence and qualities

In Bioconductor, aligned reads can be loaded with `GenomicAlignments`:

```r
library(GenomicAlignments)
reads <- readGAlignments("file_name")
```

### Coverage

Once reads are loaded, one of the first derived summaries is genomic coverage:

```r
coverage(reads)
```

Coverage turns aligned reads into a genome-wide signal profile. Peaks are later interpreted against this coverage landscape rather than from raw read records alone.

### Peak Calls as Genomic Ranges

Peak callers such as MACS2 often emit BED-like interval files. In Bioconductor, these are naturally represented as genomic ranges:

```r
library(rtracklayer)
peaks <- import.bed("file_name")
chrom(peaks)
ranges(peaks)
score(peaks)
```

This is a very important mental model: peaks are not just rows in a table, but intervals on a genome with coordinates and metadata.

## `GRanges` Is the Working Language

A lot of ChIP-seq analysis in Bioconductor becomes easier once you treat everything as genomic intervals.

Typical operations then become:

- overlap reads with peaks
- compare peak sets between samples
- extend reads
- annotate peaks with nearby genes
- summarize signal inside bins

This is why `GRanges` and related objects matter so much in Bioconductor workflows.

## Importing and Summarizing Signal

The workflow in the course emphasizes moving from reads to interval-level summaries.

Examples include:

- importing BAM alignments
- computing coverage tracks
- importing peak calls
- extracting coordinates and scores from peaks

For exploratory overlap between peak sets, UpSet-style set summaries are useful:

```r
upset(fromList(peak_sets))
```

This helps show which peaks are shared and which are sample-specific.

## Binned Coverage Around Peaks

A practical way to quantify signal is to bin genomic regions and count overlapping reads.

The course uses ideas like:

```r
overlap <- from(findOverlaps(bins, target))
peak_bins <- count_bins(reads_ext, peaks, bins)
bkg_bins <- subset(bins, !bins %in% peak_bins & !bins %in% bl_bins)
```

This workflow is useful because it separates:

- bins overlapping peaks
- background bins
- blacklisted or excluded bins

That distinction matters when you want interpretable enrichment rather than just raw coverage.

## Differential Binding

One of the main downstream goals of ChIP-seq is comparing binding between conditions.

The course example uses two groups such as:

- primary tumor
- treatment-resistant tumor

The key questions are:

- are replicates within a group similar
- are groups different from each other
- which loci drive those differences

## DiffBind Workflow

`DiffBind` is a common Bioconductor-centered workflow for differential binding analysis.

A typical sequence looks like:

```r
counts <- dba.count(qc_results, summits = 250)
peak_counts <- dba.count(qc_output, summits = 250)
peak_counts <- dba.contrast(peak_counts, categories = DBA_CONDITION)
bind_diff <- dba.analyze(peak_counts)
```

This encodes several important ideas:

- first create a shared peak set
- then count reads in comparable regions across all samples
- define contrasts between conditions
- run differential analysis

Key point: differential binding usually requires a consensus peak universe before comparing counts. Otherwise each sample is being measured on different regions.

## Sample Similarity and QC

Before trusting differential results, sample-level similarity should be checked.

The course highlights patterns such as:

```r
distance <- dist(t(coverage))
dba.plotHeatmap(peaks, maxSites = peak_count, correlations = FALSE)
```

Useful QC views include:

- clustering from coverage or counts
- PCA of samples
- heatmaps of signal at top sites

These help answer whether samples from the same condition behave more like each other than samples from different conditions.

## Common Differential Binding Visualizations

DiffBind commonly exposes:

- PCA plots
- heatmaps
- MA plots
- volcano plots
- box plots

These plots answer slightly different questions:

- PCA: overall sample-level separation
- heatmap: structured signal differences at selected regions
- MA plot: effect size vs average abundance
- volcano plot: effect size vs significance
- box plot: distributional comparison or QC

No single plot proves the biology. They are complementary views of the same count-based comparison.

## Interpreting Peaks

After differential peaks are found, the next problem is interpretation.

Typical questions:

- which genes are near these peaks
- are peaks promoter-proximal or distal
- which genomic features are enriched
- which genes are associated with stronger binding in one condition

This is where peak annotation becomes central.

## Peak Annotation

Peak interpretation usually involves assigning genomic intervals to nearby genes or genomic features such as:

- promoters
- exons
- introns
- intergenic regions
- enhancers when external annotation is available

Conceptually, peak annotation is not the same as proving target-gene regulation. It is a pragmatic mapping step that makes downstream biological interpretation possible.

## Practical Workflow

A compact Bioconductor-oriented ChIP-seq workflow looks like this:

1. align reads and keep BAM files
2. import reads with `readGAlignments()`
3. compute coverage and inspect signal shape
4. import called peaks as genomic ranges
5. compare peak sets across samples
6. build a shared peak universe for group comparison
7. count reads in consensus regions
8. run differential binding with `DiffBind`
9. inspect PCA / heatmap / MA / volcano outputs
10. annotate significant peaks to genes or genomic features

## Common Mistakes

- treating peak files as plain tables instead of genomic intervals
- comparing samples without first defining a shared peak set
- skipping replicate similarity checks before differential analysis
- interpreting nearest-gene annotation as direct causal regulation
- focusing only on peak significance without checking effect size and consistency
- forgetting that background bins, blacklist regions, and normalization choices affect interpretation
