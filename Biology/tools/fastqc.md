# FastQC

---

[FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) is a widely used tool for performing quality control checks on raw high-throughput sequencing data (FASTQ files). It provides an overview of per-base sequence quality, GC content, adapter contamination, and other technical artifacts.

## Key Features

---

- **Per base sequence quality**
- **Per sequence GC content**
- **Adapter content detection**
- **K-mer overrepresentation**
- **Sequence duplication levels**
- **Per base N content**
- Generates an interactive **HTML report**

> Review the .html report to decide whether trimming or filtering is needed before analysis.

## How to Run FastQC

---

Install with Conda:

```bash
conda install -c bioconda fastqc
```

Run on a single FASTQ file:

```bash
fastqc sample_R1.fastq.gz
```

Run on multiple files and output to a directory:

```bash
fastqc *.fastq.gz -o ./fastqc_reports/
```

- `-t`: Number of threads (faster with more cores)

Output:

- `.html` file for interactive summary
- `.zip` file containing raw data and metrics

## Reference

---

- **CSDN**: ([Website](https://blog.csdn.net/qq_44520665/article/details/113779792) | [PDF](fastqc_reference_01.pdf))
