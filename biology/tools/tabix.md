# Tabix

---

## Overview

---

**Tabix** is a command-line utility that allows efficient random access to **TAB-delimited, position-sorted** text files compressed using BGZF. It is commonly used in genomics to index and query files like VCF, BED, GFF, and SAM by genomic coordinates.

Tabix works with `.gz` files created by `bgzip` and creates a corresponding `.tbi` index file. With the index, tabix can rapidly extract rows that overlap specified genomic regions.

## Key Features

---

- Fast random access to large compressed genomic files
- Supports various file types (VCF, BED, GTF/GFF, SAM)
- Simple region-based querying
- Integrates with tools like `bcftools`, `samtools`, and other bioinformatics pipelines

---

## Indexing a File

---

Before querying with tabix, the file must be:

1. **BGZF-compressed** (with `bgzip`)
2. **Sorted** by chromosomal coordinate

**Example**: Compress and index a VCF

```bash
bgzip input.vcf                                        # Creates input.vcf.gz
bcftools sort input.vcf.gz -Oz -o input.sorted.vcf.gz  # Optional: sort if not already
tabix -p vcf input.sorted.vcf.gz                       # Create tabix index (.tbi)
```

- `-p vcf` specifies the file format (preset); other options include `bed`, `gff`, `sam`, etc.

## Query by Genomic Region

---

Once the file is indexed, you can extract subsets of the file using genomic coordinates:

```bash
# Extract entire chromosome 11
tabix input.vcf.gz 11

# Extract a specific position
tabix input.vcf.gz 11:123456

# Extract a range of positions
tabix input.vcf.gz 11:123456-123457
```

**Notes**:

- Chromosome names must match exactly (e.g., `chr1` vs `1`)
- The index file (`.tbi`) must be in the same directory as the `.vcf.gz`
- Output is written to stdout

## Related Tools

---

- `bgzip`: compresses input to BGZF format compatible with tabix
- [bcftools index](bcftools.md#vcf-indexing): an alternative to tabix for VCF indexing
- [samtools](samtools.md): similar indexing functions for BAM/CRAM files

---

## References

---

- [HTSlib Tabix Documentation](http://www.htslib.org/doc/tabix.html)
- [VCF Specification](https://samtools.github.io/hts-specs/VCFv4.3.pdf)
- [BCFtools GitHub](https://github.com/samtools/bcftools)
