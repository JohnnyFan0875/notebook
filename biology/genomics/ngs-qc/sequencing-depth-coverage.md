# Sequencing Depth and Coverage

Depth and coverage describe different aspects of sequencing completeness and confidence.

## Definitions

- Depth: the number of reads supporting a genomic position, often written as `30x` or `100x`.
- Coverage: the proportion of target bases that meet a chosen depth threshold.

## Why the Distinction Matters

- High mean depth does not guarantee uniform performance across all targets.
- Clinical panels often care about the percent of target bases above a minimum threshold.
- Low coverage regions can hide variants even when the average depth looks acceptable.

## Reference

- [Sequencing depth vs coverage](https://3billion.io/blog/sequencing-depth-vs-coverage)
