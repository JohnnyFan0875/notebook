# BEDtools

---

## Overview

---

**BEDtools** is a powerful suite of command-line utilities for performing genomic arithmetic. It allows users to intersect, merge, count, complement, and manipulate genomic intervals from multiple files in BED, GFF/GTF, VCF, or BAM formats.

## Key Features

---

- Intersect genomic features
- Merge overlapping regions
- Calculate coverage and statistics
- Subtract or complement regions
- Shuffle or randomize intervals
- Convert between file formats

## Merge Overlapping Regions

---

Sort the BED file

```bash
sort -k1,1 -k2,2n input.bed > input.sorted.bed
```

Merge overlapping or adjacent intervals in the BED file

```bash
bedtools merge -i input.sorted.bed > input.sorted.merged.bed
```

Merge with Column Collapse

```bash
bedtools merge -i bam_file.sorted -c 4 -o collapse > bam_file.sorted.merged
```

- **Output:** Includes a 4th column where overlapping features are collapsed into a comma-separated list (e.g., `chr1 1 100 EGFR,EGFR`).
- `-c 4`: Specifies the column to operate on (e.g., gene name)
- `-o collapse`: Collapse the values into a comma-separated string

## Intersect

---

```bash
bedtools intersect -a bedfile1 -b bedfile2 > outputfile
```

### Parameters

- `-a`: Input file A (e.g., BED/BAM/VCF/GFF); features in this file are compared against B
- `-b`: Input file B; one or more files with features to intersect with A
- `-wa`: Write the original entry in A for each overlap

> For full documentation: [bedtools intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html)

## References

---

- [BEDtools Homepage](https://bedtools.readthedocs.io/en/latest/)
- [BEDtools GitHub](https://github.com/arq5x/bedtools2)
- [BED Format Specification](https://genome.ucsc.edu/FAQ/FAQformat.html#format1)
