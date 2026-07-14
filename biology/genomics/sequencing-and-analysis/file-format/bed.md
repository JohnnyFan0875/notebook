# BED

## Overview

The **BED (Browser Extensible Data)** format is a lightweight text format used to define genomic regions. It is widely used in genome browsers (e.g., UCSC Genome Browser) and analysis tools to represent features like exons, peaks, regulatory elements, or custom intervals.

BED files are simple, compact, and flexible, making them useful for filtering, annotating, and visualizing genomic data.

## Structure

BED files are plain-text files with **0-based, half-open intervals**. The start position is inclusive, and the end position is exclusive. `[start, end)` Each line represents one feature.

```text
chr1    1   2         # position 2
chr1    1   1000      # position 2-1000
```

A BED file typically consists of **at least 3 mandatory fields**, and optionally up to 12 fields:

1. **Basic Fields (Required)**:

| Field      | Description                           | Example |
| ---------- | ------------------------------------- | ------- |
| chrom      | Chromosome name                       | chr1    |
| chromStart | Start position (0-based)              | 999     |
| chromEnd   | End position (non-inclusive, 1-based) | 1050    |

**Example:**

```text
chr1    999    1050
```

2. **Optional Fields (BED3+ format)**:

| Field       | Description                                        | Example |
| ----------- | -------------------------------------------------- | ------- |
| name        | Feature name                                       | geneA   |
| score       | Score from 0 to 1000                               | 960     |
| strand      | Strand (+ or -)                                    | +       |
| thickStart  | Start position for thick display (e.g., CDS)       | 1000    |
| thickEnd    | End position for thick display                     | 1045    |
| itemRgb     | RGB color (comma-separated, e.g., 255,0,0 for red) | 0,0,255 |
| blockCount  | Number of blocks (e.g., exons)                     | 2       |
| blockSizes  | Comma-separated list of block sizes                | 20,30   |
| blockStarts | Comma-separated list of start positions (relative) | 0,21    |

**Extended Example:**

```text
chr1    999    1050    geneA    960    +    1000    1045    0,0,255    2    20,30    0,21
```

## Applications

- Defining regions of interest (ROIs) for filtering BAM/VCF files
- Input for genome browsers (e.g., UCSC, IGV)
- Defining peak regions in ChIP-seq or ATAC-seq
- Genomic intersection, union, and subtraction using tools like `bedtools`

## Common tools

| Tool                                                                  | Purpose                          |
| --------------------------------------------------------------------- | -------------------------------- |
| [**bedtools**](../../../bioinformatics-tools/bioinformatics/bedtools.md)                                  | Manipulate and compare BED files |
| [**IGV**](../../../bioinformatics-tools/visualization/igv.md)                                            | Visualize BED annotations        |
| [**samtools**](../../../bioinformatics-tools/bioinformatics/samtools.md)                                  | Filter BAM reads overlapping BED |
| [**UCSC tools**](https://genome.ucsc.edu/goldenPath/help/bigBed.html) | Convert to BigBed format         |

## References

- [UCSC BED Format Definition](https://genome.ucsc.edu/FAQ/FAQformat.html#format1)
- [BEDTools User Guide](https://bedtools.readthedocs.io/en/latest/)
- [IGV BED Format](https://igv.org/doc/desktop/#FileFormats/DataTracks/)
