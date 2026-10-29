# Fastp

[fastp](https://github.com/OpenGene/fastp) is a fast and versatile tool for preprocessing FASTQ files. It performs quality filtering, adapter trimming, polyG/polyX trimming, per-base correction, and generates QC reports — all in one step.

## Key Features

- Quality filtering and trimming
- Adapter detection and removal (automatic or manual)
- PolyG tail trimming (for Illumina NextSeq/NovaSeq)
- Base correction for overlapping paired-end reads
- UMI preprocessing
- Quality control report in **HTML** and **JSON**
- Multi-threaded for high speed

## Usage

Install with Conda:

```bash
conda install -c bioconda fastp
```

Basic usage for paired-end reads:

```bash
fastp -i sample_R1.fastq.gz -I sample_R2.fastq.gz \
      -o clean_R1.fastq.gz -O clean_R2.fastq.gz \
      -h report.html -j report.json
```

For single-end:

```bash
fastp -i sample_SE.fastq.gz -o clean_SE.fastq.gz \
      -h report.html -j report.json
```

Outputs:

- `clean_R1.fastq.gz`, `clean_R2.fastq.gz`: Filtered and trimmed reads
- `report.html`: Interactive quality report
- `report.json`: Machine-readable QC stats

## When to Use Fastp

- Run it before alignment or assembly.
- Review the HTML report to confirm trimming and filtering behavior.
- Pair it with FastQC when you want both preprocessing and a standalone QC report.
