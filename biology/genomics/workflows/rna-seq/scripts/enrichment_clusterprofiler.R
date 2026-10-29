#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(enrichplot)
})

de_file <- commandArgs(trailingOnly = TRUE)[1]
universe_file <- commandArgs(trailingOnly = TRUE)[2]
out_dir <- commandArgs(trailingOnly = TRUE)[3]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

de <- read_csv(de_file, show_col_types = FALSE)
universe <- read_csv(universe_file, show_col_types = FALSE)

sig_symbols <- de %>%
  filter(!is.na(FDR), FDR < 0.05, abs(logFC) >= 1, !is.na(gene_symbol)) %>%
  pull(gene_symbol) %>%
  unique()

universe_symbols <- universe %>%
  filter(!is.na(gene_symbol)) %>%
  pull(gene_symbol) %>%
  unique()

sig_entrez <- bitr(sig_symbols, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
universe_entrez <- bitr(universe_symbols, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)

ego <- enrichGO(
  gene = unique(sig_entrez$ENTREZID),
  universe = unique(universe_entrez$ENTREZID),
  OrgDb = org.Hs.eg.db,
  ont = "BP",
  pAdjustMethod = "BH",
  minGSSize = 10,
  maxGSSize = 500,
  readable = TRUE
)

write_csv(as.data.frame(ego), file.path(out_dir, "go_bp_ora_results.csv"))
png(file.path(out_dir, "go_bp_dotplot.png"), width = 1100, height = 750)
print(dotplot(ego, showCategory = 15))
dev.off()

ranked <- de %>%
  filter(!is.na(logFC), !is.na(gene_symbol)) %>%
  distinct(gene_symbol, .keep_all = TRUE) %>%
  arrange(desc(logFC))
rank_df <- bitr(ranked$gene_symbol, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
ranked <- ranked %>% inner_join(rank_df, by = c("gene_symbol" = "SYMBOL"))
gene_list <- ranked$logFC
names(gene_list) <- ranked$ENTREZID
gene_list <- sort(gene_list, decreasing = TRUE)

gsea <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, ont = "BP", pAdjustMethod = "BH")
write_csv(as.data.frame(gsea), file.path(out_dir, "go_bp_gsea_results.csv"))

