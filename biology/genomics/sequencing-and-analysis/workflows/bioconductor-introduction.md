# Introduction to Bioconductor

`Bioconductor` is an R ecosystem for genomics, transcriptomics, and other high-dimensional biological data. The practical value is not only the package collection itself, but also a shared set of data structures that make sequencing workflows composable.

## Installation

Most packages are installed through `BiocManager`:

```r
install.packages("BiocManager")
BiocManager::install("GenomicRanges")
BiocManager::install("Biostrings")
BiocManager::install("ShortRead")
```

## What Bioconductor Tries to Represent

Bioconductor workflows usually describe biology in terms of structured objects:

- sequence strings
- genomic intervals
- aligned reads
- feature-level measurements
- metadata attached to each observation

This matters because many sequencing tasks are really operations on structured biological coordinates rather than plain tables.

## `Biostrings` for Biological Sequences

`Biostrings` provides memory-efficient containers for sequence data.

- `XString`: virtual base class for a single sequence
- `DNAString`, `RNAString`, `AAString`: typed single-sequence containers
- `XStringSet`: collection of many sequences
- `DNAStringSet`, `RNAStringSet`, `AAStringSet`: typed sequence collections

Example:

```r
library(Biostrings)
dna_seq <- DNAString("ATGATCTCGTAA")
```

Useful mental model: use ordinary R strings for light text work, but use `Biostrings` objects once the sequence itself becomes an analysis object.

## `IRanges` for Coordinate Arithmetic

`IRanges` is the foundation for interval-style work. A range is defined by genomic-like coordinates, even before chromosome names are introduced.

```r
library(IRanges)

IRanges(start = 20, end = 30)
IRanges(start = c(1, 20), width = c(30, 11))
IRanges(start = c(1, 20), end = 30)
```

Important relation:

```text
width = end - start + 1
```

`IRanges` also works naturally with logical runs. This is useful when you have long vectors of repeated values and want to recover contiguous positive segments.

```r
Rle(c(FALSE, FALSE, TRUE, TRUE, FALSE))
IRanges(start = c(FALSE, FALSE, TRUE, TRUE))
```

## `Rle` for Repetitive Vectors

`Rle` means run-length encoding. It stores long repeated vectors efficiently and appears throughout Bioconductor objects.

Why it matters:

- chromosome labels are repetitive
- strand labels are repetitive
- coverage-like vectors often contain long repeated runs

So `Rle` is both a storage optimization and part of the object model for genomic data.

## `GRanges` for Genomic Intervals

`GRanges` extends interval logic from abstract ranges to genomic coordinates.

```r
library(GenomicRanges)
GRanges("chr1:200-300")
```

A `GRanges` object typically contains:

- `seqnames`: chromosome or contig
- `ranges`: interval coordinates
- `strand`
- metadata columns such as score, GC content, annotation, or sample-level summaries

You can also convert tabular coordinates into genomic ranges:

```r
myGR <- as(df, "GRanges")
```

This is one of the most important Bioconductor ideas. Reads, peaks, exons, SNPs, and binding sites can all be treated as genomic intervals, which makes overlap, annotation, and summarization workflows much easier to compose.

## `ShortRead` for FASTA and FASTQ

`ShortRead` provides I/O and QC-oriented containers for short sequencing reads.

FASTA example:

```r
library(ShortRead)
fasample <- readFasta(dirPath = "data/", pattern = "fasta")
writeFasta(fasample, file = "data/sample.fasta")
```

FASTQ example:

```r
fqsample <- readFastq(dirPath = "data/", pattern = "fastq")
writeFastq(fqsample, file = "data/sample.fastq.gz")
```

Typical object types:

- `ShortRead`: FASTA-oriented read container
- `ShortReadQ`: FASTQ container with base qualities

For large FASTQ files, sampling is often more practical than loading everything at once:

```r
sampler <- FastqSampler("data/SRR1971253.fastq", 500)
sample_small <- yield(sampler)
```

## Reading Sequence and Quality Together

`ShortRead` makes the sequence and its qualities accessible as linked data:

```r
sread(fqsample)[1]
quality(fqsample)[1]
```

Quality strings are ASCII-encoded. They can be converted to numeric Phred scores:

```r
pq <- PhredQuality(quality(fqsample))
qs <- as(pq, "IntegerList")
```

This is useful when you want to move from "the file stores a quality line" to "the workflow reasons about per-base quality scores".

## Built-in QC Summary

`ShortRead` also provides a quality assessment summary:

```r
qaSummary <- qa(fqsample, lane = 1)
names(qaSummary)
report(qaSummary)
```

The summary can expose:

- read counts
- base calls
- read quality scores
- per-cycle patterns
- frequent sequences
- adapter contamination

This makes `ShortRead` useful not only for file parsing, but also for compact in-R QC inspection.

## Base Composition by Cycle

Per-cycle summaries help detect sequencing bias or chemistry drift.

```r
abc <- alphabetByCycle(sread(fullSample))
```

A common next step is to inspect how `A`, `C`, `G`, and `T` proportions change across cycles.

## Practical Workflow

A compact Bioconductor-centered sequencing workflow often looks like this:

1. install the relevant package family with `BiocManager`
2. represent sequences with `Biostrings`
3. represent intervals with `IRanges`
4. promote genomic coordinates to `GRanges`
5. load FASTA or FASTQ reads with `ShortRead`
6. inspect qualities before downstream analysis
7. hand structured objects to downstream packages such as `limma`, `GenomicAlignments`, or peak-calling and annotation workflows

## Common Mistakes

- treating Bioconductor packages as isolated tools instead of a shared object system
- keeping genomic coordinates as plain data frames longer than necessary
- ignoring `Rle` and `GRanges` accessors, then writing unnecessary manual parsing code
- loading large FASTQ files eagerly when sampling or streaming would be enough
- treating ASCII quality strings as opaque text instead of converting them when numeric scores are needed
