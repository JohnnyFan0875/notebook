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

## Quality control

```bash
fastqc -o output_file -t 8 file.fastq.gz
```

- `-o`: Output directory for report files
- `-t`: Number of threads (faster with more cores)

- Output:

  - `.html` file for interactive summary
  - `.zip` file containing raw data and metrics

- Key Metrics:

  - Per-base sequence quality
  - Per-sequence GC content
  - Overrepresented sequences
  - Adapter content
  - Sequence duplication levels

> Review the .html report to decide whether trimming or filtering is needed before analysis.

## Optional: Adapter & Quality Trimming

```bash
fastp -i input_R1.fastq.gz -I input_R2.fastq.gz \
      -o trimmed_R1.fastq.gz -O trimmed_R2.fastq.gz \
      -q 20 -u 30 -l 50 -w 8 -h report.html -j report.json
```

- `-q`: Quality score cutoff
- `-u`: Max allowed % of low-quality bases per read
- `-l`: Minimum read length
- `-w`: Threads
- `-h`: Generate HTML report
- `-j`: Generate JSON summary
