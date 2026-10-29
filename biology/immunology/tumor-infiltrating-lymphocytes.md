[Biology](../README.md) › [免疫學](README.md) › 腫瘤浸潤淋巴球

# 腫瘤浸潤淋巴球 (Tumor-Infiltrating Lymphocytes, TILs)

TIL 是從血液移入腫瘤微環境 (tumor microenvironment, TME) 的免疫細胞，以 T 細胞為主。數量與分布反映宿主對腫瘤的免疫反應，在多種癌症中具預後價值，也影響免疫治療的反應。

## 組成

| 細胞 | 在腫瘤中的角色 |
| --- | --- |
| CD8⁺ 毒殺 T 細胞 | 以 perforin、granzyme 殺死腫瘤細胞；密度高通常預後較好 |
| CD4⁺ 輔助 T 細胞 | 以細胞激素協調反應；TH1 偏向抗腫瘤 |
| 調節性 T 細胞 (Treg) | 抑制抗腫瘤免疫；CD8 / Treg 比值比單看 Treg 更有意義 |
| B 細胞、三級淋巴結構 (TLS) | 腫瘤內的類淋巴濾泡結構，與免疫治療反應較好相關 |
| NK 細胞 | 數量通常少，但可殺死 MHC I 下降的腫瘤細胞 |

髓系細胞（腫瘤相關巨噬細胞 TAM、MDSC）不屬於淋巴球，但是 TME 中主要的免疫抑制來源，分析時常一併評估。

## 免疫表型：熱腫瘤 vs 冷腫瘤

| 表型 | T 細胞位置 | 典型機制 | 免疫治療反應 |
| --- | --- | --- | --- |
| 發炎型（hot / inflamed） | 浸潤到腫瘤細胞之間 | 有抗原與 T 細胞，但被 PD-L1 等檢查點抑制 | 較可能有反應 |
| 排除型（immune-excluded） | 卡在基質 / 腫瘤邊緣 | 基質屏障、TGF-β | 反應差 |
| 荒漠型（immune-desert） | 幾乎沒有 | 抗原少、抗原呈現缺陷、T 細胞未被招募 | 反應差 |

> 「有 TIL」不等於「TIL 有功能」：長期抗原刺激下許多 TIL 進入耗竭狀態（PD-1、TIM-3、TOX 高），見 [T 細胞亞群：耗竭](t-cell-subsets-and-cytokines.md#cd8-t-細胞分化與耗竭)。

## 評估方法

| 方法 | 能看到 | 限制 |
| --- | --- | --- |
| H&E 病理判讀 | 基質 TIL (stromal TILs) 佔基質面積百分比 | 分不出亞群；觀察者間差異 |
| IHC / 多重螢光 IHC | CD3、CD8、CD4、FOXP3 的密度與空間分布 | 一次標記數有限 |
| Immunoscore | 腫瘤中心與侵襲邊緣的 CD3⁺、CD8⁺ 密度 | 主要在大腸癌驗證 |
| 流式細胞術 / scRNA-seq | 詳細表型、耗竭與 TCR 克隆 | 需新鮮組織解離，失去空間資訊 |
| 從 bulk RNA-seq 反推 | 免疫細胞比例估計（CIBERSORTx、xCell 等 deconvolution） | 依賴參考 signature，結果是相對估計 |

> 乳癌的基質 TIL 有國際 TILs Working Group 的標準化評分方式（以基質區域、排除腫瘤巢內與壞死區）；三陰性與 HER2⁺ 乳癌中，TIL 越高預後與化療反應越好。

## 臨床意義

| 面向 | 內容 |
| --- | --- |
| 預後 | 黑色素瘤、乳癌（三陰性、HER2⁺）、大腸癌等，TIL 越多存活通常越好 |
| 預測 | 浸潤的 CD8⁺ T 細胞多、發炎型 TME 的腫瘤較可能對檢查點抑制劑（anti-PD-1 / PD-L1、anti-CTLA-4）有反應；常與 PD-L1、TMB 一起看，見 [免疫標記](immune-marker.md#免疫檢查點-immune-checkpoints) |
| 治療 | 過繼性 TIL 療法 (adoptive TIL therapy)：手術取出腫瘤 → 體外擴增 TIL → 淋巴清除化療後回輸 + IL-2；在晚期黑色素瘤有持久反應，美國 FDA 於 2024 年 2 月加速核准 lifileucel（Amtagvi），用於 anti-PD-1 治療後惡化的晚期黑色素瘤，是第一個核准用於實體腫瘤的 TIL 療法 |

## 挑戰

| 問題 | 說明 |
| --- | --- |
| 標準化 | 各癌別評分方式、閾值不一 |
| 空間異質性 | 同一腫瘤不同區域密度差很多，切片取樣影響結果 |
| 功能耗竭 | 數量多但功能差，需搭配功能 / 耗竭標記 |
| 旁觀者 T 細胞 | 許多 TIL 辨識的是病毒等非腫瘤抗原，不參與抗腫瘤 |

相關：[癌症基因體](../genomics/cancer-genomics/README.md)、[單細胞 RNA-seq](../genomics/sequencing-techniques/single-cell-rna-seq/README.md)、[細胞激素網路](cytokines.md)。
