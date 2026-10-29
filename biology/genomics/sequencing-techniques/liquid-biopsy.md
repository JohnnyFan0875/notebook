[基因體學](../README.md) › [定序技術](README.md) › 液態切片

# 液態切片 (Liquid Biopsy)

從血液（或尿液、腦脊髓液）偵測腫瘤來源的物質，取代或補充組織切片。主要分析對象是游離 DNA（cfDNA）中的腫瘤 DNA（ctDNA），以及循環腫瘤細胞（CTC）。

## cfDNA、ctDNA、CTC

```
血漿中的 cfDNA（cell-free DNA）
 ├── 來自正常細胞（主要是血球）……大部分
 └── ctDNA（circulating tumor DNA）……腫瘤來源，常只佔 0.01–10%
血液中的 CTC（circulating tumor cells）……完整的腫瘤細胞，每 mL 約 1–10 個
```

| | cfDNA | ctDNA | CTC |
| --- | --- | --- | --- |
| 本質 | 所有游離 DNA 片段 | cfDNA 中腫瘤來源的部分 | 完整、存活的腫瘤細胞 |
| 來源 | 正常細胞凋亡 / 壞死（血球為主；懷孕時含胎盤） | 腫瘤細胞凋亡、壞死、主動分泌 | 從腫瘤脫落進入血流 |
| 大小 / 量 | ~167 bp（核小體大小）；健康人 5–50 ng/mL 血漿 | 片段往往比正常 cfDNA 短 | 極稀少 |
| 分析層次 | 濃度、片段型態、甲基化 | 突變、CNV、甲基化、片段型態 (fragmentomics) | 形態、單細胞 DNA / RNA、蛋白、藥物測試 |
| 主要用途 | NIPT、移植排斥監測、組織損傷 | 突變檢測、療效監測、MRD、早期篩檢 | 預後、轉移機制研究 |

## ctDNA vs CTC

| 面向 | ctDNA | CTC |
| --- | --- | --- |
| 代表意義 | 腫瘤負荷與細胞更新（死亡細胞的 DNA） | 具轉移能力的存活細胞 |
| 敏感度 | 高（可偵測 VAF 0.1% 以下） | 中（細胞稀少） |
| 專一性 | 中（會混入克隆性造血 CHIP 等非腫瘤變異） | 高（可確認腫瘤來源） |
| 技術難度 | 中：血漿萃取 + 高靈敏定序 | 高：分離困難、標準化不足 |
| 臨床成熟度 | 已用於標靶治療用藥（如 *EGFR*） | CellSearch（FDA 核准，用於乳癌、攝護腺癌、大腸癌預後） |

| 目的 | 首選 | 原因 |
| --- | --- | --- |
| 標靶治療突變檢測（*EGFR*、*KRAS*、*PIK3CA*） | ctDNA | 靈敏、非侵入、臨床已標準化 |
| 療效與復發監測、MRD | ctDNA | 可量化、可長期追蹤，常早於影像 |
| 早期多癌篩檢 (MCED) | ctDNA 甲基化 / 片段型態 | 例：GRAIL Galleri |
| 轉移機制、EMT、幹細胞性 | CTC | 有存活細胞可做形態與功能分析 |
| 轉移風險 | CTC + ctDNA | 互補：活性 vs 負荷 |

## 依癌別

| 癌別 | ctDNA | CTC | 備註 |
| --- | --- | --- | --- |
| 肺癌 | *EGFR*（含抗藥突變 T790M）、*KRAS*、*ALK* 融合 | 數量少 | ctDNA 為臨床主流 |
| 乳癌 | *PIK3CA*、*ESR1*（內分泌治療抗藥） | CellSearch 偵測率高，預後價值明確 | 兩者都成熟 |
| 攝護腺癌 | *BRCA1/2*、*ATM* | AR-V7 剪接變體 | mCRPC 常合併使用 |
| 大腸癌 | *KRAS*、*NRAS*、*BRAF*（預測抗 EGFR 療效）；MRD | 反映轉移與復發風險 | ctDNA 較靈敏 |
| 肝癌 | 甲基化、*TP53* | 可用於監測 | ctDNA 快速發展中 |
| 胰臟 / 膽道癌 | *KRAS* | 不易偵測 | ctDNA 較佳 |
| 腦瘤 | 血漿中極少（血腦屏障） | 罕見 | 改測腦脊髓液 (CSF) cfDNA |
| 胃 / 食道癌 | *HER2*、*TP53*、甲基化 | 反映轉移進展 | 兩者都在發展 |

## 偵測技術

| 技術 | 範圍 | 靈敏度 | 說明 |
| --- | --- | --- | --- |
| qPCR / ddPCR | 已知熱點 | 高（~0.1%） | 便宜快速，一次只能測少數突變 |
| 標靶 NGS panel + UMI | 數十到數百個基因 | 0.1–0.5% | 需要極高原始深度與 UMI 錯誤校正 |
| 腫瘤導向 (tumor-informed) MRD | 依組織定序結果客製 16–50 個突變追蹤 | 0.01% 以下 | 例：Natera Signatera |
| 全基因組低深度 / 甲基化 / 片段型態 | 全基因組 | 依方法 | 早期篩檢、組織來源預測 |

## 分析上的挑戰

| 挑戰 | 說明 | 對策 |
| --- | --- | --- |
| 極低 VAF | 真突變與定序 / PCR 錯誤同一量級 | UMI 一致序列（duplex 最準）、背景錯誤模型 |
| 起始分子數有限 | 10 ng cfDNA 約 3,000 個基因組拷貝；VAF 0.1% 只有約 3 個突變分子 | 偵測極限由分子數決定，不只是定序深度 |
| 克隆性造血 (CHIP) | 血球的體細胞突變（*DNMT3A*、*TET2*、*ASXL1*）出現在 cfDNA | 同時定序白血球 (buffy coat) 排除 |
| 前處理 | 血球破裂釋出基因組 DNA 稀釋 ctDNA | 專用採血管（Streck）、時限內分離血漿 |
| 陰性結果 | 腫瘤釋出 DNA 少（低 shedding）時偽陰性 | 陰性不代表無腫瘤，必要時仍需組織檢測 |

相關：[重複率與 UMI](../ngs-qc/duplication-rate.md)、[Picard MarkDuplicates：UMI](../../bioinformatics-tools/ngs-tools/picard-markduplicates.md)、[癌症基因體](../cancer-genomics/README.md)、[血清 vs 血漿](../../laboratory-medicine/sample-types/serum-plasma.md)。
