# FASTQ

## Introduction

**FASTQ** is a standard text-based format for storing both biological sequence data and corresponding base quality scores. It is commonly produced by high-throughput sequencing platforms such as Illumina, and forms the foundation for downstream analyses like alignment, quantification, and variant calling.

## Data Structure

Each read in a FASTQ file consists of **4 lines**:

1. `@` identifier line, usually gives the information of the sample
2. DNA sequence
3. `+` separator (optionally repeats identifier)
4. Quality scores (ASCII-encoded Phred scores)

Example:

```text
@SEQ_ID
GATTTGGGGTTTAAAGGG
+
!''\*((((\*\*\*+))%%%++)
```

- The last line contains quality scores encoded as ASCII characters.

- Higher Phred scores indicate more confident base calls.

## Quality Control

- [FastQC](fastqc.md): Quality control report generation

- [Fastp](fastp.md): Adapter trimming and filtering