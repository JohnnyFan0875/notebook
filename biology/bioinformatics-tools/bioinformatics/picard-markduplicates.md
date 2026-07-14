# Picard MarkDuplicates

Picard `MarkDuplicates` identifies duplicate reads that likely arose during PCR amplification or optical duplication. Marking duplicates is a common preprocessing step before variant calling.

## What It Does

- Scans aligned reads in a BAM file
- Groups reads with the same alignment signature
- Marks duplicate records instead of deleting them by default
- Produces metrics for duplication review

## Example

```bash
picard MarkDuplicates \
  I=aligned.bam \
  O=dedup.bam \
  M=marked_dup_metrics.txt
```

## Notes

- Run it after alignment and coordinate sorting.
- Review the metrics output together with coverage and library complexity.
