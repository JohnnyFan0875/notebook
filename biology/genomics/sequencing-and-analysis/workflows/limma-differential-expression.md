# Differential Expression with limma

`limma` is a Bioconductor workflow for differential expression analysis built around linear models. The important idea is that we fit the same design logic to every gene, then stabilize variance estimates with empirical Bayes shrinkage.

This makes `limma` useful for:

- two-group comparisons
- multiple phenotype groups
- factorial designs
- interaction effects
- batch-aware expression analysis

## Core Mental Model

At a high level, the workflow is:

1. inspect expression distributions
2. log-transform if needed
3. normalize across samples
4. filter weakly expressed features
5. encode the study design with a design matrix
6. define biological questions as contrasts
7. fit gene-wise linear models
8. apply empirical Bayes moderation
9. summarize, rank, and visualize differential signals

The course repeatedly reinforces that differential expression is mostly a design problem. If the design matrix and contrasts correctly encode the biology, the downstream testing becomes much more straightforward.

## Pre-processing

### Inspect Sample Distributions

Before modeling, inspect whether samples have comparable expression distributions:

```r
library(limma)
plotDensities(eset, legend = FALSE)
```

Density plots are a quick check for:

- shifts in sample intensity distributions
- obvious outlier samples
- whether normalization is still needed

### Log Transform

Expression values are often easier to model on a log scale because multiplicative differences become additive:

```r
exprs(eset) <- log(exprs(eset))
plotDensities(eset, legend = FALSE)
```

The practical goal is not "always log-transform", but to put measurements onto a scale where variance is more stable and between-sample comparisons are interpretable.

### Quantile Normalization

When the sample distributions are not aligned, the course uses quantile normalization:

```r
exprs(eset) <- normalizeBetweenArrays(exprs(eset))
plotDensities(eset, legend = FALSE)
```

Quantile normalization forces samples to share a comparable marginal distribution. This is especially common in array-oriented workflows, where technical distributional differences can otherwise dominate biological comparisons.

### Filter Low-Signal Features

Weakly expressed genes usually add noise and multiple-testing burden without helping inference:

```r
plotDensities(eset, legend = FALSE)
abline(v = 5)
keep <- rowMeans(exprs(eset)) > 5
eset <- eset[keep, ]
plotDensities(eset, legend = FALSE)
```

The exact threshold depends on platform and preprocessing, but the principle is stable: remove features that are too close to background to support reliable differential testing.

## Modeling with Design Matrices

The central `limma` abstraction is the design matrix:

```r
design <- model.matrix(~er, data = pData(eset))
```

This turns sample annotations into coefficients that can be interpreted biologically. For a simple two-group comparison, one coefficient usually plays the role of the reference level and another captures the group effect.

For group-means parameterization, the course often uses a no-intercept design:

```r
design <- model.matrix(~0 + er, data = pData(eset))
```

This parameterization is convenient because each coefficient corresponds directly to a group mean, which makes custom contrasts easier to read.

Key point: different parameterizations can encode the same biological question. A good workflow chooses the representation that makes coefficients and contrasts easiest to interpret.

## Contrasts Represent the Biological Question

Once the design matrix defines what can be estimated, contrasts define what should be tested.

For a two-group comparison:

```r
cm <- makeContrasts(
  status = erpositive - ernegative,
  levels = design
)
```

For multiple disease groups, several contrasts can be tested in one model:

```r
cm <- makeContrasts(
  AMLvALL = typeAML - typeALL,
  CMLvALL = typeCML - typeALL,
  CMLvAML = typeCML - typeAML,
  levels = design
)
```

This is one of `limma`'s biggest strengths: fit one design, then ask multiple related biological questions without rebuilding the whole workflow from scratch.

## Standard limma Testing Pipeline

The core testing sequence is:

```r
fit <- lmFit(eset, design)
fit2 <- contrasts.fit(fit, contrasts = cm)
fit2 <- eBayes(fit2)
results <- decideTests(fit2)
```

How to read this:

- `lmFit()` estimates gene-wise model coefficients
- `contrasts.fit()` rewrites those coefficients into the comparisons you care about
- `eBayes()` moderates standard errors across genes
- `decideTests()` summarizes which genes are up, down, or not significant

The empirical Bayes step is the conceptual center of `limma`. It borrows strength across genes so that variance estimates are less unstable than fully separate per-gene models.

## Inspecting Ranked Results

Use `topTable()` to inspect the strongest signals:

```r
topTable(fit2, number = 3)
stats <- topTable(fit2, number = nrow(fit2), sort.by = "none")
```

`topTable()` is useful for:

- ranked candidate genes
- fold-change and p-value inspection
- exporting complete result tables

`decideTests()` and `topTable()` answer different questions:

- `decideTests()` summarizes how many genes pass thresholds
- `topTable()` shows the per-gene statistics behind those summaries

## Exploring Sources of Variation

The course uses `plotMDS()` to see whether major expression differences line up with known biology:

```r
plotMDS(eset, labels = pData(eset)[, "time"], gene.selection = "common")
plotMDS(eset, labels = pData(eset)[, "genotype"], gene.selection = "common")
plotMDS(eset, labels = pData(eset)[, "treatment"], gene.selection = "common")
```

This is useful for checking:

- whether replicates cluster together
- whether treatment or phenotype separates samples
- whether hidden technical structure is dominating the data

If major structure does not match the study design, pause before interpreting p-values.

## Batch Effects

If unwanted technical structure is visible, the course shows batch adjustment with `removeBatchEffect()`:

```r
exprs(eset) <- removeBatchEffect(
  exprs(eset),
  batch = pData(eset)[, "batch"],
  covariates = pData(eset)[, "rin"]
)
```

This is useful for exploratory visualization and cleaned expression summaries, but the larger lesson is that batch should be modeled deliberately rather than treated as an afterthought.

## Factorial and Interaction Designs

`limma` becomes especially helpful when the experiment has more than one factor.

A 2x2 design can be encoded by collapsing factors into a combined group label:

```r
group <- with(pData(eset), paste(genotype, treatment, sep = "."))
group <- factor(group)

design <- model.matrix(~0 + group)
colnames(design) <- levels(group)
```

Then define contrasts for specific biological questions:

```r
cm <- makeContrasts(
  dox_wt = wt.dox - wt.pbs,
  dox_top2b = top2b.dox - top2b.pbs,
  interaction = (top2b.dox - top2b.pbs) - (wt.dox - wt.pbs),
  levels = design
)
```

This pattern is important:

- main-condition response can be tested within each genotype
- genotype-specific response can be compared between conditions
- the interaction contrast directly asks whether treatment response differs by genotype

In practice, many biological studies are less about "case vs control" and more about whether one perturbation changes the effect of another. `limma` handles that naturally.

## Common Diagnostic Plots

The course repeatedly uses a few plotting patterns:

- density plots with `plotDensities()`
- MDS views with `plotMDS()`
- ranked result tables with `topTable()`
- p-value histograms with `hist(...)`
- volcano plots with `volcanoplot()`

Example volcano plot:

```r
gene_symbols <- fit2$genes[, "symbol"]
volcanoplot(fit2, coef = "dox_wt", highlight = 5, names = gene_symbols)
```

These views are complementary:

- density plots check preprocessing
- MDS checks global structure
- p-value histograms check signal shape and calibration
- volcano plots highlight effect size versus significance

## Gene Set Follow-up

The material also points to gene set methods such as `camera` and `roast`.

This reflects an important downstream idea: differential expression often starts at single genes, but interpretation usually moves toward pathways, programs, or coordinated biological processes.

## Practical Workflow

A compact reusable workflow is:

1. load an expression object with feature and sample metadata
2. inspect sample distributions with `plotDensities()`
3. log-transform and normalize when appropriate
4. filter weak features
5. inspect sample structure with `plotMDS()`
6. build `design <- model.matrix(...)`
7. define `cm <- makeContrasts(...)`
8. run `lmFit()`, `contrasts.fit()`, and `eBayes()`
9. summarize with `decideTests()` and `topTable()`
10. visualize selected contrasts with p-value histograms and volcano plots

## Takeaways

- `limma` is fundamentally a linear-model framework for expression data
- the design matrix determines what biological effects are estimable
- contrasts translate biological questions into statistical tests
- empirical Bayes moderation is the main reason `limma` is so stable and widely used
- preprocessing, batch awareness, and diagnostic plots are part of the analysis, not optional extras
