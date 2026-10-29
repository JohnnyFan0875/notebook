[臨床資訊與標準](../README.md) › [臨床資料庫](README.md) › UK Biobank

# UK Biobank

UK Biobank 是約 50 萬名英國成人的前瞻性世代，整合基因體、影像、生物標記、問卷與長期病歷連結（住院、癌症登記、死亡登記、基層醫療）。它是 GWAS、多基因風險分數 (PRS)、孟德爾隨機化與蛋白質體研究最常用的資源。

| 項目 | 內容 |
| --- | --- |
| 網站 | [ukbiobank.ac.uk](https://www.ukbiobank.ac.uk)、欄位瀏覽 [Data Showcase](https://biobank.ndph.ox.ac.uk/showcase/) |
| 招募 | 2006–2010 年，40–69 歲 |
| 申請 | 註冊研究者 → 提交研究計畫 → 核准 → 付存取費；成果需回傳 UK Biobank |
| 存取 | 雲端 Research Analysis Platform（UKB-RAP，DNAnexus），在平台上運算並付雲端費用 |

## 資料類型

| 資料 | 規模 | 用途 |
| --- | --- | --- |
| 基因型晶片 + imputation | 全體約 50 萬人 | GWAS、PRS |
| 全外顯子定序 (WES) | 約 47 萬人 | 罕見變異負荷檢定 (burden test) |
| 全基因組定序 (WGS) | 全體 50 萬人（2023 年釋出） | 非編碼與結構變異 |
| 影像 | 目標 10 萬人（腦、心臟、腹部 MRI、DXA） | 影像表型、影像基因體 |
| 蛋白質體 | UKB-PPP 約 5.3 萬人（Olink） | pQTL，見 [pQTL](../../genomics/genome-wide-analysis/pqtl.md) |
| 生化檢驗、問卷、穿戴裝置 | 全體 / 子集 | 共變數、環境暴露 |
| 病歷連結 | ICD-10 住院、癌症、死亡、部分基層醫療 | 疾病結果 |

## 分析注意

| 注意 | 說明 |
| --- | --- |
| Healthy volunteer bias | 參與者比一般族群健康、社經地位高，盛行率與絕對風險不能直接外推，見 [資料偏誤與代表性](../../../data-science/responsible-ai/data-bias-and-representativeness.md) |
| 族群組成 | 以歐洲血統為主；其他族群樣本小，PRS 可轉移性差 |
| 親緣與族群結構 | 用官方提供的親緣係數排除相關個體、以 PCs 校正，見 [GWAS](../../genomics/genome-wide-analysis/gwas-fundamental.md) |
| 結果定義 | 疾病常合併自填、ICD 住院碼與死亡登記；不同來源的敏感度不同 |
| 欄位版本 | 用 Data Showcase 的 field ID，並記錄資料釋出日期 |

台灣的對應資源是台灣人體生物資料庫 (Taiwan Biobank) 與 [TaiwanGenomes](../../genetics/databases/population-frequency/taiwangenomes.md)。
