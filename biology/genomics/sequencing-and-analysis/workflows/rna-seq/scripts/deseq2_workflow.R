#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(DESeq2)
})

count_file <- commandArgs(trailingOnly = TRUE)[1]
metadata_file <- commandArgs(trailingOnly = TRUE)[2]
out_dir <- commandArgs(trailingOnly = TRUE)[3]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

counts_tbl <- read_csv(count_file, show_col_types = FALSE)
metadata <- read_csv(metadata_file, show_col_types = FALSE)
counts <- round(as.matrix(counts_tbl[, metadata$sample_id]))
rownames(counts) <- counts_tbl[[1]]
metadata$group <- relevel(factor(metadata$group), ref = "control")

dds <- DESeqDataSetFromMatrix(countData = counts, colData = metadata, design = ~ group)
dds <- dds[rowSums(counts(dds) >= 10) >= 3, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("group", "treated", "control"), alpha = 0.05)
res_df <- as.data.frame(res)
write_csv(cbind(gene_id = rownames(res_df), res_df), file.path(out_dir, "deseq2_wald_results.csv"))

if (requireNamespace("apeglm", quietly = TRUE)) {
  shr <- lfcShrink(dds, coef = "group_treated_vs_control", type = "apeglm")
  write_csv(cbind(gene_id = rownames(shr), as.data.frame(shr)), file.path(out_dir, "deseq2_lfc_shrunk_results.csv"))
}

