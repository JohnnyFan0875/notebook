# BAM

## Generate alignment statistics

- option 1

```bash
samtools stats -@ threads_no input.bam > input.bam.stats
plot-bamstats -p prefix_name input.bam.stats #-p test/ will create files in test folder
```

```text
# output
```

- option 2

```bash
samtools flagstats input.bam > input.bam.stats
```

```text
# output
363458 + 0 in total (QC-passed reads + QC-failed reads)
363458 + 0 primary
0 + 0 secondary
0 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
362756 + 0 mapped (99.81% : N/A)
362756 + 0 primary mapped (99.81% : N/A)
0 + 0 paired in sequencing
0 + 0 read1
0 + 0 read2
0 + 0 properly paired (N/A : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (N/A : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)
```

- For detail information, please referred to the following documentations
  - **Biostars**: [PDF](reference/samtools_flagstas_result.pdf) | [Website](https://www.biostars.org/p/268550/)
  - **Biostars**: [PDF](reference/samtools_flagstas_result_2.pdf) | [Website](https://www.biostars.org/p/149883/#149889)

---

## Calculate coverage by a BED file

### Region-level coverage

```bash
samtools bedcov regions.bed input.bam > coverage_output.txt
```

```text
# output

chr12   25358179        25362845        KRAS    1       0
chr12   25378547        25378707        KRAS    1       709757
chr12   25380167        25380346        KRAS    1       501596
chr12   25398207        25398329        KRAS    1       877467
```

### Per-base coverage

```bash
samtools depth -b regions.bed input.bam > per_base_coverage.txt
```

```text
# output

chr12   25378548        4909
chr12   25378549        4903
chr12   25378550        4907
```
