# Quality Score

Sequencing quality scores estimate the probability that a called base is incorrect. They are commonly represented on the Phred scale.

## Phred Scale

`Q = -10 log10(P error)`

- `Q20`: about 1 error in 100 bases
- `Q30`: about 1 error in 1000 bases
- `Q40`: about 1 error in 10000 bases

## Why It Matters

- Base quality affects alignment confidence and variant calling accuracy.
- Per-cycle quality decay can indicate run or library issues.
- Quality filtering is often part of FASTQ preprocessing.

## Reference

- [Illumina quality score note](https://www.illumina.com/documents/products/technotes/technote_Q-Scores.pdf)
