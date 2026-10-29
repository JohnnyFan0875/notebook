[基因體學](../README.md) › [全基因體分析](README.md) › Colocalization

# 共定位分析 (Colocalization)

判斷同一個位點上的兩個關聯訊號（例如 GWAS 與 eQTL）是否**由同一個致病變異**驅動。兩個訊號在同一區域出現不代表共享：可能是兩個不同的變異剛好鄰近並處於 LD。

## coloc 的五個假說

| 假說 | 意義 |
| --- | --- |
| H0 | 兩個性狀在此區域都沒有關聯 |
| H1 | 只有性狀 1 有關聯 |
| H2 | 只有性狀 2 有關聯 |
| H3 | 兩者都有關聯，但是**不同**的致病變異 |
| H4 | 兩者都有關聯，且是**同一個**致病變異 |

輸出每個假說的後驗機率；常以 **PP.H4 > 0.8** 視為支持共定位。PP.H3 高代表訊號接近但機制不同。

```r
library(coloc)
res <- coloc.abf(
  dataset1 = list(beta = gwas$beta, varbeta = gwas$se^2, snp = gwas$snp, type = "cc", s = 0.3, N = 50000),
  dataset2 = list(beta = eqtl$beta, varbeta = eqtl$se^2, snp = eqtl$snp, type = "quant", N = 500, sdY = 1))
res$summary          # nsnps、PP.H0.abf … PP.H4.abf（coloc 5.2 實跑；模擬共享變異時 PP.H4 ≈ 1）
```

## 方法

| 方法 | 特點 |
| --- | --- |
| coloc（ABF） | 經典方法；**假設每個性狀在區域內只有一個致病變異** |
| coloc + SuSiE | 先用 SuSiE 拆出多個獨立訊號，再兩兩做 coloc；處理多個致病變異 |
| eCAVIAR | 以 fine-mapping 後驗機率計算共同致病機率 (CLPP) |
| SMR / HEIDI | 以孟德爾隨機化框架檢定，HEIDI 檢定排除連鎖 |

## 常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 兩邊的 LD 不同 | GWAS 與 eQTL 來自不同族群時，LD 型態不同會影響結果 |
| SNP 不一致 | 兩份摘要統計的 SNP 集合、等位基因方向、基因組版本要對齊 |
| 先驗設定 | p1、p2、p12 先驗會影響後驗機率；預設 p12 = 1e-5 |
| 組織選擇 | 用與疾病相關的組織的 eQTL；不同組織可能給出不同目標基因 |
| 共定位 ≠ 因果 | 支持兩者共享變異，但方向與機制仍需實驗驗證 |

用途：GWAS 位點的目標基因排序、區分「真正共享」與「只是鄰近」的訊號。前置步驟見 [GWAS 基礎](gwas-fundamental.md#從位點到基因)、[eQTL](eqtl.md)。
