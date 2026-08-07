#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(edgeR)
})

count_file <- commandArgs(trailingOnly = TRUE)[1]
metadata_file <- commandArgs(trailingOnly = TRUE)[2]
out_dir <- commandArgs(trailingOnly = TRUE)[3]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

counts_tbl <- read_csv(count_file, show_col_types = FALSE)
metadata <- read_csv(metadata_file, show_col_types = FALSE)
sample_cols <- metadata$sample_id
counts <- as.matrix(counts_tbl[, sample_cols])
rownames(counts) <- counts_tbl[[1]]

metadata$group <- relevel(factor(metadata$group), ref = "control")
design <- model.matrix(~ group, data = metadata)
y <- DGEList(counts = counts, group = metadata$group)
keep <- filterByExpr(y, design)
y <- y[keep, , keep.lib.sizes = FALSE]
y <- calcNormFactors(y, method = "TMM")
y <- estimateDisp(y, design)
fit <- glmQLFit(y, design)
qlf <- glmQLFTest(fit, coef = "grouptreated")
res <- topTags(qlf, n = Inf)$table
write_csv(cbind(gene_id = rownames(res), as.data.frame(res)), file.path(out_dir, "edger_qlf_results.csv"))
saveRDS(y, file.path(out_dir, "edger_dgelist_filtered_normalized.rds"))

