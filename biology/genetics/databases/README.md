# Genetics Databases

Genetics and genomics databases answer different questions. A good lookup usually moves from a stable gene or variant identifier, to disease evidence, population frequency, functional annotation, and then to domain-specific resources such as pharmacogenomics or cancer databases.

## Where This Fits

The content from `~/project/source.txt` belongs here rather than under `data-science/statistics`: it is about biomedical reference databases, not statistical methods. The closest notebook location is `biology/genetics/databases`, with some cross-links to molecular biology and genomics pages when the resource is protein- or genome-browser-centered.

## Modules

| Module | Core Databases | Main Questions |
| ------ | -------------- | -------------- |
| [Gene Databases](gene/README.md) | NCBI Gene, HGNC, GeneCards, Ensembl, UCSC Genome Browser | What is this gene, where is it located, and what identifiers or transcripts should I use? |
| [Gene-Disease Association](gene-disease-association/README.md) | OMIM, ClinGen, GenCC, HPO, GeneReviews, HGMD | Which diseases or phenotypes are associated with this gene, and how strong is the evidence? |
| [Variant Databases](variant/README.md) | ClinVar, dbSNP, GWAS Catalog, COSMIC, VEP, VarSome, OpenCRAVAT | What is this variant, how has it been interpreted, and what functional impact is predicted? |
| [Population Frequency](population-frequency/README.md) | gnomAD, 1000 Genomes, Taiwan Biobank/TaiwanGenomes, HGVD | How common is this variant in reference populations? |
| [Pharmacogenomics](pharmacogenomics/README.md) | PharmGKB, CIViC | Does the variant or gene affect drug response or treatment evidence? |
| [Functional and Expression Databases](functional-expression/README.md) | GTEx, KEGG, UniProt, InterPro, Human Protein Atlas | Where is the gene expressed, what pathway is it in, and what does the protein do? |

## Practical Lookup Workflow

| Step | Use | Why It Matters |
| ---- | --- | -------------- |
| Identify the gene or variant | NCBI Gene, HGNC, Ensembl, dbSNP | Prevents errors from aliases, deprecated symbols, and genome-build mismatches |
| Check clinical evidence | ClinVar, OMIM, ClinGen, GenCC, GeneReviews | Separates curated disease relationships from broad database mentions |
| Check population frequency | gnomAD, 1000 Genomes, local population databases | Common variants are usually less likely to explain rare Mendelian disease |
| Review predicted or observed function | VEP, UniProt, InterPro, GTEx, KEGG | Connects genomic change to transcript, protein, tissue, and pathway context |
| Add domain-specific evidence | COSMIC, PharmGKB, CIViC, GWAS Catalog | Cancer, drug response, and complex-trait interpretation often require separate evidence streams |

## Notes

- Do not treat one database as final evidence. Cross-check identifiers, genome build, transcript version, phenotype terminology, and evidence level.
- Gene-level resources are useful for orientation, but clinical interpretation usually depends on variant-level evidence and disease context.
- Subscription databases such as HGMD can be useful, but access restrictions and licensing should be documented in any reproducible workflow.
