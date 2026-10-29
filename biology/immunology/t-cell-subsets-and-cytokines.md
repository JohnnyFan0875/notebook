[Biology](../README.md) › [免疫學](README.md) › T 細胞亞群

# T 細胞亞群 (T Cell Subsets)

T 細胞依 TCR 類型、共受體（CD4 / CD8）與分化環境分成功能不同的亞群。亞群之間由細胞激素互相誘導與抑制，平衡偏向哪一邊決定了感染能否清除、是否出現過敏或自體免疫。細胞激素本身的家族、交互抑制與治療標的見 [細胞激素網路](cytokines.md)。

## 免疫細胞的大分類

| 類別 | 代表細胞 | 功能 |
| --- | --- | --- |
| 先天免疫 (innate) | 巨噬細胞、樹突細胞 (DC)、嗜中性球、NK 細胞、肥大細胞 | 快速、非專一：吞噬、發炎、早期抗病毒 |
| 後天免疫 (adaptive) | T 細胞（CD4⁺ 輔助、CD8⁺ 毒殺）、B 細胞（→ 漿細胞） | 抗原專一、抗體生成、免疫記憶 |
| 調節 / 輔助 | 調節性 T (Treg)、濾泡輔助 T (Tfh)、抗原呈現 DC | 維持耐受、協助 B 細胞成熟 |
| 介於兩者之間 | γδ T、NKT、MAIT、先天淋巴細胞 (ILC) | 有 T 細胞樣受體或細胞激素譜，但反應快、受體多樣性低 |

## T 細胞活化：三個訊號

| 訊號 | 分子 | 缺少時 |
| --- | --- | --- |
| 1. 抗原辨識 | TCR 辨識 MHC 上的胜肽（CD4 ↔ MHC II、CD8 ↔ MHC I） | 無反應 |
| 2. 共刺激 (co-stimulation) | CD28 ↔ B7（CD80 / CD86）；被 CTLA-4 競爭抑制 | 失能 (anergy) |
| 3. 細胞激素 | IL-12、IL-4、IL-6 + TGF-β… | 決定往哪個亞群分化（下表） |

> CTLA-4（搶走 B7，削弱訊號 2）與 PD-1（抑制 TCR / CD28 下游訊號）是兩個主要的負向檢查點，臨床阻斷藥物見 [免疫標記：免疫檢查點](immune-marker.md#免疫檢查點-immune-checkpoints)。

## CD4⁺ 輔助 T 亞群

| 亞群 | 誘導因子 | 主要分泌 | 功能 | 轉錄因子 | 相關疾病 |
| --- | --- | --- | --- | --- | --- |
| TH1 | IL-12、IFN-γ | IFN-γ、IL-2、TNF-α | 活化巨噬細胞與 CTL；抗病毒、胞內細菌 | T-bet、STAT4 | 結核防禦；MS、T1DM |
| TH2 | IL-4 | IL-4、IL-5、IL-13 | 體液免疫、抗寄生蟲、促 IgE | GATA3、STAT6 | 氣喘、異位性皮膚炎、蠕蟲感染 |
| TH17 | IL-6 + TGF-β、IL-23（維持） | IL-17A、IL-17F、IL-22 | 招募嗜中性球；抗黴菌、胞外細菌 | RORγt、STAT3 | 乾癬、RA、IBD |
| Treg | TGF-β、IL-2 | IL-10、TGF-β | 抑制免疫活化、維持耐受 | FOXP3、STAT5 | 缺陷 → 自體免疫（IPEX）；腫瘤內過多 → 免疫逃脫 |
| Tfh | IL-6、IL-21 | IL-21、IL-4 | 協助 B 細胞分化與親和力成熟（CD40L） | BCL6、STAT3 | SLE、慢性病毒感染 |
| TH9 | IL-4 + TGF-β | IL-9 | 強化嗜酸性球、肥大細胞反應 | PU.1、IRF4 | 過敏性氣喘、寄生蟲免疫 |
| TH22 | IL-6、TNF-α | IL-22 | 上皮修復、黏膜防禦 | AHR | 乾癬、皮膚炎 |

> 亞群不是固定終點：TH17 在 IL-12 / IL-23 下可轉成分泌 IFN-γ 的 "TH17.1"，Treg 在發炎環境可失去 FOXP3。單細胞資料常看到介於兩群之間的連續狀態，註解時以 marker 組合而非單一基因判斷。

## CD8⁺ T 細胞：分化與耗竭

| 狀態 | 表面標記 | 特性 |
| --- | --- | --- |
| 初始 (naive) | CCR7⁺ CD45RA⁺ CD62L⁺ | 在淋巴結巡邏，尚未遇過抗原 |
| 中央記憶 (T<sub>CM</sub>) | CCR7⁺ CD45RA⁻ | 留在淋巴組織，再次遇抗原時大量增生 |
| 效應記憶 (T<sub>EM</sub>) | CCR7⁻ CD45RA⁻ | 在周邊組織巡邏，快速分泌細胞激素 |
| T<sub>EMRA</sub> | CCR7⁻ CD45RA⁺ | 終末分化、毒殺力強、增生力低 |
| 組織駐留記憶 (T<sub>RM</sub>) | CD69⁺ CD103⁺ | 不回到血液，局部第一線防禦（PBMC 中幾乎沒有） |
| 耗竭 (exhausted, T<sub>EX</sub>) | PD-1、TIM-3、LAG-3、TIGIT 高；TOX⁺ | 慢性抗原刺激（慢性感染、腫瘤）後功能遞減；前驅耗竭 (TCF1⁺) 是檢查點抑制劑主要作用對象 |

CD8⁺ 毒殺 T 細胞 (CTL) 以 perforin、granzyme 與 Fas–FasL 殺死感染或腫瘤細胞；在腫瘤中的角色見 [腫瘤浸潤淋巴球](tumor-infiltrating-lymphocytes.md)。

## 亞群判讀的對應

| 想知道 | 流式 / CITE-seq 標記 | scRNA-seq 常用 marker 基因 |
| --- | --- | --- |
| CD4 vs CD8 | CD4、CD8 | *CD4*（RNA 偵測率低）、*CD8A*、*CD8B* |
| Treg | CD4⁺ CD25<sup>hi</sup> CD127<sup>lo</sup> FOXP3⁺ | *FOXP3*、*IL2RA*、*CTLA4* |
| 初始 vs 記憶 | CCR7、CD45RA / CD45RO | *CCR7*、*SELL*、*TCF7* vs *GZMK*、*GZMB* |
| 耗竭 | PD-1、TIM-3 | *PDCD1*、*HAVCR2*、*LAG3*、*TOX* |

> CD45RA / CD45RO 是同一基因 *PTPRC* 的不同剪接型，scRNA-seq 用 3′ 計數分不出來，需要靠表面蛋白（CITE-seq）或其他 marker 組合。

相關：[B 細胞亞群](b-cell-subsets-and-cytokines.md)、[免疫標記](immune-marker.md)、[單細胞 RNA-seq](../genomics/sequencing-techniques/single-cell-rna-seq/README.md)。
