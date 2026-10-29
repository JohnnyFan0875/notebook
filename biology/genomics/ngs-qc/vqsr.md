# VQSR vs Hard Filtering

Variant Quality Score Recalibration (VQSR) models variant annotation patterns from trusted call sets and uses that model to separate likely true variants from technical artifacts.

## VQSR

- Common in large germline workflows
- Uses annotation features such as QD, MQ, FS, and SOR
- Needs enough variants and suitable training resources

## Hard Filtering

- Applies explicit cutoffs to each metric
- Useful when sample size is small or VQSR is unstable
- Easier to explain but less adaptive

## Reference

- [VQSR and hard filtering overview](https://huangshujia.com/2018/03/2018-03-23-wgs-best-practics-2/)
