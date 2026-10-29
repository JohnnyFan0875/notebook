[分子生物學](../README.md) › [實驗方法](README.md) › Western blot

# Western Blot

以 SDS-PAGE 依分子量分離蛋白質、轉漬到膜上，再用抗體偵測特定蛋白。可確認蛋白是否表現、大小是否正確，以及磷酸化等轉譯後修飾 (PTM)；常用來驗證轉錄體或基因編輯（knockout）的結果在蛋白層級是否成立。

## 流程

```text
細胞 / 組織裂解 → 蛋白定量（BCA / Bradford）→ SDS-PAGE
→ 轉漬到 PVDF / 硝化纖維膜 → blocking（脫脂奶粉 / BSA）
→ 一級抗體 → 二級抗體（HRP 或螢光）→ 化學冷光 / 螢光顯影 → 條帶定量
```

## 關鍵控制與判讀

| 項目 | 做法 / 意義 |
| --- | --- |
| 上樣對照 (loading control) | GAPDH、β-actin、tubulin，或總蛋白染色（較不受處理影響，期刊漸多要求） |
| 抗體專一性 | 用 knockout / knockdown 樣本或過表現樣本確認條帶；同一抗體可能有非專一條帶 |
| 修飾蛋白 | 磷酸化抗體搭配總蛋白抗體，報告磷酸化 / 總量比值 |
| 分子量偏移 | 糖基化、磷酸化、剪接型或裂解會讓條帶偏離預測大小 |
| 定量限制 | 化學冷光易飽和、線性範圍窄；只算**半定量**，需在線性範圍內曝光並做生物重複 |

> 要精確定量（尤其是體液蛋白）改用 [ELISA](elisa.md) 或質譜；蛋白的預測大小、PTM 位點可查 [UniProt](../molecular-databases/uniprot.md)，抗體驗證影像可查 [Human Protein Atlas](../molecular-databases/human-proteome-atlas.md)。
