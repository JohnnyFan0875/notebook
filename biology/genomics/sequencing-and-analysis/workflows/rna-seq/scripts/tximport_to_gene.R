#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(tximport)
})

metadata_file <- commandArgs(trailingOnly = TRUE)[1]
tx2gene_file <- commandArgs(trailingOnly = TRUE)[2]
quant_dir <- commandArgs(trailingOnly = TRUE)[3]
out_dir <- commandArgs(trailingOnly = TRUE)[4]

dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
metadata <- read_csv(metadata_file, show_col_types = FALSE)
tx2gene <- read_tsv(tx2gene_file, col_names = c("TXNAME", "GENEID"), show_col_types = FALSE)

files <- file.path(quant_dir, metadata$sample_id, "quant.sf")
names(files) <- metadata$sample_id
stopifnot(all(file.exists(files)))

txi <- tximport(
  files,
  type = "salmon",
  tx2gene = tx2gene,
  countsFromAbundance = "lengthScaledTPM"
)

write_csv(as.data.frame(txi$counts), file.path(out_dir, "gene_counts_from_tximport.csv"))
write_csv(as.data.frame(txi$abundance), file.path(out_dir, "gene_tpm_from_tximport.csv"))
write_csv(as.data.frame(txi$length), file.path(out_dir, "gene_effective_length_from_tximport.csv"))

