# Base Quality

Base quality is the confidence assigned to each base call in a sequencing read.

## Interpretation

- Usually encoded as a Phred-style score
- Higher values indicate lower estimated error probability
- Per-base quality plots help detect cycle-specific degradation

## Practical Notes

- Low-quality tails are often trimmed during preprocessing.
- Base quality influences alignment, variant calling, and downstream filtering.
