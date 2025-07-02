# SAMtools

---

## Overview

---

**SAMtools** is a suite of programs for interacting with high-throughput sequencing data in SAM, BAM, and CRAM formats. It is commonly used for viewing, filtering, indexing, and summarizing alignment files in bioinformatics pipelines.

SAMtools supports compressed and indexed formats and is optimized for efficient access and manipulation of large alignment datasets.

## Generate Alignment Statistics

---

### `samtools stats` Method

```bash
samtools stats -@ threads_no input.bam > input.bam.stats
plot-bamstats -p prefix_name input.bam.stats  # -p test/ will create files in test folder
```

### `samtools flagstats` Method

```bash
samtools flagstats input.bam > input.bam.stats
```

Output

```bash
363458 + 0 in total (QC-passed reads + QC-failed reads) # Total number of reads including other such as supplementary
363458 + 0 primary                                      # Total number of reads that were provided as input for mapping
0 + 0 secondary                                         # One of the many places a multimapper can align. Note that multimappers will have one primary and 0 or more such secondary alignments.
0 + 0 supplementary                                     # For chimeric/fusion/non-linear alignments, this is the location of one part of the alignment. For reads that align in a chimeric fashion, one segment will be designated as primary and the remainder supplementary.
0 + 0 duplicates                                        # If you've marked possible PCR duplicates, then this will be set. The definition of a duplicate is somewhat dependent on the tool used (N.B., aligners don't typically set this flag, it's down by picard's markDuplicates command or similar).
0 + 0 primary duplicates                                # primary reads that were marked as duplicates
362756 + 0 mapped (99.81% : N/A)                        # number of mapped reads including supplementary
362756 + 0 primary mapped (99.81% : N/A)                # number of mapped reads that are labelled primary (just the number of mapped reads out of the input reads). i.e. excludes the number of reads that are supplementary.
0 + 0 paired in sequencing                              # This is the number of paired reads. If you used only paired reads after trimming, this will be the same as the number in the primary field
0 + 0 read1                                             # This is the number of forward (R1) reads. If you used only paired reads after trimming, this will be half of the number in the primary field
0 + 0 read2                                             # This is the number of reverse (R2) reads. If you used only paired reads after trimming, this will be the same as the read1 field.
0 + 0 properly paired (N/A : N/A)                       # This is the number of reads that map in a way that makes sense (Not too far apart, on different chromosomes, R1 read maps to the forward strand and R2 to the reverse strand etc. depending on the aligner). See this for some more information. This is suitable if you want to be very conservative with the number of reads that you consider mapped.
0 + 0 with itself and mate mapped                       # Number of reads with its corresponding reverse / forward read also mapped. This is less strict that properly paired but more that primary mapped.
0 + 0 singletons (N/A : N/A)                            # This is the number of reads that are mapped but their corresponding reverse / forward read did not map. (primary mapped - with itself and mate mapped = singletons)
0 + 0 with mate mapped to a different chr               # This is the number of reads that are mapped but their corresponding reverse / forward read mapped to a different chromosome. Remove these from properly paired to get an even more conservative estimate of number of mapped reads.
0 + 0 with mate mapped to a different chr (mapQ>=5)     # This is the number of reads that are mapped but their corresponding reverse / forward read mapped to a different chromosome with good quality for the alignment. Remove these from properly paired to get a more conservative estimate of number of mapped reads.
```

- Reference: [Biostars](https://www.biostars.org/p/268550/)

## Create Smaller BAM File by a Given Region

---

```bash
regions="chr1:1-100"
samtools view -h -b -o bam_file.selected.bam bam_file "$regions"
```

- `-h`: Output BAM includes the SAM header (e.g., @SQ, @PG, etc.)
- `-b`: Output in BAM format

## Calculate Coverage by a BED File

---

### Region-level Coverage

```bash
samtools bedcov regions.bed input.bam > coverage_output.txt
```

**Output**:

Columns 1–5 from the BED file + total read depth across the region

```text
chr12   25358179        25362845        KRAS    1       0
chr12   25378547        25378707        KRAS    1       709757
chr12   25380167        25380346        KRAS    1       501596
chr12   25398207        25398329        KRAS    1       877467
```

### Per-base Coverage

```bash
samtools depth -b regions.bed input.bam > per_base_coverage.txt
```

```text
# output
chr12   25378548        4909
chr12   25378549        4903
chr12   25378550        4907
```

- Per-base Coverage by sambamba: [sambamba depth base](#sambamba.md#per-base-coverage)

## Convert BAM to SAM

---

```bash
samtools view -h -o output.sam input.bam
```

- Add `-h` to include the SAM header.

## Indexing BAM Files

---

To enable fast random access (e.g., viewing reads in a specific genomic window), indexing is required. The extension of BAM file index is `.bai`:

```bash
samtools index sample.bam
```
