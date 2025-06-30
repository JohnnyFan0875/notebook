## Generate alignment statistics

### `samtools stats` method

```bash
samtools stats -@ threads_no input.bam > input.bam.stats
plot-bamstats -p prefix_name input.bam.stats #-p test/ will create files in test folder
```

### `samtools flagstats` method

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
  - **Biostars**: [PDF](samtools_flagstats_reference_01.pdf) | [Website](https://www.biostars.org/p/268550/)
  - **Biostars**: [PDF](samtools_flagstats_reference_02.pdf) | [Website](https://www.biostars.org/p/149883/#149889)
