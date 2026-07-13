# Structural Equation Modeling with lavaan

Structural equation modeling (SEM) lets us describe relationships among **observed variables**, **latent variables**, and sometimes even **other latent variables** in one model. In practice, `lavaan` is one of the most common R packages for fitting these models.

Key point: SEM is not just "regression with arrows." Its real value is that it combines measurement models and structural relationships in the same framework.

## Why SEM Exists

SEM is usually worth considering when:

- several survey items are intended to measure the same latent construct
- you want to test a confirmatory factor structure rather than only explore one
- multiple relationships among variables should be evaluated together
- measurement error should be modeled explicitly rather than ignored

This makes SEM especially useful for:

- confirmatory factor analysis (CFA)
- latent-variable path models
- mediation with latent constructs
- higher-order factor models

## Manifest vs Latent Variables

A basic SEM diagram separates two kinds of variables:

- **Manifest variables**: directly observed values in the dataset
- **Latent variables**: unobserved constructs inferred from manifest indicators

Typical mental picture:

- squares = manifest variables
- circles or ovals = latent variables

For example, a latent construct like `visual` may be measured by observed test items `x1`, `x2`, and `x3`.

## The Most Important lavaan Syntax

`lavaan` uses a compact formula language. The most important operator is:

- `=~` : a latent variable is measured by observed indicators

Example:

```r
library(lavaan)

visual.model <- '
  visual =~ x1 + x2 + x3
'

visual.fit <- cfa(model = visual.model, data = HolzingerSwineford1939)
summary(visual.fit, standardized = TRUE, fit.measures = TRUE)
```

Read this as:

- `visual` is a latent factor
- `x1`, `x2`, and `x3` are indicators of that factor

If you only remember one line of `lavaan` syntax, remember this one.

## CFA as the First Practical SEM Use Case

A lot of real `lavaan` usage starts as CFA.

Why?

- you already have a theory about which items should belong to which factor
- you want to test whether the proposed measurement structure is plausible
- exploratory factor analysis is no longer the main question

Example with more than one factor:

```r
multi.model <- '
  visual =~ x1 + x2 + x3
  speed  =~ x7 + x8 + x9
'

multi.fit <- cfa(model = multi.model, data = HolzingerSwineford1939)
summary(multi.fit, standardized = TRUE, fit.measures = TRUE)
```

Key point: fitting two separate small CFAs is not the same as fitting one joint multifactor model. The joint model can estimate how the latent factors relate to each other.

## Why a Joint Multifactor Model Matters

Suppose `visual` and `speed` are both real constructs in the same test battery.

If you fit them separately:

- each factor is evaluated in isolation
- relationships between factors are hidden
- overall model structure is not tested jointly

If you fit them together:

- cross-factor structure becomes explicit
- latent covariances can be estimated
- model fit reflects the full confirmatory hypothesis

This is one of the main reasons SEM is richer than just running several isolated regressions or factor models.

## Interpreting Fit Indices

`summary(..., fit.measures = TRUE)` often reports a set of global fit indices. Common ones include:

- `CFI`
- `TLI`
- `RMSEA`
- `SRMR`

These do not answer exactly the same question:

- `CFI` / `TLI` compare your model to a weaker baseline model
- `RMSEA` asks how much approximate misfit remains per degree of freedom
- `SRMR` summarizes residual discrepancy in the correlation or covariance structure

Practical habit: do not judge a model from one fit index alone. Fit interpretation is much more stable when several indices and the parameter estimates point in the same direction.

## Standardized Solutions Matter

When reviewing a fitted SEM, the standardized output is often easier to interpret than raw coefficients:

```r
summary(fit, standardized = TRUE, fit.measures = TRUE)
```

Standardized loadings are useful for asking:

- which indicators strongly represent the latent construct
- whether some items load much more weakly than expected
- whether a factor appears poorly defined

Very weak or inconsistent loadings are often a model-quality signal, not just a numerical detail.

## Higher-Order Factor Models

SEM becomes especially powerful when latent variables themselves are modeled as outcomes of broader latent traits.

A higher-order model might say:

- `verbal_comp` and `working_memory` are first-order factors
- both are explained by a second-order factor like `verbal_iq`

Likewise:

- `perceptual_org` and `processing_speed` may load onto `performance_iq`

This is useful when a test battery has:

- many observed items
- several domain factors
- one or more broader umbrella constructs

Key point: higher-order SEM asks whether several first-order latent traits themselves reflect a more general latent structure.

## Structural Paths

Once measurement models are defined, SEM can also express directional relationships among latent variables or observed outcomes.

Conceptually, this shifts the question from:

- "Which items measure this construct?"

to:

- "How do these constructs relate to each other?"

That is what makes SEM different from CFA alone. CFA focuses on measurement. SEM adds structural relations on top of measurement.

## Heywood Cases

One of the classic SEM problems is a **Heywood case**.

Typical signs include:

- negative variance estimates
- correlations outside valid bounds
- latent covariance matrices that are not positive definite

In `lavaan`, this often appears as a warning after fitting:

- covariance matrix of latent variables is not positive definite

The practical meaning is usually:

- the model is overstrained, misspecified, or poorly identified
- indicators may be too redundant
- sample size or data quality may be insufficient

This is not the kind of warning to ignore and keep reporting the output anyway.

## How to Investigate a Heywood Case

When `lavaan` warns about impossible latent relationships, inspect the fitted object rather than guessing:

```r
inspect(fit, "cov.lv")
```

Then check:

- are latent correlations implausibly close to `1` or `-1`?
- are some factors essentially duplicates of each other?
- do some indicators behave oddly or cross-load conceptually?

Practical interpretation:

- an out-of-bounds latent correlation often means two supposed factors are not empirically separable in this dataset
- a negative residual variance often suggests a badly behaving indicator or an overly aggressive model

## A Good SEM Workflow

In practice, a stable SEM workflow often looks like this:

1. define the theoretical measurement structure first
2. write the `lavaan` syntax explicitly
3. fit with `cfa()` or `sem()`
4. inspect global fit indices
5. inspect standardized loadings and latent covariances
6. investigate warnings before interpreting substantive results
7. only then discuss whether the structural theory is supported

This order matters because SEM can produce polished-looking output even when the underlying model is unstable.

## Common Mistakes

- using SEM with no clear measurement theory
- treating fit indices as a pass/fail checklist instead of model evidence
- fitting several isolated factor models instead of one coherent joint model
- ignoring Heywood warnings
- interpreting structural paths before confirming that the measurement model is acceptable
- treating latent factors as automatically real just because the software estimated them

## Where It Fits in the Bigger Picture

SEM sits naturally near CFA, factor structure, and multivariate latent-variable modeling. It is most useful when:

- multiple observed variables jointly measure fewer underlying constructs
- those constructs are part of a confirmatory theory
- the relationships among constructs matter, not just the raw item-level correlations

If PCA asks "what low-dimensional structure explains the variance?", SEM asks a more theory-driven question:

- "Does this hypothesized latent structure, and the relations among its parts, fit the data?"
