[基因體學](../README.md) › [癌症基因體](README.md) › 突變特徵

# 突變特徵 (Mutational Signatures)

不同的致突變過程（老化、紫外線、菸草、APOBEC 酵素、DNA 修復缺陷）會在基因組上留下特定的突變「型態」。把腫瘤的體細胞突變分類計數，再拆解成已知特徵的組合，可以推斷腫瘤經歷過哪些過程，有些還有治療意義。

## 突變怎麼分類

| 類型 | 分類方式 | 類別數 |
| --- | --- | --- |
| SBS（單鹼基置換） | 6 種置換（以嘧啶 C / T 為參考：C>A、C>G、C>T、T>A、T>C、T>G）× 前後各一個鹼基（4 × 4） | **96** |
| DBS（雙鹼基置換） | 相鄰兩個鹼基同時改變（如 CC>TT） | 78 |
| ID（小插入 / 缺失） | 長度、是否在重複序列 / microhomology 中 | 83 |
| CN、SV | 拷貝數片段長度 / 狀態、結構變異型態 | 依版本 |

例：`A[C>T]G` 是「前一個鹼基 A、後一個鹼基 G 的 C>T」，屬於 CpG 位點的 C>T，是 SBS1 的特徵。

## 常見 SBS 特徵（COSMIC）

| 特徵 | 成因 | 臨床 / 生物意義 |
| --- | --- | --- |
| SBS1 | 5-甲基胞嘧啶自發去胺基（CpG 的 C>T） | 時鐘型：隨年齡與細胞分裂累積 |
| SBS5 | 不明，時鐘型 | 幾乎所有腫瘤都有 |
| SBS2、SBS13 | APOBEC 胞嘧啶去胺基酶（TCW 序列的 C>T / C>G） | 乳癌、膀胱癌、子宮頸癌常見 |
| SBS3 | 同源重組修復缺陷 (HRD)，如 *BRCA1/2* | 可能對 PARP 抑制劑、鉑類藥物敏感 |
| SBS4 | 菸草（C>A） | 吸菸者的肺癌 |
| SBS7a / b | 紫外線（CC>TT、C>T） | 黑色素瘤、皮膚癌 |
| SBS6、15、26、44 | 錯配修復缺陷 (MMR / MSI) | 可能對免疫檢查點抑制劑有反應 |
| SBS10a / b | *POLE* 校對功能突變 | 超高突變量 |
| SBS18 | 活性氧造成的損傷（C>A） | 也可能是樣本處理假象 |

COSMIC 目錄持續改版，也標示了已知的**定序假象特徵**（例如某些 SBS 與 FFPE、氧化損傷相關），解讀前先排除。參考目錄：[COSMIC Mutational Signatures](https://cancer.sanger.ac.uk/signatures/)。

## 分析方法

| 方法 | 做法 | 工具 |
| --- | --- | --- |
| 萃取 (extraction / de novo) | 用 NMF 從一批腫瘤的突變矩陣中找出特徵，再與 COSMIC 比對 | SigProfilerExtractor、MutationalPatterns |
| 擬合 (fitting / refitting) | 已知特徵目錄下，估計每個樣本各特徵的貢獻比例 | SigProfilerAssignment、deconstructSigs、MutationalPatterns `fit_to_signatures()`、sigminer |

```r
library(MutationalPatterns); library(BSgenome.Hsapiens.UCSC.hg38)
grl <- read_vcfs_as_granges(vcf_files, sample_names, "BSgenome.Hsapiens.UCSC.hg38")
mm  <- mut_matrix(grl, ref_genome = "BSgenome.Hsapiens.UCSC.hg38")   # 96 × 樣本
plot_96_profile(mm[, 1:2])
sigs <- get_known_signatures()                                          # COSMIC SBS
fit  <- fit_to_signatures_strict(mm, sigs, max_delta = 0.004)          # 減少過度擬合
# 以上依 MutationalPatterns 官方文件整理，未在本機實跑（需要 BSgenome hg38）
```

## 解讀注意

| 注意 | 說明 |
| --- | --- |
| 突變數要夠 | 擬合需要足夠突變（WGS 通常沒問題；WES / panel 突變少，結果不穩、常需整批分析） |
| 過度擬合 | 用全部特徵擬合會分配少量貢獻給許多不相關特徵；限制在該癌別已知的特徵，或用 strict / bootstrap 方法 |
| 必須是體細胞突變 | 未扣除 germline 變異會污染結果；只有腫瘤時更要小心 |
| 定序假象 | FFPE（C>T）、氧化（C>A）會產生類似特徵 |
| 成因未明 | 不少特徵的病因仍不清楚，不要過度推論 |

相關：[Somatic 變異呼叫](../workflows/variant-calling.md#somatic-流程mutect2)、[COSMIC](../../genetics/databases/variant/cosmic.md)；中文概述參考 [突變特徵（yourgene）](https://yourgene.pixnet.net/blog/posts/7120936731)。
