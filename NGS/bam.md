# BAM

## Generate alignment statistics

```bash
samtools stats -@ threads_no input.bam > input.bam.stats
plot-bamstats -p prefix_name input.bam.stats #-p test/ will create files in test folder
```

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
