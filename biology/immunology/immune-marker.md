[Biology](../README.md) › [免疫學](README.md) › 免疫標記

# 免疫標記 (Immune Markers)

免疫標記是可量測、能反映免疫系統狀態的分子或細胞特徵，用來辨認細胞類型、評估活化程度、追蹤疾病進展與治療反應。同一個標記用不同方法量（流式、IHC、RNA）會得到不同意義的數字，判讀時要先確認量測方式。

## 標記類別

| 類別 | 量的是什麼 | 例 |
| --- | --- | --- |
| 細胞表面標記 (CD) | 細胞類型與分化狀態 | CD3、CD4、CD8、CD19、CD56 |
| 細胞激素 / 趨化激素 | 細胞間的訊號 | IL-2、IL-6、IL-10、TNF-α、IFN-γ、CXCL8（IL-8） |
| 功能 / 活化標記 | 活化、增生、毒殺 | CD69、CD25、Ki-67、granzyme B、perforin、CD107a |
| 免疫檢查點 | 抑制性受體與配體 | PD-1、PD-L1、CTLA-4、LAG-3、TIM-3 |
| 抗體與血清蛋白 | 體液免疫與發炎 | IgG / IgA / IgM、補體 C3 / C4、CRP |

## 細胞類型的 CD 標記

分化群 (cluster of differentiation, CD) 編號是國際統一的表面分子命名，流式細胞術 (flow cytometry) 以多個 CD 組合定義細胞族群（gating）。

| 細胞 | 定義標記 | 補充 |
| --- | --- | --- |
| T 細胞 | CD3⁺ | CD4⁺ 輔助 T、CD8⁺ 毒殺 T；亞群見 [T 細胞亞群](t-cell-subsets-and-cytokines.md) |
| Treg | CD4⁺ CD25<sup>hi</sup> CD127<sup>lo</sup> FOXP3⁺ | FOXP3 是核內蛋白，需要固定破膜才能染 |
| B 細胞 | CD19⁺ / CD20⁺ | 漿細胞 CD20⁻ CD138⁺；亞群見 [B 細胞亞群](b-cell-subsets-and-cytokines.md) |
| NK 細胞 | CD3⁻ CD56⁺ | CD56<sup>bright</sup>（分泌細胞激素）vs CD56<sup>dim</sup> CD16⁺（毒殺） |
| 單核球 | CD14⁺ | 典型 CD14<sup>++</sup> CD16⁻、非典型 CD14<sup>+</sup> CD16<sup>++</sup> |
| 樹突細胞 | HLA-DR⁺、lineage⁻ | cDC1（CD141）、cDC2（CD1c）、pDC（CD123、CD303） |
| 白血球（全部） | CD45⁺ | 組織樣本中用來區分免疫細胞與腫瘤 / 基質細胞 |

## 功能與活化標記

| 標記 | 意義 | 時間 |
| --- | --- | --- |
| CD69 | 早期活化；也是組織駐留標記 | 數小時 |
| CD25（IL-2Rα） | 活化 T 細胞；Treg 持續高表現 | 1–2 天 |
| HLA-DR（T 細胞上） | 晚期活化 | 數天 |
| Ki-67 | 增生（細胞週期中的核蛋白） | 非 G0 期皆表現 |
| Granzyme B、perforin | 毒殺能力（胞內） | — |
| CD107a（LAMP-1） | 脫顆粒，表示剛釋放毒殺顆粒 | 刺激後數小時 |

> CD25 同時是活化標記與 Treg 標記，只看 CD25 無法區分；要加 CD127 與 FOXP3。

## 免疫檢查點 (Immune Checkpoints)

| 分子 | 表現位置 | 作用 | 臨床 |
| --- | --- | --- | --- |
| PD-1（CD279） | 活化 / 耗竭 T 細胞 | 與 PD-L1 / PD-L2 結合後抑制 T 細胞 | anti-PD-1：pembrolizumab、nivolumab |
| PD-L1（CD274） | 腫瘤細胞、APC；受 IFN-γ 誘導 | 抑制腫瘤內 T 細胞 | anti-PD-L1：atezolizumab、durvalumab；IHC 是伴隨診斷 |
| CTLA-4（CD152） | 活化 T、Treg | 與 CD28 競爭 B7，在淋巴結抑制初始活化 | anti-CTLA-4：ipilimumab |
| LAG-3（CD223） | 耗竭 T、Treg | 結合 MHC II，抑制 T 細胞 | anti-LAG-3：relatlimab（與 nivolumab 合併） |
| TIM-3、TIGIT | 耗竭 T、NK | 抑制性受體 | 臨床試驗中 |

PD-L1 IHC 的計分方式依抗體與癌別而異：

| 分數 | 定義 | 例 |
| --- | --- | --- |
| TPS（tumor proportion score） | PD-L1⁺ 腫瘤細胞 / 存活腫瘤細胞 × 100% | 非小細胞肺癌（22C3） |
| CPS（combined positive score） | (PD-L1⁺ 腫瘤細胞 + 淋巴球 + 巨噬細胞) / 存活腫瘤細胞 × 100，上限 100 | 胃癌、頭頸癌、子宮頸癌 |
| IC | PD-L1⁺ 免疫細胞佔腫瘤面積比例 | SP142 部分適應症 |

> 不同抗體株（22C3、28-8、SP263、SP142）與不同計分方式的閾值**不能互換**；哪個檢測對應哪個藥，以 [FDA 伴隨診斷清單](../clinical-informatics-and-standards/regulatory-databases/fda-drug-database.md#伴隨診斷清單) 為準。PD-L1 陰性的病人仍可能有反應，它是不完美的預測標記；TMB、MSI-H / dMMR 是另外兩個常用的免疫治療生物標記。

## 血清標記

| 標記 | 用途 | 注意 |
| --- | --- | --- |
| IgG / IgA / IgM | 體液免疫狀態、免疫缺陷篩檢 | IgM 先上升（急性），IgG 後上升（恢復期、記憶） |
| 補體 C3、C4 | 補體消耗（SLE 活動期下降） | — |
| CRP | 急性期發炎 | 非特異；細菌感染通常比病毒高 |
| IL-6、ferritin | 細胞激素釋放症候群 (CRS)、重症發炎 | 檢體採集與處理時間影響細胞激素濃度，見 [血清 vs 血漿](../laboratory-medicine/sample-types/serum-plasma.md) |

## 量測方法

| 方法 | 量什麼 | 解析度 | 特點 |
| --- | --- | --- | --- |
| 流式細胞術 | 細胞表面 / 胞內蛋白 | 單細胞 | 一次 10–40 色；臨床 CD4 計數、白血病分型 |
| 質譜流式 (CyTOF) | 同上，用金屬標記 | 單細胞 | 40 個以上標記、干擾少；細胞會被破壞 |
| [ELISA](../molecular-biology/experimental-methods/elisa.md) / 多重 bead assay | 可溶性蛋白濃度 | 樣本平均 | 細胞激素定量 |
| ELISPOT | 分泌特定細胞激素的細胞數 | 單細胞計數 | 抗原專一 T 細胞（如 IFN-γ release assay） |
| IHC / 多重螢光 IHC | 組織中的蛋白 | 保留空間位置 | 病理判讀、TIL 與 PD-L1 |
| scRNA-seq / CITE-seq | 轉錄體（+ 表面蛋白） | 單細胞 | 不需預選 marker；RNA 與蛋白不一定一致 |

## 臨床應用

| 應用 | 標記 |
| --- | --- |
| HIV 監測 | CD4⁺ T 細胞計數 |
| 淋巴瘤 / 白血病分型 | 異常的 CD 表現組合（如 CLL：CD5⁺ CD19⁺ CD23⁺） |
| 免疫治療選擇 | PD-L1 IHC、TMB、MSI |
| CAR-T 療效與毒性 | CAR-T 擴增（流式 / qPCR）、IL-6、ferritin |
| 疫苗研究 | 抗體力價、ELISPOT、抗原專一 T 細胞 |

相關：[PBMC](pbmc.md)、[腫瘤浸潤淋巴球](tumor-infiltrating-lymphocytes.md)、[細胞激素網路](cytokines.md)。
