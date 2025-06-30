# BAM Format

---

## Overview

---

The **BAM (Binary Alignment/Map)** format is the binary, compressed version of the SAM (Sequence Alignment/Map) format. It is widely used in genomics to store read alignments against a reference genome, especially in NGS workflows.

BAM files are preferred over SAM due to their smaller size, random access capability (with index), and compatibility with downstream tools.

## Structure

---

A BAM file consists of:

1. **Header Section**: Metadata (e.g., reference sequence names and lengths, read group info).

2. **Alignment Section**: Each record represents a mapped or unmapped read and its alignment to the reference genome.

Unlike SAM (plain text), BAM is a compressed binary format using **BGZF (Blocked GZip Format)**.

## Example

---

A BAM file cannot be viewed directly due to its binary nature. Here's an example SAM line (human-readable):

```text
SRR1234567.1 0 chr1 10050 60 101M * 0 0 AGCTTAGCTAGCTACCTAT... FFFFFFFFFFFFFFFFFFFF...
```

| Field | Description                             | Example Value           |
| ----- | --------------------------------------- | ----------------------- |
| QNAME | Query name (read ID)                    | SRR1234567.1            |
| FLAG  | Bitwise flag (e.g., mapped, paired)     | 0                       |
| RNAME | Reference sequence name                 | chr1                    |
| POS   | Position (1-based)                      | 10050                   |
| MAPQ  | Mapping quality                         | 60                      |
| CIGAR | Alignment representation                | 101M                    |
| RNEXT | Mate reference name (`*` if single-end) | \*                      |
| PNEXT | Mate alignment position (0 if N/A)      | 0                       |
| TLEN  | Template length (0 if single-end)       | 0                       |
| SEQ   | Read sequence                           | AGCTTAGCTAGCTACCTAT...  |
| QUAL  | Quality string (ASCII-encoded Phred)    | FFFFFFFFFFFFFFFFFFFF... |

- The **CIGAR** string can get more complex (e.g., 76M2I23M1D), representing matches, insertions, deletions, clipping, etc.

  ![Images](bam-format.webp)
  Reference: [futurelearn](https://www.futurelearn.com/info/courses/bioinformatics-for-biologists-analysing-and-interpreting-genomics-datasets/0/steps/388425)

- The **FLAG** field is important for filtering reads. 0 = simple case.
  - Reference: [Decoding SAM flags](https://broadinstitute.github.io/picard/explain-flags.html)
  - Reference: [BAM format](https://weitinglin.com/2016/01/27/sambam-and-cram/)
  - Reference: [BAM format](https://yourgene.pixnet.net/blog/post/95204728)

## Common tools

---

| Tool         | Purpose                             |
| ------------ | ----------------------------------- |
| **Samtools** | View, sort, index, filter BAM files |
| **Picard**   | Mark duplicates, collect metrics    |
| **bedtools** | Intersect BAM with BED regions      |
| **IGV**      | Visualize BAM alignments            |

## Convert BAM to SAM

---

```bash
samtools view -h -o output.sam input.bam
```

- Add `-h` to include header.


## Indexing BAM Files

To enable fast random access (e.g., view reads in a genomic window), you need to **index** the BAM:

```bash
samtools index sample.bam
# Produces sample.bam.bai
```


## Create smaller bam file by a given regions

```bash
regions="chr1:1-100"
samtools view -h -b -o bam_file.selected.bam bam_file "$regions"
```

## Calculate coverage by a BED file

### Region-level coverage

```bash
samtools bedcov regions.bed input.bam > coverage_output.txt
```

```text
# output

chr12   25358179        25362845        KRAS    1       0
chr12   25378547        25378707        KRAS    1       709757
chr12   25380167        25380346        KRAS    1       501596
chr12   25398207        25398329        KRAS    1       877467
```

### Per-base coverage

#### `samtools depth` method

```bash
samtools depth -b regions.bed input.bam > per_base_coverage.txt
```

```text
# output

chr12   25378548        4909
chr12   25378549        4903
chr12   25378550        4907
```

#### `sambamba depth base` method

```bash
sambamba depth base -L regions.bed -o per_base_coverage.txt -c 0 -q20 input.bam

# -c: minimal count depth
```

- Convert sambamba output position to bed file: [Link](bed.md#convert-sambamba-output-position-to-bed-file)
