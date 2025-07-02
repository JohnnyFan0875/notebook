# VCF

---

## Overview

---

The **VCF (Variant Call Format)** is a standardized text file format used in bioinformatics to store genetic variation data, such as SNPs (single nucleotide polymorphisms), insertions, deletions, and structural variants.

It is commonly used to represent the results of variant calling in NGS workflows and allows for easy annotation, filtering, and comparison of genetic variants across samples.

## Structure

---

A VCF file is human-readable and consists of two main sections: a **header section** (with metadata) and a **data section** (with variant records).

1. **Header Section**: The header lines begin with `##` and define metadata such as file format, reference genome, and INFO/FORMAT fields. The final header line starts with a single `#` and defines the column names for the variant records.

| Tag            | Description                           |
| -------------- | ------------------------------------- |
| `##fileformat` | Version of VCF format                 |
| `##INFO`       | Definitions of INFO field annotations |
| `##FORMAT`     | Definitions of genotype format fields |
| `##FILTER`     | Filters used to flag variants         |
| `#CHROM`       | Column names: starts the data table   |

Example:

```text
##fileformat=VCFv4.2
##FILTER=<ID=PASS,Description="All filters passed">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  Sample1
```

2. **Data Section**: Each row corresponds to a variant record with details about the genomic position, alleles, quality, filters, and sample-level genotypes.

* Example:

  ```text
  chr1    123456  rs1234567   G       A       29.7    PASS    AC=1;AF=0.5  GT      0/1
  ```

  | Field   | Description                     | Example Value |
  | ------- | ------------------------------- | ------------- |
  | CHROM   | Chromosome name                 | chr1          |
  | POS     | 1-based position of the variant | 123456        |
  | ID      | Variant ID (e.g., dbSNP rsID)   | rs1234567     |
  | REF     | Reference allele                | G             |
  | ALT     | Alternate allele(s)             | A             |
  | QUAL    | Phred-scaled quality score      | 29.7          |
  | FILTER  | Variant filter status           | PASS          |
  | INFO    | Semicolon-separated annotations | AC=1;AF=0.5   |
  | FORMAT  | Genotype format keys            | GT            |
  | Sample1 | Sample-level genotype data      | 0/1           |

* The **GT** field indicates genotype (`0/0` = homozygous reference, `0/1` = heterozygous, `1/1` = homozygous alternate).

* Additional FORMAT fields can include `DP` (depth), `GQ` (genotype quality), etc.

## Common tools

---

| Tool                                 | Purpose                                   |
| ------------------------------------ | ----------------------------------------- |
| [**bcftools**](../tools/bcftools.md) | View, filter, merge, and annotate VCFs    |
| [**vcftools**](../tools/vcftools.md) | Summary stats, filtering, manipulation    |
| [**GATK**](../tools/gatk.md)         | Variant calling, recalibration, filtering |
| [**SnpEff**](../tools/snpeff.md)     | Variant annotation and effect prediction  |
| [**IGV**](../tools/igv.md)           | Visual inspection of variants             |