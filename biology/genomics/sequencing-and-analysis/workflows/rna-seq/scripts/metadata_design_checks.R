#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(readr))

count_file <- commandArgs(trailingOnly = TRUE)[1]
metadata_file <- commandArgs(trailingOnly = TRUE)[2]

counts <- read_csv(count_file, show_col_types = FALSE)
metadata <- read_csv(metadata_file, show_col_types = FALSE)

gene_cols <- intersect(c("gene_id", "gene_symbol", "length"), names(counts))
count_mat <- as.matrix(counts[, setdiff(names(counts), gene_cols)])
rownames(count_mat) <- counts[[1]]
metadata$sample_id <- as.character(metadata$sample_id)

stopifnot(!anyDuplicated(metadata$sample_id))
stopifnot(!anyDuplicated(colnames(count_mat)))
stopifnot(setequal(colnames(count_mat), metadata$sample_id))

metadata <- metadata[match(colnames(count_mat), metadata$sample_id), ]
stopifnot(identical(colnames(count_mat), metadata$sample_id))
stopifnot(!anyNA(metadata))

print(table(metadata$group))

design <- model.matrix(~ group + batch + sex + age, data = metadata)
cat("Design columns:\n")
print(colnames(design))
cat("Rank:", qr(design)$rank, "of", ncol(design), "\n")
if (qr(design)$rank < ncol(design)) {
  stop("Design matrix is not full rank. Check confounding or redundant variables.")
}

