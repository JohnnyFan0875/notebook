[Biology](../README.md) › [免疫學](README.md) › 細胞激素

# 細胞激素網路 (Cytokine Network)

細胞激素 (cytokine) 是免疫細胞之間溝通的可溶性訊號分子，決定免疫反應偏向發炎或耐受、偏向哪一種類型（第 1 / 2 / 3 型免疫），進而影響感染、過敏、自體免疫與癌症的走向。各細胞亞群的特性見 [T 細胞亞群](t-cell-subsets-and-cytokines.md) 與 [B 細胞亞群](b-cell-subsets-and-cytokines.md)。

## 細胞激素家族

| 家族 | 代表成員 | 主要作用 | 主要來源 |
| --- | --- | --- | --- |
| 介白素 (IL) | IL-1 至 IL-38 | 活化、分化、發炎調節，功能多樣 | 各種免疫細胞 |
| 干擾素 (IFN) | 第 I 型 IFN-α / β；第 II 型 IFN-γ | 抗病毒、提升 MHC 表現與抗原呈現 | 樹突細胞、NK、TH1 |
| 腫瘤壞死因子 (TNF) | TNF-α、TNF-β（LT-α） | 發炎、細胞凋亡 | 巨噬細胞、T 細胞 |
| 轉化生長因子 (TGF) | TGF-β1、TGF-β2 | 免疫抑制、纖維化、組織修復 | Treg、上皮細胞 |
| 趨化激素 (chemokine) | CCL2、CXCL8（IL-8）、CXCL10 | 引導免疫細胞移動到感染 / 發炎處 | 多種細胞 |
| 群落刺激因子 (CSF) | GM-CSF、G-CSF | 刺激骨髓與顆粒球系的生成與分化 | 基質細胞、T 細胞 |

| 功能分類 | 代表 | 作用 | 來源 |
| --- | --- | --- | --- |
| 促發炎 | IL-1β、IL-6、TNF-α、IFN-γ、IL-17 | 引發發炎、發燒、血管擴張、細胞活化 | 巨噬細胞、TH1、TH17 |
| 抗發炎 | IL-10、TGF-β | 抑制過度活化、促進修復 | Treg、Breg、樹突細胞 |
| 生長 / 存活 | IL-2、IL-7、IL-15、IL-21 | 淋巴球增生與維持 | T 細胞、NK、Tfh |
| B 細胞刺激 | IL-4、IL-5、IL-6、IL-21、BAFF、APRIL | 活化 B 細胞、促進抗體生成與漿細胞存活 | TH2、Tfh、單核球、FDC |

## 細胞間的激素溝通

| 方向 | 細胞激素 | 結果 |
| --- | --- | --- |
| NK / 樹突細胞 → T 細胞 | IL-12、IFN-α/β | 誘導 TH1 分化、抗病毒免疫 |
| TH1 → 巨噬細胞 | IFN-γ、TNF-α | 活化巨噬細胞，清除胞內病原 |
| TH2 → B 細胞 / 嗜酸性球 / 肥大細胞 | IL-4、IL-5、IL-13 | IgE 生成、嗜酸性球活化：過敏與抗寄生蟲 |
| TH17 → 嗜中性球 / 上皮 | IL-17A、IL-22 | 招募嗜中性球、強化黏膜屏障 |
| Tfh → B 細胞 | IL-21、IL-4（+ CD40L） | 生發中心形成、親和力成熟 |
| Treg / Breg → 多種細胞 | IL-10、TGF-β | 抑制 TH1 / TH17、維持耐受 |

## 交互抑制

```
TH1（IFN-γ）────┬── 活化巨噬細胞
                └── 抑制 TH2、TH17
TH2（IL-4、IL-13）┬── 活化 B 細胞（IgE）
                  └── 抑制 TH1
Treg（IL-10、TGF-β）┬── 抑制 TH1 / TH17
                    └── 維持耐受
TH17（IL-17、IL-22）── 招募嗜中性球；失控時放大發炎
```

IFN-γ、IL-4、IL-10 是典型的互相拮抗的細胞激素；疾病往往反映這個平衡的偏移。

## 抗體類別轉換 (Class Switching)

| 細胞激素 | 人類 | 小鼠 | 功能 |
| --- | --- | --- | --- |
| IL-4（+ IL-13） | IgE、IgG4 | IgE、IgG1 | 過敏、抗寄生蟲 |
| TGF-β（+ IL-5、APRIL） | IgA | IgA | 黏膜防禦 |
| IFN-γ | IgG1、IgG3（促進） | IgG2a / IgG2c | 調理作用、抗病毒 |
| IL-21 | IgG1、IgG3 | — | 補體活化、生發中心反應 |
| IL-10 | IgG4（與 IL-4 協同） | — | 抗發炎 |

> 教科書與原始文獻中「IFN-γ → IgG2a」是**小鼠**的結果；人類沒有 IgG2a，引用時注意物種。B 細胞的分化路徑見 [B 細胞亞群](b-cell-subsets-and-cytokines.md)。

## 疾病中的主導軸

| 情境 | 主導細胞 | 細胞激素 | 免疫反應類型 |
| --- | --- | --- | --- |
| 病毒感染（流感、HBV、SARS-CoV-2） | TH1、CTL、NK | IFN-α / γ、IL-2、IL-12 | 第 1 型 |
| 胞內細菌（結核） | TH1、巨噬細胞 | IFN-γ、TNF-α | 第 1 型；肉芽腫 |
| 寄生蟲（蠕蟲） | TH2、嗜酸性球 | IL-4、IL-5、IL-13 | 第 2 型 |
| 黴菌（念珠菌、麴菌） | TH17 | IL-17、IL-22 | 第 3 型 |
| 過敏（氣喘、異位性皮膚炎） | TH2 | IL-4、IL-13、IL-5 | 第 2 型 |
| 自體免疫（RA、MS、T1DM、乾癬） | TH1、TH17 | IFN-γ、IL-17、TNF-α | 發炎 |
| 腫瘤免疫逃脫、慢性發炎 | Treg、M2 巨噬細胞 | IL-10、TGF-β | 抑制 / 耐受 |
| 自體抗體疾病（SLE） | 過度活化的生發中心 B 細胞 | IL-6、BAFF、IL-21、IFN-α | 體液 |

## 治療標的

| 標的 | 藥物例 | 疾病 |
| --- | --- | --- |
| TNF-α | adalimumab、infliximab、etanercept | RA、IBD、乾癬 |
| IL-6 受體 | tocilizumab | RA、細胞激素釋放症候群 (CRS) |
| IL-17A / IL-23 | secukinumab / ustekinumab、guselkumab | 乾癬、乾癬性關節炎 |
| IL-4Rα（阻斷 IL-4 / IL-13） | dupilumab | 異位性皮膚炎、氣喘 |
| IL-5 | mepolizumab | 嗜酸性球氣喘 |
| BAFF | belimumab | SLE |
| 重組細胞激素 | IFN-α、IL-2 | 病毒性肝炎（舊療法）、部分癌症 |

相關：[免疫標記](immune-marker.md)、[腫瘤浸潤淋巴球](tumor-infiltrating-lymphocytes.md)、[PBMC](pbmc.md)。
