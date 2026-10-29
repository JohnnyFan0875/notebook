[分子生物學](../README.md) › [實驗方法](README.md) › BAC

# 細菌人工染色體 (Bacterial Artificial Chromosome, BAC)

以大腸桿菌 F 質體 (F-factor) 為基礎的選殖載體，可在細菌內穩定攜帶約 100–300 kb 的外來 DNA，且每個細胞只維持 1–2 個拷貝，不易重組。它是人類基因體計畫「逐一選殖定序」策略的核心。

## 載體比較

| 載體 | 插入片段大小 | 宿主 | 特性 |
| --- | --- | --- | --- |
| 質體 (plasmid) | < 約 15 kb | 大腸桿菌 | 高拷貝、操作最簡單 |
| Cosmid | 35–45 kb | 大腸桿菌 | 利用 λ 噬菌體 cos 位點包裝 |
| Fosmid | 約 40 kb | 大腸桿菌 | F 質體骨架、單拷貝、穩定 |
| BAC | 100–300 kb | 大腸桿菌 | 單拷貝、穩定、嵌合 (chimera) 少 |
| PAC | 100–300 kb | 大腸桿菌 | 以 P1 噬菌體為基礎 |
| YAC（酵母人工染色體） | 100 kb – 1 Mb 以上 | 酵母 | 可攜帶最大片段，但易嵌合與重排 |

## 應用

| 應用 | 說明 |
| --- | --- |
| 基因體定序 | 人類基因體計畫先建立 BAC 物理圖譜，再逐一 shotgun 定序每個 BAC；GRCh 參考基因體的許多片段仍以 BAC 為單位（見[參考基因體](../../genomics/reference-data/reference-genomes.md)） |
| 細胞遺傳學 | BAC 作為 FISH 探針；早期 array CGH 用 BAC 陣列偵測拷貝數變異 |
| 轉殖動物 | BAC 轉殖小鼠攜帶完整基因與遠端調控元件 |
| 長片段參考 | 複雜或重複區域（如 MHC）的組裝、驗證 long-read 組裝 |

> 現在全基因體組裝多以 long-read 定序（PacBio HiFi、ONT）+ Hi-C 完成（如 T2T-CHM13），BAC 的角色轉為特定區域的驗證與功能研究。
