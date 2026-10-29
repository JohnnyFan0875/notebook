#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(edgeR)
  library(limma)
})

count_file <- commandArgs(trailingOnly = TRUE)[1]
metadata_file <- commandArgs(trailingOnly = TRUE)[2]
out_dir <- commandArgs(trailingOnly = TRUE)[3]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

counts_tbl <- read_csv(count_file, show_col_types = FALSE)
metadata <- read_csv(metadata_file, show_col_types = FALSE)
counts <- as.matrix(counts_tbl[, metadata$sample_id])
rownames(counts) <- counts_tbl[[1]]

metadata$group <- factor(metadata$group, levels = c("control", "treated"))
design <- model.matrix(~ 0 + group, data = metadata)
colnames(design) <- sub("^group", "", colnames(design))
y <- DGEList(counts = counts)
y <- y[filterByExpr(y, design), , keep.lib.sizes = FALSE]
y <- calcNormFactors(y)
v <- voom(y, design, plot = TRUE)
fit <- lmFit(v, design)
contrast <- makeContrasts(treated - control, levels = design)
fit2 <- contrasts.fit(fit, contrast)
fit2 <- eBayes(fit2)
res <- topTable(fit2, number = Inf, sort.by = "P")
write_csv(cbind(gene_id = rownames(res), as.data.frame(res)), file.path(out_dir, "limma_voom_results.csv"))

