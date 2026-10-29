[遺傳學](../README.md) › [變異判讀](README.md) › HGVS 命名

# HGVS 變異命名 (HGVS Nomenclature)

HGVS（Human Genome Variation Society）制定的序列變異描述標準，讓研究與臨床報告用同一種寫法表示同一個變異。完整規範：[hgvs-nomenclature.org](https://hgvs-nomenclature.org/stable/)。

一個完整的 HGVS 描述 = **參考序列（含版本）+ 前綴 + 變異**，例：`NM_000546.6(TP53):c.215C>G p.(Pro72Arg)`。

## 參考序列前綴

| 前綴 | 參考序列 | 例 |
| --- | --- | --- |
| `g.` | 基因組 | `NC_000017.11:g.7676154G>C` |
| `c.` | 編碼 DNA（cDNA），A of ATG = c.1 | `NM_000546.6:c.215C>G` |
| `n.` | 非編碼 RNA 轉錄本 | `NR_…:n.100A>G` |
| `r.` | RNA | `r.215c>g` |
| `p.` | 蛋白質 | `NP_000537.3:p.(Pro72Arg)` |
| `m.` | 粒線體 | `m.3243A>G` |

## 常見寫法

| 類型 | DNA | 蛋白質 |
| --- | --- | --- |
| 置換 | `c.35G>A` | `p.(Gly12Asp)`（KRAS G12D） |
| 缺失 | `c.68_69del` | `p.(Glu23ValfsTer17)`（移碼） |
| 重複 | `c.5266dup` | `p.(Gln1756ProfsTer74)` |
| 插入 | `c.100_101insT` | |
| 缺失插入 | `c.100_102delinsTT` | |
| 無意義 | `c.1234C>T` | `p.(Arg412Ter)` 或 `p.(Arg412*)` |
| 同義 | `c.123A>G` | `p.(=)` |
| 起始密碼子 | `c.1A>G` | `p.(Met1?)` |

| 位置寫法 | 意義 |
| --- | --- |
| `c.88+1G>A` | exon 最後一個鹼基 c.88 之後，intron 第 1 個鹼基（剪接供位） |
| `c.89-2A>G` | 下一個 exon 第一個鹼基 c.89 之前 2 個鹼基（剪接受位） |
| `c.-14G>C` | 5′ UTR（ATG 上游） |
| `c.*30A>T` | 3′ UTR（終止密碼子下游） |

> 蛋白質變化加括號 `p.(…)` 表示是**預測**（未直接檢驗 RNA / 蛋白）。舊寫法 `c.68_69delAG`、`185delAG` 仍常見於文獻，現行建議 `c.68_69del`，並用三字母胺基酸碼。

## 3′ 規則 vs VCF 左對齊

重複序列中的 indel 有多個等效位置：

| 系統 | 規則 |
| --- | --- |
| HGVS | **3′ 規則**：放在轉錄本方向最 3′ 端的位置（負股基因要依轉錄方向判斷） |
| VCF | **左對齊**：放在基因組座標最左側（`bcftools norm`） |

兩者對同一個 indel 給出的位置可能不同；VEP 等工具會自動處理，手動轉換時容易出錯。

## 實務

| 原則 | 說明 |
| --- | --- |
| 一律帶轉錄本與版本號 | `c.` 位置依轉錄本而異；臨床用 [MANE Select](../../genomics/reference-data/gene-annotations.md#mane臨床報告的預設轉錄本) |
| 用工具驗證 | [VariantValidator](https://variantvalidator.org/)、[Mutalyzer](https://mutalyzer.nl/) 檢查寫法、轉換 `g.` ↔ `c.` ↔ `p.` |
| 報告同時列 `c.` 與 `p.` | 再附 `g.` 座標與基因組版本 |
| 搜尋資料庫 | 文獻可能用舊寫法或不同轉錄本，必要時以基因組座標搜尋 |

相關：[座標系統](../../genomics/file-formats/zero-one-based.md)、[VCF 正規化](../../genomics/file-formats/vcf.md#同一個變異的不同寫法)、[Ensembl VEP](../databases/variant/ensembl-vep.md)。
