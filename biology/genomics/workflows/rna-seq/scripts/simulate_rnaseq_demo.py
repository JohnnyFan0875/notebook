#!/usr/bin/env python3
"""Generate small simulated RNA-seq teaching data and figures.

The generated data are for workflow demonstration only. They are not biological
findings and should not be used as benchmark truth.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def geometric_mean(x: np.ndarray) -> float:
    x = x[x > 0]
    if len(x) == 0:
        return np.nan
    return float(np.exp(np.mean(np.log(x))))


def bh_adjust(p_values: np.ndarray) -> np.ndarray:
    order = np.argsort(p_values)
    ranked = p_values[order]
    n = len(p_values)
    adj = ranked * n / np.arange(1, n + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty_like(adj)
    out[order] = np.minimum(adj, 1)
    return out


def pca_2d(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = x - x.mean(axis=0, keepdims=True)
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    scores = u[:, :2] * s[:2]
    var = (s**2) / np.sum(s**2)
    return scores, var[:2]


def savefig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="biology/genomics/sequencing-and-analysis/workflows/rna-seq")
    parser.add_argument("--seed", type=int, default=20260727)
    args = parser.parse_args()

    root = Path(args.outdir)
    data_dir = root / "data"
    fig_dir = root / "src"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)
    n_genes = 1200
    samples = [f"ctrl_{i}" for i in range(1, 4)] + [f"treat_{i}" for i in range(1, 4)]
    group = np.array(["control"] * 3 + ["treated"] * 3)
    batch = np.array(["batch1", "batch2", "batch1", "batch1", "batch2", "batch1"])
    sex = np.array(["F", "M", "F", "M", "F", "M"])

    base_mean = rng.gamma(shape=1.3, scale=120, size=n_genes)
    gene_length = rng.integers(500, 8000, size=n_genes)
    de_up = np.arange(0, 60)
    de_down = np.arange(60, 110)
    true_lfc = np.zeros(n_genes)
    true_lfc[de_up] = rng.normal(1.4, 0.25, len(de_up))
    true_lfc[de_down] = rng.normal(-1.2, 0.2, len(de_down))
    lib_size_factor = np.array([0.78, 1.1, 0.93, 1.35, 0.82, 1.18])
    composition_spike = np.ones((n_genes, len(samples)))
    composition_spike[110:125, 3:] = 5.0

    counts = np.zeros((n_genes, len(samples)), dtype=int)
    dispersion = 0.18
    for j in range(len(samples)):
        mu = base_mean * lib_size_factor[j] * composition_spike[:, j]
        if group[j] == "treated":
            mu = mu * (2 ** true_lfc)
        size = 1 / dispersion
        prob = size / (size + mu)
        counts[:, j] = rng.negative_binomial(size, prob)

    genes = [f"ENSGDEMO{idx:06d}" for idx in range(1, n_genes + 1)]
    symbols = [f"GENE{idx:04d}" for idx in range(1, n_genes + 1)]
    count_df = pd.DataFrame(counts, index=genes, columns=samples)
    count_df.insert(0, "gene_symbol", symbols)
    count_df.insert(1, "length", gene_length)
    count_df.to_csv(data_dir / "simulated_gene_counts.csv")

    metadata = pd.DataFrame({
        "sample_id": samples,
        "group": group,
        "batch": batch,
        "sex": sex,
        "age": [41, 38, 45, 42, 39, 44],
        "fastq1": [f"raw/{s}_R1.fastq.gz" for s in samples],
        "fastq2": [f"raw/{s}_R2.fastq.gz" for s in samples],
    })
    metadata.to_csv(data_dir / "sample_metadata.csv", index=False)

    count_mat = count_df[samples]
    lib_sizes = count_mat.sum(axis=0)
    detected = (count_mat > 0).sum(axis=0)
    zero_prop = (count_mat == 0).mean(axis=0)
    cpm = count_mat.div(lib_sizes, axis=1) * 1e6

    # DESeq2-like median-of-ratios size factors for demonstration.
    gmeans = count_mat.apply(lambda row: geometric_mean(row.values), axis=1)
    valid = gmeans.notna() & (gmeans > 0)
    ratios = count_mat.loc[valid].div(gmeans[valid], axis=0)
    size_factors = ratios.median(axis=0)
    norm_counts = count_mat.div(size_factors, axis=1)
    norm_cpm = norm_counts.div(norm_counts.sum(axis=0), axis=1) * 1e6

    # TMM-like factors are computed here only for teaching plots.
    ref = count_mat.columns[np.argsort(lib_sizes.values)[len(samples) // 2]]
    tmm = {}
    ref_counts = count_mat[ref]
    for sample in samples:
        y = count_mat[sample]
        keep = (y > 0) & (ref_counts > 0)
        m = np.log2((y[keep] / lib_sizes[sample]) / (ref_counts[keep] / lib_sizes[ref]))
        a = 0.5 * np.log2((y[keep] / lib_sizes[sample]) * (ref_counts[keep] / lib_sizes[ref]))
        lo_m, hi_m = np.quantile(m, [0.3, 0.7])
        lo_a, hi_a = np.quantile(a, [0.05, 0.95])
        trim = (m >= lo_m) & (m <= hi_m) & (a >= lo_a) & (a <= hi_a)
        tmm[sample] = 2 ** np.average(m[trim])
    tmm_factor = pd.Series(tmm)
    tmm_factor = tmm_factor / np.exp(np.mean(np.log(tmm_factor)))
    eff_lib = lib_sizes * tmm_factor
    tmm_cpm = count_mat.div(eff_lib, axis=1) * 1e6

    pd.DataFrame({
        "sample_id": samples,
        "library_size": lib_sizes.values,
        "deseq2_size_factor_demo": size_factors.values,
        "tmm_norm_factor_demo": tmm_factor.values,
        "effective_library_size_demo": eff_lib.values,
        "detected_genes": detected.values,
        "zero_proportion": zero_prop.values,
    }).to_csv(data_dir / "simulated_library_qc.csv", index=False)

    # Simple differential-expression table for visual teaching.
    log2fc = np.log2(norm_counts.iloc[:, 3:6].mean(axis=1) + 1) - np.log2(norm_counts.iloc[:, 0:3].mean(axis=1) + 1)
    se = 0.45 + 2.5 / np.sqrt(cpm.mean(axis=1) + 1)
    z = np.abs(log2fc) / se
    # Normal tail approximation without scipy.
    p = np.array([math.erfc(v / np.sqrt(2)) for v in z])
    fdr = bh_adjust(p)
    de_table = pd.DataFrame({
        "gene_id": genes,
        "gene_symbol": symbols,
        "logFC": log2fc.values,
        "logCPM": np.log2(cpm.mean(axis=1).values + 1),
        "PValue": p,
        "FDR": fdr,
        "is_simulated_true_de": true_lfc != 0,
    })
    de_table.to_csv(data_dir / "simulated_de_results.csv", index=False)

    colors = {"control": "#2f6f9f", "treated": "#c95f3f"}
    sample_colors = [colors[g] for g in group]

    plt.figure(figsize=(7.2, 4.2))
    plt.bar(samples, lib_sizes / 1e6, color=sample_colors)
    plt.ylabel("Library size (million reads)")
    plt.xticks(rotation=35, ha="right")
    plt.title("Simulated library size")
    savefig(fig_dir / "library-size-barplot.png")

    fig, ax1 = plt.subplots(figsize=(7.2, 4.2))
    ax1.bar(samples, detected, color=sample_colors, alpha=0.85)
    ax1.set_ylabel("Detected genes")
    ax1.tick_params(axis="x", rotation=35)
    ax2 = ax1.twinx()
    ax2.plot(samples, zero_prop, color="#333333", marker="o")
    ax2.set_ylabel("Zero count proportion")
    plt.title("Detected genes and zero count proportion")
    savefig(fig_dir / "detected-genes-zero-proportion.png")

    plt.figure(figsize=(7.2, 4.2))
    for sample in samples:
        vals = np.log2(cpm[sample] + 1)
        plt.hist(vals, bins=45, density=True, histtype="step", linewidth=1.5, label=sample)
    plt.xlabel("log2(CPM + 1)")
    plt.ylabel("Density")
    plt.title("Count distribution before filtering")
    plt.legend(fontsize=7, ncol=2)
    savefig(fig_dir / "count-distribution-logcpm-density.png")

    keep_filter = (cpm >= 1).sum(axis=1) >= 3
    plt.figure(figsize=(7.2, 4.2))
    for sample in samples:
        plt.hist(np.log2(cpm.loc[keep_filter, sample] + 1), bins=45, density=True,
                 histtype="step", linewidth=1.5, label=sample)
    plt.xlabel("log2(CPM + 1)")
    plt.ylabel("Density")
    plt.title("Log-CPM density after CPM filtering")
    plt.legend(fontsize=7, ncol=2)
    savefig(fig_dir / "filtered-logcpm-density.png")

    plt.figure(figsize=(7.2, 4.2))
    box_data = [np.log2(tmm_cpm.loc[keep_filter, s] + 1) for s in samples]
    plt.boxplot(box_data, tick_labels=samples, patch_artist=True)
    plt.ylabel("log2(TMM-normalized CPM + 1)")
    plt.xticks(rotation=35, ha="right")
    plt.title("Normalized expression boxplot")
    savefig(fig_dir / "normalized-expression-boxplot.png")

    corr = np.corrcoef(np.log2(tmm_cpm.loc[keep_filter] + 1).T)
    plt.figure(figsize=(5.2, 4.6))
    im = plt.imshow(corr, cmap="viridis", vmin=0.85, vmax=1)
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Pearson correlation")
    plt.xticks(range(len(samples)), samples, rotation=45, ha="right")
    plt.yticks(range(len(samples)), samples)
    plt.title("Sample correlation heatmap")
    savefig(fig_dir / "sample-correlation-heatmap.png")

    log_expr = np.log2(tmm_cpm.loc[keep_filter] + 1).T.values
    scores, var = pca_2d(log_expr)
    plt.figure(figsize=(5.8, 4.8))
    for g in np.unique(group):
        idx = group == g
        plt.scatter(scores[idx, 0], scores[idx, 1], s=80, label=g, color=colors[g])
        for x, y, label in zip(scores[idx, 0], scores[idx, 1], np.array(samples)[idx]):
            plt.text(x, y, label, fontsize=8, va="bottom")
    plt.axhline(0, color="#cccccc", linewidth=0.8)
    plt.axvline(0, color="#cccccc", linewidth=0.8)
    plt.xlabel(f"PC1 ({var[0] * 100:.1f}% variance)")
    plt.ylabel(f"PC2 ({var[1] * 100:.1f}% variance)")
    plt.legend(frameon=False)
    plt.title("PCA after filtering and normalization")
    savefig(fig_dir / "pca-after-filtering-normalization.png")

    plt.figure(figsize=(5.8, 4.8))
    d = np.linalg.norm(log_expr[:, None, :] - log_expr[None, :, :], axis=2)
    im = plt.imshow(d, cmap="magma_r")
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Euclidean distance")
    plt.xticks(range(len(samples)), samples, rotation=45, ha="right")
    plt.yticks(range(len(samples)), samples)
    plt.title("Sample distance heatmap")
    savefig(fig_dir / "sample-distance-heatmap.png")

    plt.figure(figsize=(7.0, 4.2))
    x = np.log2(cpm.mean(axis=1) + 1)
    y = np.sqrt(count_mat.var(axis=1))
    plt.scatter(x, y, s=8, alpha=0.25, color="#2f6f9f")
    plt.xlabel("Mean expression log2(CPM + 1)")
    plt.ylabel("Square root variance of raw counts")
    plt.title("Mean-variance trend")
    savefig(fig_dir / "mean-variance-trend.png")

    plt.figure(figsize=(7.2, 4.2))
    xloc = np.arange(len(samples))
    width = 0.35
    plt.bar(xloc - width / 2, lib_sizes / 1e6, width, label="Raw library size", color="#777777")
    plt.bar(xloc + width / 2, eff_lib / 1e6, width, label="Effective library size", color="#2f6f9f")
    plt.xticks(xloc, samples, rotation=35, ha="right")
    plt.ylabel("Million reads")
    plt.title("Raw vs TMM effective library size")
    plt.legend(frameon=False)
    savefig(fig_dir / "tmm-library-size-comparison.png")

    plt.figure(figsize=(7.2, 4.2))
    plt.bar(samples, tmm_factor, color=sample_colors)
    plt.axhline(1, color="#333333", linewidth=1, linestyle="--")
    plt.ylabel("TMM normalization factor (demo)")
    plt.xticks(rotation=35, ha="right")
    plt.title("TMM normalization factors")
    savefig(fig_dir / "tmm-normalization-factor-comparison.png")

    plt.figure(figsize=(7.2, 4.2))
    for sample in samples:
        plt.hist(np.log2(cpm.loc[keep_filter, sample] + 1), bins=45, density=True,
                 histtype="step", linewidth=1.2, alpha=0.65)
    for sample in samples:
        plt.hist(np.log2(tmm_cpm.loc[keep_filter, sample] + 1), bins=45, density=True,
                 histtype="step", linewidth=1.8)
    plt.xlabel("log2(CPM + 1)")
    plt.ylabel("Density")
    plt.title("Expression distribution before and after TMM")
    savefig(fig_dir / "tmm-logcpm-density-comparison.png")

    plt.figure(figsize=(6.4, 4.8))
    sig = (de_table["FDR"] < 0.05) & (np.abs(de_table["logFC"]) >= 1)
    plt.scatter(de_table["logCPM"], de_table["logFC"], s=8, alpha=0.25, color="#777777")
    plt.scatter(de_table.loc[sig, "logCPM"], de_table.loc[sig, "logFC"], s=10, alpha=0.65, color="#c95f3f")
    plt.axhline(0, color="#333333", linewidth=0.8)
    plt.xlabel("Average abundance log2(CPM + 1)")
    plt.ylabel("log2 fold change treated/control")
    plt.title("MA plot")
    savefig(fig_dir / "differential-expression-ma-plot.png")

    plt.figure(figsize=(6.4, 4.8))
    yv = -np.log10(np.maximum(de_table["FDR"], 1e-300))
    plt.scatter(de_table["logFC"], yv, s=8, alpha=0.25, color="#777777")
    plt.scatter(de_table.loc[sig, "logFC"], yv[sig], s=10, alpha=0.7, color="#c95f3f")
    plt.axvline(-1, color="#333333", linewidth=0.8, linestyle="--")
    plt.axvline(1, color="#333333", linewidth=0.8, linestyle="--")
    plt.axhline(-np.log10(0.05), color="#333333", linewidth=0.8, linestyle="--")
    plt.xlabel("log2 fold change treated/control")
    plt.ylabel("-log10(FDR)")
    plt.title("Volcano plot")
    savefig(fig_dir / "differential-expression-volcano.png")

    top = de_table.sort_values("FDR").head(40)["gene_id"]
    mat = np.log2(tmm_cpm.loc[top] + 1)
    mat = mat.sub(mat.mean(axis=1), axis=0).div(mat.std(axis=1).replace(0, 1), axis=0)
    plt.figure(figsize=(6.2, 7.0))
    im = plt.imshow(mat.values, cmap="RdBu_r", aspect="auto", vmin=-2.5, vmax=2.5)
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Row-scaled log-CPM")
    plt.xticks(range(len(samples)), samples, rotation=45, ha="right")
    plt.yticks(range(len(top)), [symbols[genes.index(g)] for g in top], fontsize=5)
    plt.title("Top differential-expression heatmap")
    savefig(fig_dir / "differential-expression-heatmap.png")

    plt.figure(figsize=(6.4, 4.2))
    plt.hist(de_table["logFC"], bins=60, color="#2f6f9f", alpha=0.85)
    plt.axvline(0, color="#333333", linewidth=0.8)
    plt.xlabel("log2 fold change treated/control")
    plt.ylabel("Gene count")
    plt.title("Log2 fold-change distribution")
    savefig(fig_dir / "logfc-distribution.png")

    up = int(((de_table["FDR"] < 0.05) & (de_table["logFC"] >= 1)).sum())
    down = int(((de_table["FDR"] < 0.05) & (de_table["logFC"] <= -1)).sum())
    plt.figure(figsize=(4.8, 4.2))
    plt.bar(["Up", "Down"], [up, down], color=["#c95f3f", "#2f6f9f"])
    plt.ylabel("Significant genes")
    plt.title("Upregulated and downregulated genes")
    savefig(fig_dir / "up-downregulated-gene-count.png")

    example_gene = de_table.sort_values("FDR").iloc[0]["gene_id"]
    expr = np.log2(tmm_cpm.loc[example_gene] + 1)
    plt.figure(figsize=(5.4, 4.2))
    for g in np.unique(group):
        vals = expr[group == g]
        xpos = 1 if g == "control" else 2
        plt.scatter(np.repeat(xpos, len(vals)) + rng.normal(0, 0.025, len(vals)), vals,
                    s=80, color=colors[g], label=g)
        plt.hlines(vals.mean(), xpos - 0.22, xpos + 0.22, colors="#333333", linewidth=2)
    plt.xticks([1, 2], ["control", "treated"])
    plt.ylabel("log2(TMM CPM + 1)")
    plt.title(f"Top gene expression: {example_gene}")
    savefig(fig_dir / "top-gene-expression-plot.png")

    terms = [
        "response to steroid hormone",
        "extracellular matrix organization",
        "immune effector process",
        "cell cycle checkpoint",
        "ribosome biogenesis",
        "cytokine signaling",
        "oxidative phosphorylation",
        "chromatin organization",
    ]
    enrich = pd.DataFrame({
        "term": terms,
        "gene_ratio": [0.18, 0.15, 0.13, 0.11, 0.10, 0.09, 0.08, 0.07],
        "fdr": [0.0008, 0.002, 0.006, 0.012, 0.019, 0.026, 0.034, 0.045],
        "count": [34, 28, 26, 22, 18, 16, 15, 12],
    })
    enrich.to_csv(data_dir / "simulated_enrichment_results.csv", index=False)
    plt.figure(figsize=(7.2, 4.8))
    yy = np.arange(len(enrich))[::-1]
    sc = plt.scatter(enrich["gene_ratio"], yy, s=enrich["count"] * 12,
                     c=-np.log10(enrich["fdr"]), cmap="viridis")
    plt.yticks(yy, enrich["term"])
    plt.xlabel("Gene ratio")
    plt.colorbar(sc, label="-log10(FDR)")
    plt.title("GO enrichment dotplot")
    savefig(fig_dir / "go-enrichment-dotplot.png")

    plt.figure(figsize=(7.2, 4.8))
    plt.barh(yy, -np.log10(enrich["fdr"]), color="#2f6f9f")
    plt.yticks(yy, enrich["term"])
    plt.xlabel("-log10(FDR)")
    plt.title("GO enrichment barplot")
    savefig(fig_dir / "go-enrichment-barplot.png")

    # Lightweight illustrative QC images matching named teaching concepts.
    x = np.arange(1, 101)
    plt.figure(figsize=(7.0, 4.2))
    for sample in samples[:3]:
        q = 36 - 0.035 * x + rng.normal(0, 0.2, len(x))
        plt.plot(x, q, linewidth=1.4, label=sample)
    plt.axhline(20, color="#c95f3f", linestyle="--", linewidth=1)
    plt.xlabel("Base position")
    plt.ylabel("Phred quality")
    plt.ylim(15, 40)
    plt.title("FastQC per-base sequence quality")
    plt.legend(fontsize=7)
    savefig(fig_dir / "fastqc-per-base-sequence-quality.png")

    plt.figure(figsize=(7.0, 4.2))
    adapter = np.maximum(0, (x - 55) / 45 * 18)
    plt.plot(x, adapter, color="#c95f3f", linewidth=2)
    plt.xlabel("Base position")
    plt.ylabel("Adapter content (%)")
    plt.title("Adapter content increasing toward read end")
    savefig(fig_dir / "fastqc-adapter-content.png")

    metrics = pd.Series({
        "Uniquely mapped": 84.2,
        "Multi-mapped": 8.7,
        "Too short": 3.1,
        "Unmapped": 4.0,
    })
    plt.figure(figsize=(6.2, 4.2))
    plt.bar(metrics.index, metrics.values, color=["#2f6f9f", "#6f8f3f", "#c9a33f", "#c95f3f"])
    plt.ylabel("Reads (%)")
    plt.xticks(rotation=25, ha="right")
    plt.title("STAR mapping summary")
    savefig(fig_dir / "star-mapping-summary.png")

    assign = pd.Series({
        "Assigned": 72.5,
        "Unassigned_NoFeatures": 11.2,
        "Unassigned_Ambiguity": 5.8,
        "Unassigned_MultiMapping": 6.7,
        "Other": 3.8,
    })
    plt.figure(figsize=(7.0, 4.2))
    plt.bar(assign.index, assign.values, color="#2f6f9f")
    plt.ylabel("Fragments (%)")
    plt.xticks(rotation=25, ha="right")
    plt.title("featureCounts assignment summary")
    savefig(fig_dir / "featurecounts-assignment-summary.png")


if __name__ == "__main__":
    main()
