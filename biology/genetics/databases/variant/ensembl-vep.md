# Ensembl Variant Effect Predictor

Ensembl Variant Effect Predictor, often abbreviated VEP, annotates sequence variants with predicted consequences on genes, transcripts, proteins, regulatory regions, and known variant resources.

## Useful For

- Converting VCF or variant coordinates into transcript-level consequences
- Adding predicted effects such as missense, synonymous, splice-region, frameshift, and regulatory consequences
- Annotating variants with Ensembl, MANE, dbSNP, ClinVar, gnomAD, and plugin-derived fields when configured

## Access

- Web tool: [https://www.ensembl.org/Tools/VEP](https://www.ensembl.org/Tools/VEP)
- Documentation: [https://www.ensembl.org/info/docs/tools/vep/index.html](https://www.ensembl.org/info/docs/tools/vep/index.html)

## Notes

- Record the VEP version, Ensembl release, cache version, genome build, transcript set, and plugins.
- Predicted consequence is not the same as clinical classification.
- Transcript choice can change the reported consequence, especially near exon boundaries or in genes with many isoforms.
