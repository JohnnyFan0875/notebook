# BCFtools

---

## Overview

---

**BCFtools** is a set of command-line tools for manipulating [VCF](../format/vcf.md) (Variant Call Format) and BCF (Binary Call Format) files, which are used to store genetic variant information. It is commonly used in genomics pipelines for variant calling, filtering, statistics, and format conversion.

BCFtools works efficiently with compressed and indexed files, making it suitable for large-scale variant datasets.

---

## Key Features

---

- Variant calling from alignment (e.g., from mpileup)
- Filtering and querying variants
- Subsetting samples or regions
- Annotating VCF files
- Merging or concatenating multiple VCFs
- Converting between VCF and BCF
- Indexing VCF/BCF files for rapid access

## Commonly Used Commands

---

### VCF Indexing

To efficiently retrieve specific regions from a VCF or BCF file, indexing is required. BCFtools supports indexing using [tabix](tabix.md) or its own internal methods.

```bash
# Compress the VCF File (create input.vcf.gz)
bgzip input.vcf

# Sort VCF (optional)
bcftools sort input.vcf.gz -Oz -o input.sorted.vcf.gz

# Generate index (vcf.gz.tbi) File (Using tabix or bcftools)
tabix -p vcf input.sorted.vcf.gz
bcftools index -t input.sorted.vcf.gz
```

- `-O`: output format
- `-z`: compressed VCF format using BGZF (i.e., .vcf.gz), compatible with tools like `tabix`

### View VCF/BCF contents:

```bash
bcftools view input.vcf.gz
```

### Filter variants:

Creates filtered.vcf.gz, where low-quality/depth variants are filtered and marked.

```bash
bcftools filter -s LowQual -e '%QUAL<20 || DP<10' input.vcf.gz -Oz -o filtered.vcf.gz
```

- `-s LowQual`: Assigns the filter name **LowQual** to variants that fail the filter.
- `-e '%QUAL<20 || DP<10'`: Exclude (-e) variants where `QUAL` is less than 20 or `DP` (read depth) is less than 10

### Extract variants from a region:

```bash
bcftools view -r chr1:10000-20000 input.vcf.gz
```

### Subset samples:

Create a VCF file containing only sample1 and sample2 and all their variant data.

```bash
bcftools view -s sample1,sample2 input.vcf.gz -Oz -o subset.vcf.gz
```

- `-s sample1,sample2`: Select only the listed samples from the VCF

### Merge multiple VCF files:

```bash
bcftools merge file1.vcf.gz file2.vcf.gz -Oz -o merged.vcf.gz
```

### Query variant annotation (rsID)

- Obtain dbSNP reference VCF from the NCBI FTP server: [Source](https://ftp.ncbi.nlm.nih.gov/snp/latest_release/VCF/)
- dbSNP VCFs often use `RefSeq accessions` (e.g. NC_000011.9), while user VCFs may use `chr11` or `11`.
  - Inspect chromosome naming: `bcftools view -h GCF_FILE | grep contig`
  - If chromosome names are inconsistent, create a mapping file (`chrom_map.txt`) with the format:
    ```bash
    chr11   NC_000011.9
    chr1    NC_000001.10
    ```

```bash
bgzip -c test.vcf > test.vcf.gz
bcftools sort test.vcf.gz -Oz -o test.sorted.vcf.gz
tabix -c vcf test.sorted.vcf.gz
bcftools annotate --rename-chrs chrom_map.txt test.sorted.vcf.gz -Oz -o test.sorted.renamechr.vcf.gz # if required
bcftools annotate -a GCF_FILE -c ID test.sorted.renamechr.vcf.gz
```
