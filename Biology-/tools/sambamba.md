# Sambamba

---

## Overview

---

**Sambamba** is a fast and versatile command-line tool for working with SAM and BAM files in next-generation sequencing (NGS) data analysis. It provides efficient multi-threaded implementations for common operations like sorting, indexing, viewing, marking duplicates, and calculating read depth.

## Key Features

---

- Fast depth calculation at base or region level
- Multi-threaded BAM operations (sort, index, mark duplicates)
- Filter and view alignments
- Compatible with standard BAM/SAM/CRAM tools

---

## Calculate Coverage by a BED File

---

### Per-base Coverage

Extract read depth information at a specific genomic position using Sambamba and optionally convert the result into a BED file format.

```bash
# Position: chr7:150652580-150652581
# Equivalent BED format: chr7   150652579   150652581

# Using a Genomic Position
sambamba depth base -L chr7:150652580-150652581 -c 0 -q20 bam_file

# Using a BED File
sambamba depth base -L bed_file -c 0 -q20 bam_file
```

- `-c`: minimal count depth

**Output Example**

```less
REF     POS          COV     A   C   G   T   DEL REFSKIP SAMPLE
chr7    150652579    21      0   0   0   21  0   0       bam_file
chr7    150652580    22      0   0   22  0   0   0       bam_file
```

- `COV`: Total coverage at that position
- `A/C/G/T`: Base counts
- `DEL`: Deletion count
- `REFSKIP`: Skipped regions (e.g. splice junctions)
- `SAMPLE`: BAM file name

## References

---

- [Sambamba GitHub](https://github.com/biod/sambamba)
- [BED File Format](https://genome.ucsc.edu/FAQ/FAQformat.html#format1)
- [Sambamba Documentation](https://lomereiter.github.io/sambamba/)
