[Deep Learning](../README.md) › [生資應用](README.md) › 單細胞深度學習

# 單細胞深度學習 (Deep Learning for Single-Cell Data)

單細胞 RNA-seq 是稀疏的計數矩陣（細胞 × 基因，九成以上為 0），常有數十萬個細胞、多個批次。深度學習在這裡最成熟的用途是**機率式的潛在表示**：用 [VAE](../representation-learning/autoencoders-and-vae.md) 直接對原始計數建模，同時校正批次效應，代表工具是 scvi-tools。

上游流程（QC、標準化、分群、軌跡）見 [單細胞 RNA-seq](../../../biology/genomics/sequencing-and-analysis/sequencing-techniques/single-cell-rna-seq/README.md)。

## 何時需要 DL

| 情境 | 傳統做法 | DL 做法 | 建議 |
| --- | --- | --- | --- |
| 單一批次降維、分群 | log 標準化 → PCA → 鄰接圖 | scVI | PCA 已足夠 |
| 多批次 / 多實驗室整合 | Harmony、Seurat CCA / RPCA | **scVI** | 大型、複雜批次時 scVI 常表現最好；Harmony 快且是強 baseline |
| 用部分已標註細胞做細胞類型標註 | 參考圖譜 + 分類器（CellTypist） | **scANVI** | 有可靠的參考標註時 |
| 把新資料映射到參考圖譜 | — | scArches（固定參考模型，只訓練新批次參數） | 參考圖譜以 scVI / scANVI 建立時 |
| CITE-seq（RNA + 表面蛋白） | WNN | totalVI | 多模態 |
| 差異表現 | pseudobulk + DESeq2 / edgeR | scVI 的 `differential_expression` | 跨樣本推論仍以 **pseudobulk** 為主（考慮生物重複） |

## scVI 在做什麼

```
原始計數 x（不要先 log 標準化）+ 批次 s
        │
   encoder（神經網路）→ q(z | x, s)：細胞的潛在表示 z（約 10～30 維）
        │
   decoder（神經網路）：(z, s, library size) → 每個基因的負二項 (NB) 或 ZINB 分布參數
        │
   loss = −log p(x | z, s) + KL(q(z|x,s) ‖ N(0, I))
```

| 設計 | 對應的資料特性 |
| --- | --- |
| 負二項似然 | 計數資料過度離散 (overdispersion)，與 DESeq2 的 [NB-GLM](../../statistics/regression-analysis/glm-count-models.md) 同一假設 |
| library size 當作已知因子 | 定序深度差異不必靠事先標準化消除 |
| 批次 s 餵給 decoder | $z$ 不必編碼批次差異 → 整合後的表示 |
| 機率模型 | 可輸出去噪表現量、不確定性，並做差異表現 |

## 使用方式

AnnData 結構與 scanpy 前處理見 [AnnData 與 scanpy](../../python-foundations/anndata-and-scanpy.md)。

```python
import scanpy as sc
import scvi

adata = sc.read_h5ad("pbmc.h5ad")
adata.layers["counts"] = adata.X.copy()             # scVI 要原始整數計數
sc.pp.normalize_total(adata); sc.pp.log1p(adata)    # 這些只給視覺化 / 選基因用
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor="seurat_v3",
                            layer="counts", batch_key="batch", subset=True)

# 1. 訓練
scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="batch")
model = scvi.model.SCVI(adata, n_latent=30, gene_likelihood="nb")
model.train(max_epochs=400, early_stopping=True)    # 預設會切出 validation 做 early stopping

# 2. 潛在表示 → 鄰接圖、UMAP、分群（取代 PCA）
adata.obsm["X_scVI"] = model.get_latent_representation()
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata); sc.tl.leiden(adata)

# 3. 去噪、批次校正後的表現量（視覺化用，不要再拿去做統計檢定）
adata.layers["scvi_norm"] = model.get_normalized_expression(library_size=1e4)

# 4. 用部分標籤訓練 scANVI 做細胞類型標註（未知細胞標為 "Unknown"）
lvae = scvi.model.SCANVI.from_scvi_model(model, unlabeled_category="Unknown", labels_key="cell_type")
lvae.train(max_epochs=20)
adata.obs["pred_type"] = lvae.predict()

model.save("scvi_model/")                            # 之後 SCVI.load("scvi_model/", adata=adata)
```

## 怎麼判斷整合得好不好

| 面向 | 指標 / 檢查 | 目標 |
| --- | --- | --- |
| 批次混合 | iLISI、kBET、批次 ASW | 同一細胞類型內，不同批次的細胞互相混合 |
| 生物保留 | cLISI、細胞類型 ASW、NMI / ARI | 不同細胞類型仍分得開 |
| 稀有族群 | 已知稀有細胞型是否仍是獨立群 | 沒有被併入大族群 |
| 工具 | `scib-metrics` 套件可一次算出並與 Harmony 等方法比較 | — |

> 只看 UMAP「混得很均勻」不夠：過度校正會把真實的生物差異（疾病 vs 對照）也當成批次抹掉。批次與生物條件完全混雜時（每個條件只在一個批次），任何方法都無法分開兩者——這是 [實驗設計](../../statistics/experimental-design/confounding-bias.md) 問題。

## 單細胞基礎模型

scGPT、Geneformer、scFoundation 等以數千萬個細胞預訓練的 Transformer，宣稱可用於細胞類型標註、擾動預測、基因網路推論。

| 已知情況 | 說明 |
| --- | --- |
| 零樣本 embedding | 多項獨立評估中，零樣本的細胞 embedding 在批次整合、分群上常**不優於** HVG + PCA 或 scVI |
| Fine-tune 後 | 細胞類型標註表現不錯，但相較簡單分類器（logistic 迴歸、CellTypist）的優勢通常有限 |
| 擾動預測 | 是否勝過「平均擾動效應」等簡單 baseline 仍有爭議 |
| 成本 | 需要 GPU、前處理要符合模型的基因詞彙與排序方式 |

> 使用前先和 PCA / scVI / 簡單分類器在同一資料、同一切分下比較；切分以**捐贈者 / 樣本**為單位，避免同一人的細胞同時出現在訓練與測試。

## 常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 把 log 標準化後的資料餵給 scVI | 模型假設計數分布；要用 `layer="counts"` |
| 拿 scVI 去噪後的表現量做差異檢定 | 值彼此不獨立、變異被平滑掉，p 值會過度樂觀 |
| 把每個細胞當獨立樣本做跨條件比較 | 假重複 (pseudoreplication)；以樣本為單位做 pseudobulk |
| 批次定義錯 | `batch_key` 應是技術批次（實驗、晶片、定序批），不是要研究的生物條件 |
| 不同 seed 的 UMAP 長得不同 | 正常；比較的是群集與鄰近關係，不是座標 |
