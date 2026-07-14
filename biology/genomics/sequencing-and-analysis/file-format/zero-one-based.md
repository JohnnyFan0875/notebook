# One-Based vs Zero-Based Coordinates

Genome coordinate systems differ across file formats and browsers, so off-by-one mistakes are a common source of annotation errors.

## Quick Rule

- One-based: the first base is position 1.
- Zero-based half-open: the first base starts at 0 and the end position is excluded.

## Common Examples

- VCF and HGVS are typically one-based.
- BED is zero-based half-open.

## Conversion Example

A single base at position 101 in a one-based system becomes `100-101` in a zero-based BED interval.

## Reference

- [One-based vs zero-based](https://qinqianshan.com/biology/bioknowledge/one-based-and-zero-based/)
