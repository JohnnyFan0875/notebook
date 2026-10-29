[分子生物學](../README.md) › [實驗方法](README.md) › 凝膠電泳

# 凝膠電泳 (Gel Electrophoresis)

在電場中讓帶電分子通過凝膠網孔，依大小（與電荷、構形）分離。核酸骨架帶均勻負電，所以移動速度主要由長度決定；蛋白質則需 SDS 包覆後才主要依分子量分離。它是 blot、PCR 產物確認、NGS library QC 的共同基礎。

## 種類

| 種類 | 分離對象 | 解析範圍 | 典型用途 |
| --- | --- | --- | --- |
| 洋菜膠 (agarose) | DNA / RNA | 約 100 bp – 25 kb（濃度越高越適合小片段） | PCR 產物、酶切結果、RNA 完整性 |
| 聚丙烯醯胺 (PAGE)，變性 | 單股核酸 | 可分辨 1 nt 差異 | 寡核苷酸純化、小 RNA |
| SDS-PAGE | 變性蛋白 | 約 10–250 kDa | Western blot、蛋白純度 |
| Native PAGE | 未變性蛋白 / 複合體 | 依形狀與電荷 | 蛋白複合體、EMSA（蛋白–DNA 結合） |
| 脈衝電場 (PFGE) | 大 DNA | 數十 kb – Mb | 細菌分型、BAC / YAC |
| 毛細管電泳 (CE) | DNA | 單鹼基解析 | Sanger 定序、片段分析（STR、重複擴增） |

## 判讀

| 現象 | 可能原因 |
| --- | --- |
| 預期大小的單一條帶 | 專一性擴增 / 正確產物 |
| 多條帶 | 非專一擴增、剪接變體、降解 |
| 拖尾 (smear) | 降解、上樣過多、基因體 DNA 汙染 |
| 極小的條帶（< 100 bp） | primer dimer |
| RNA 看到 28S : 18S ≈ 2 : 1 | RNA 完整；降解時比例下降、出現低分子拖尾 |

大小估計靠同膠的 DNA ladder / 蛋白 marker；超螺旋質體的跑速與線性 DNA 不同，不能直接讀大小。

> NGS 實驗室多用自動化毛細管電泳（Agilent Bioanalyzer / TapeStation、Fragment Analyzer）取代手動跑膠：輸出 RNA 的 RIN / DV200 與 library 片段大小分布，是[RNA-seq](../../genomics/workflows/rna-seq/01-rnaseq-overview.md) 與 [定序前 QC](../../genomics/ngs-qc/README.md) 的常見指標。
