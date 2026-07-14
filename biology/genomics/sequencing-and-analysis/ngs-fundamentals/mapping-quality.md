# Mapping Quality

Mapping quality (MAPQ) estimates how confidently a read is aligned to a genomic location.

## Why It Matters

- Low MAPQ often reflects ambiguous or repetitive alignments.
- MAPQ filtering can improve variant calling specificity.
- Exact scoring differs across aligners, so tool-specific interpretation is important.

## Notes

- Review MAPQ distributions together with read length, reference complexity, and alignment parameters.
