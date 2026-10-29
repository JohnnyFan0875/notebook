#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(edgeR)
  library(limma)
})

args <- commandArgs(trailingOnly = TRUE)
count_file <- args[1]
metadata_file <- args[2]
out_dir <- args[3]
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
y <- normLibSizes(y)
png(file.path(out_dir, "voom_mean_variance.png"), width = 800, height = 600)
v <- voom(y, design, plot = TRUE)
dev.off()
fit <- lmFit(v, design)
contrast <- makeContrasts(treated - control, levels = design)
fit2 <- contrasts.fit(fit, contrast)
fit2 <- eBayes(fit2)
res <- topTable(fit2, number = Inf, sort.by = "P")
write_csv(cbind(gene_id = rownames(res), as.data.frame(res)), file.path(out_dir, "limma_voom_results.csv"))

