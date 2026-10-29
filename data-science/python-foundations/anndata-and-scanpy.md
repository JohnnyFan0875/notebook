[Data Science](../README.md) › [Python Foundations](README.md) › AnnData 與 scanpy

# AnnData 與 scanpy (AnnData & scanpy)

AnnData 是 Python 單細胞分析的標準資料結構：把**稀疏計數矩陣**和**細胞 / 基因的 metadata、降維結果、鄰接圖**綁在同一個物件，存成 `.h5ad`。scanpy、scvi-tools、squidpy、cellxgene 都以它為輸入輸出。R 的對應是 Seurat 物件與 `SingleCellExperiment`。

## 物件結構

```
                 var（基因 metadata：DataFrame，index = var_names）
                 ┌─────────────────────────┐
 obs（細胞        │  X：細胞 × 基因          │  varm（基因 × k：PCA loadings）
 metadata，       │  （通常是 CSR 稀疏矩陣） │  varp（基因 × 基因）
 index =          │  layers["counts"] 等    │
 obs_names）      └─────────────────────────┘
 obsm（細胞 × k：X_pca、X_umap、X_scVI）   obsp（細胞 × 細胞：kNN distances / connectivities）
 uns（非結構化：參數、顏色、rank_genes_groups 結果）
```

| 欄位 | 內容 | 例子 |
| --- | --- | --- |
| `X` | 主矩陣（`n_obs × n_vars`） | 標準化 + log 後的表現量 |
| `layers` | 與 `X` 同形狀的其他版本 | `layers["counts"]` 原始整數計數 |
| `obs` / `var` | 細胞 / 基因的 DataFrame | `sample`、`batch`、`pct_counts_mt`；`gene_ids`、`highly_variable` |
| `obsm` / `varm` | 多維嵌入 | `X_pca`、`X_umap`；`PCs` |
| `obsp` | 細胞間成對矩陣 | `connectivities`（Leiden / UMAP 用） |
| `uns` | 字典 | `uns["leiden"]`、`uns["log1p"]`、繪圖顏色 |
| `raw` | 凍結的舊版矩陣 + var | 舊流程用來保留全部基因；新流程改用 `layers` |

> 慣例：**細胞是列、基因是欄**，與 Bioconductor 的 `SummarizedExperiment`（基因 × 樣本）相反，在 R ↔ Python 轉換時要轉置（`zellkonverter` 會處理）。

## 建立、讀寫、子集

```python
import anndata as ad
import scanpy as sc

# 1. 讀取
adata = sc.read_10x_h5("filtered_feature_bc_matrix.h5")   # Cell Ranger 輸出
adata = sc.read_10x_mtx("filtered_feature_bc_matrix/")    # matrix.mtx + barcodes + features
adata = ad.read_h5ad("pbmc.h5ad")
adata = ad.read_h5ad("atlas.h5ad", backed="r")            # 不全部載入，X 留在磁碟
adata.var_names_make_unique()                              # 基因 symbol 可能重複

# 2. 自己組：X 用稀疏矩陣，obs / var 的 index 要和列 / 欄對齊
adata = ad.AnnData(X=counts_csr, obs=cell_meta, var=gene_meta)

# 3. 子集：與 pandas 相同語法，但結果是 view
sub = adata[adata.obs["sample"] == "s1", adata.var["highly_variable"]]
sub.is_view                                                # True
sub = sub.copy()                                           # 要修改前先 copy

# 4. 取值成 DataFrame（自動 densify，只取少數基因）
sc.get.obs_df(adata, keys=["CD3E", "leiden", "total_counts"])

# 5. 合併多個樣本
adata = ad.concat({"s1": a1, "s2": a2}, label="sample", index_unique="-")   # barcode 加後綴避免重複

# 6. 存檔
adata.write_h5ad("pbmc_processed.h5ad", compression="gzip")
```

| 陷阱 | 說明 |
| --- | --- |
| 在 view 上修改 | 會觸發隱式 copy 並警告（`ImplicitModificationWarning`）；明確 `.copy()` |
| 不同樣本 barcode 重複 | `concat` 不加 `index_unique` 會得到重複的 `obs_names` |
| `X` 被覆寫後找不回原始計數 | 標準化前先 `adata.layers["counts"] = adata.X.copy()` |
| 對 `X` 做 `scale` | 稀疏矩陣被中心化 → 變 dense（見 [scipy.sparse 陷阱](scipy-sparse.md#常見陷阱)） |
| `backed="r"` 後做大量運算 | 每次都讀磁碟；只適合切子集後 `.to_memory()` |

`.h5ad` 是 HDF5 為底，也能用 `h5py` 直接看結構；更新的 `.zarr` 格式適合雲端與平行讀寫（`ad.read_zarr`）。檔案格式比較見 [Storage and Models](../data-engineering/storage-and-models.md)。

## scanpy 標準流程

scanpy 的函式分三個命名空間：`sc.pp`（前處理）、`sc.tl`（工具 / 分析）、`sc.pl`（作圖）；結果寫回 `adata` 的對應欄位。

```
QC 過濾 → 保存 counts → 標準化 + log1p → HVG → PCA → kNN 圖 → UMAP / Leiden → marker 基因
```

```python
# 1. QC 指標：每個細胞的基因數、總計數、粒線體比例
adata.var["mt"] = adata.var_names.str.startswith("MT-")   # 小鼠是 "mt-"
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)
# → obs: n_genes_by_counts, total_counts, pct_counts_mt；var: n_cells_by_counts...
sc.pl.violin(adata, ["n_genes_by_counts", "total_counts", "pct_counts_mt"], groupby="sample")

adata = adata[(adata.obs.n_genes_by_counts > 200) & (adata.obs.pct_counts_mt < 15)].copy()
sc.pp.filter_genes(adata, min_cells=3)
sc.pp.scrublet(adata, batch_key="sample")                  # doublet 分數（需 scikit-image）

# 2. 標準化
adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)               # 每個細胞縮放到相同總數
sc.pp.log1p(adata)

# 3. 高變異基因：seurat_v3 用原始計數（需 pip install scikit-misc）
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor="seurat_v3",
                            layer="counts", batch_key="sample")

# 4. 降維、鄰接圖、分群、視覺化
sc.tl.pca(adata, n_comps=50, mask_var="highly_variable")   # 結果在 obsm["X_pca"]
sc.pl.pca_variance_ratio(adata, log=True)                   # 選 n_pcs
sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)            # obsp["connectivities"]
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=1.0, flavor="igraph", n_iterations=2, directed=False)
sc.pl.umap(adata, color=["leiden", "sample", "CD3E"])

# 5. marker 基因
sc.tl.rank_genes_groups(adata, groupby="leiden", method="wilcoxon")
sc.get.rank_genes_groups_df(adata, group="0").head()       # names, scores, logfoldchanges, pvals, pvals_adj
sc.pl.dotplot(adata, ["CD3E", "MS4A1", "LYZ"], groupby="leiden")
```

| 步驟 | 關鍵參數 | 判斷依據 |
| --- | --- | --- |
| QC 閾值 | `n_genes`、`pct_counts_mt` | 看分布找斷點，依組織調整（心肌、肝細胞粒線體比例天生高）；各樣本分開看 |
| HVG | `n_top_genes`、`batch_key` | 有批次時加 `batch_key`，避免選到批次差異基因 |
| PCA | `n_comps` / `n_pcs` | elbow；結果對 20–50 通常不敏感 |
| kNN | `n_neighbors` | 小 → 細分小群；大 → 平滑、全域結構 |
| Leiden | `resolution` | 越大群越多；用 marker 是否有生物意義判斷，不是追求某個群數 |

kNN 圖與 Leiden 的原理見 [單細胞 kNN 圖 + Leiden](../network-analysis/network-analysis-case-studies.md#單細胞-knn-圖--leiden)；批次整合與 scVI 見 [單細胞深度學習](../deep-learning/bio-applications/single-cell-deep-learning.md)。

## 統計上要注意的事

| 問題 | 為什麼 | 做法 |
| --- | --- | --- |
| 用細胞當樣本比較條件（處理 vs 對照） | 同一個體的細胞不獨立 → [假重複](../statistics/experimental-design/core-concepts.md#實驗單位-vs-觀測單位)，p 值極小但不可信 | **pseudobulk**：每個樣本 × 細胞類型加總計數，再用 DESeq2 / edgeR（[NB-GLM](../statistics/regression-analysis/glm-count-models.md)）；或用 [混合效應模型](../statistics/regression-analysis/mixed-effects-models.md) |
| marker 基因的 p 值 | 分群與檢定用同一份資料（double dipping），p 值偏小 | 只用來排序 marker，不當作「差異顯著」的證據 |
| UMAP 距離 | 群間距離與群大小不具定量意義 | 定量分析用 PCA / 潛在空間；UMAP 只用來看 |
| 對 log 標準化資料做檢定 | 不同 library size 的細胞變異不同 | 差異表現用原始計數的計數模型 |
| 多重檢定 | 每群數千個基因 | 看 `pvals_adj`（BH），見 [多重檢定](../statistics/inferential-statistics/multiple-testing.md) |

```python
# pseudobulk：每個 sample × cell type 加總原始計數（需 scanpy ≥ 1.10）
pb = sc.get.aggregate(adata, by=["sample", "cell_type"], func="sum", layer="counts")
pb.X = pb.layers["sum"]                     # 樣本 × 基因的計數矩陣 → pydeseq2 / R DESeq2
```

## R 對照

| Python（scanpy） | R（Seurat） | R（Bioconductor） |
| --- | --- | --- |
| `AnnData` | `Seurat` 物件 | `SingleCellExperiment` |
| `sc.pp.normalize_total` + `log1p` | `NormalizeData()` | `scuttle::logNormCounts()` |
| `highly_variable_genes` | `FindVariableFeatures()` | `scran::modelGeneVar()` |
| `sc.tl.pca` / `neighbors` / `leiden` | `RunPCA` / `FindNeighbors` / `FindClusters` | `scater::runPCA`、`bluster` |
| `rank_genes_groups` | `FindAllMarkers()` | `scran::findMarkers()` |
| `.h5ad` ↔ R | `SeuratDisk`、`zellkonverter::readH5AD()` | `zellkonverter` |

相關：[scipy.sparse](scipy-sparse.md)、[匯入資料](importing-data.md)、[PCA](../statistics/multivariate-analysis/pca.md)、[分群](../statistics/multivariate-analysis/clustering.md)、[單細胞 RNA-seq（biology）](../../biology/genomics/sequencing-techniques/single-cell-rna-seq/README.md)、[RNA-seq 差異表現](../../biology/genomics/workflows/rna-seq/07-differential-expression.md)。
