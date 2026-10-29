[遺傳學](../README.md) › [變異判讀](README.md) › ACMG/AMP

# ACMG/AMP 變異分級 (ACMG/AMP Variant Classification)

ACMG 與 AMP 於 2015 年發布的 germline 序列變異判讀準則（Richards et al., Genet Med 2015），是孟德爾疾病臨床報告的共同語言：把各類證據歸成有方向（致病 / 良性）與強度的準則，再依組合規則分成五級。

| 分級 | 意義 |
| --- | --- |
| Pathogenic (P) | 致病 |
| Likely pathogenic (LP) | 可能致病（約 > 90% 確定） |
| Uncertain significance (VUS) | 意義不明：**不應用於臨床決策** |
| Likely benign (LB) | 可能良性 |
| Benign (B) | 良性 |

> 分級的對象是「某個變異對某個疾病（含遺傳模式）」，不是變異本身。同一個變異對不同疾病可能有不同分級。

## 致病證據

| 強度 | 準則 | 內容 |
| --- | --- | --- |
| 非常強 | PVS1 | 無功能變異（nonsense、frameshift、±1/2 剪接位點、起始密碼子、單 / 多 exon 缺失），且功能喪失是該疾病的機制 |
| 強 | PS1 | 與已知致病變異造成相同胺基酸改變 |
| | PS2 | 確認的新生變異（親子關係已確認），且表型相符 |
| | PS3 | 可靠的功能試驗顯示有害 |
| | PS4 | 病例中的頻率顯著高於對照 |
| 中 | PM1 | 位於突變熱點或無良性變異的關鍵功能區 |
| | PM2 | 在族群資料庫中缺席或極罕見 |
| | PM3 | 隱性疾病：與致病變異呈反式 (in trans) |
| | PM4 | 蛋白長度改變（框內 indel、終止密碼子消失） |
| | PM5 | 新的錯義變異，同一胺基酸位置已有不同的致病錯義變異 |
| | PM6 | 假定的新生變異（未確認親子關係） |
| 支持 | PP1 | 在家族中與疾病共分離 |
| | PP2 | 錯義變異，且該基因很少有良性錯義、錯義是常見致病機制 |
| | PP3 | 多個計算工具預測有害（見 [in-silico 預測](in-silico-prediction.md)） |
| | PP4 | 病人表型或家族史高度專一於該基因的疾病 |
| | PP5 | 可信來源報告為致病（ClinGen SVI 建議**不再使用**） |

## 良性證據

| 強度 | 準則 | 內容 |
| --- | --- | --- |
| 獨立 | BA1 | 族群頻率 > 5%（ClinGen 另列少數例外變異） |
| 強 | BS1 | 頻率高於該疾病所能容許的程度 |
| | BS2 | 在健康成人中觀察到（完全外顯、早發的疾病） |
| | BS3 | 可靠的功能試驗顯示無影響 |
| | BS4 | 家族中不共分離 |
| 支持 | BP1 | 錯義變異，但該基因的致病機制主要是截斷型變異 |
| | BP2 | 與致病變異呈順式 (in cis)，或顯性基因中與致病變異呈反式 |
| | BP3 | 重複區中、無已知功能的框內 indel |
| | BP4 | 多個計算工具預測無影響 |
| | BP5 | 病人已找到其他分子病因 |
| | BP6 | 可信來源報告為良性（SVI 建議不再使用） |
| | BP7 | 同義變異且預測不影響剪接 |

## 組合規則（2015 原版）

| 分級 | 符合任一組合 |
| --- | --- |
| Pathogenic | PVS1 + (≥ 1 PS 或 ≥ 2 PM 或 1 PM + 1 PP 或 ≥ 2 PP)；≥ 2 PS；1 PS + (≥ 3 PM 或 2 PM + ≥ 2 PP 或 1 PM + ≥ 4 PP) |
| Likely pathogenic | PVS1 + 1 PM；1 PS + 1–2 PM；1 PS + ≥ 2 PP；≥ 3 PM；2 PM + ≥ 2 PP；1 PM + ≥ 4 PP |
| Benign | BA1；≥ 2 BS |
| Likely benign | 1 BS + 1 BP；≥ 2 BP |
| VUS | 不符合上述，或致病與良性證據互相矛盾 |

### 計分版（貝氏框架）

Tavtigian et al.（2018、2020）把準則轉成點數，更容易處理強度調整與矛盾證據；新版 ACMG/AMP 準則也朝計分制發展。

| 強度 | 致病點數 | 良性點數 |
| --- | --- | --- |
| 支持 | +1 | −1 |
| 中 | +2 | −2 |
| 強 | +4 | −4 |
| 非常強 | +8 | −8 |

| 總分 | ≥ 10 | 6–9 | 0–5 | −1 至 −6 | ≤ −7 |
| --- | --- | --- | --- | --- | --- |
| 分級 | P | LP | VUS | LB | B |

例：無意義變異 PVS1（+8）+ gnomAD 缺席 PM2_Supporting（+1）= 9 → LP；再加確認的新生變異 PS2（+4）= 13 → P。

## ClinGen SVI 的重要修訂

| 準則 | 修訂 |
| --- | --- |
| PVS1 | 決策樹（Abou Tayoun 2018）：依 NMD、剪接、exon 是否在關鍵區域等，下調為 Strong / Moderate / Supporting |
| PM2 | 預設降為 **Supporting** |
| PP3 / BP4 | 以 REVEL 等工具的校準閾值決定強度，最高可到 Strong（Pejaver 2022），見 [in-silico 預測](in-silico-prediction.md) |
| PS2 / PM6 | 新生變異依表型專一性與親子確認計分 |
| PS3 / BS3 | 功能試驗需經驗證，依對照數量給強度 |
| PP5 / BP6 | 不再使用 |
| 基因專一規則 | ClinGen VCEP 為特定基因（如 *MYH7*、*PTEN*、*TP53*）訂定調整版準則，優先採用 |

## 相關架構

| 架構 | 適用 |
| --- | --- |
| ACMG/AMP 2015 + SVI | germline 序列變異 |
| ACMG / ClinGen CNV 準則（Riggs 2020） | 拷貝數變異，計分制 |
| AMP / ASCO / CAP 2017 | **體細胞**變異：Tier I（強臨床意義）– IV（良性），依治療、診斷、預後證據 |
| ClinGen / CGC / VICC 致癌性準則（2022） | 體細胞變異的致癌性 (oncogenicity) 分級 |
| ACGS 最佳實務 | 英國版的 ACMG 調整，見 [ACGS 指引](acgs-guideline.md) |

證據來源：[族群頻率](../databases/population-frequency/README.md)、[ClinVar](../databases/variant/clinvar.md)、[基因–疾病關聯](../databases/gene-disease-association/README.md)、[新生變異](../foundations/de-novo-variant.md)。ClinGen 的工具與指引見 [ClinGen 指引](clingen-guidelines.md)。
