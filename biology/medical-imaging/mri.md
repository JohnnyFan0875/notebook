[Biology](../README.md) › [醫學影像](README.md) › MRI

# 磁振造影 (Magnetic Resonance Imaging, MRI)

MRI 把人體放在強磁場中，以射頻脈衝激發氫原子核，再量測它們回到平衡時發出的訊號。不同組織的弛豫時間 (T1、T2) 不同，調整脈衝參數就能得到強調不同性質的「加權」影像。軟組織對比是所有模態中最好的，且沒有游離輻射。

## 常用序列

| 序列 | 亮（高訊號） | 暗（低訊號） | 主要用途 |
| --- | --- | --- | --- |
| T1 加權 (T1WI) | 脂肪、釓顯影劑、亞急性出血 | 水、腦脊髓液 | 解剖結構；打顯影劑前後比較 |
| T2 加權 (T2WI) | 水、腦脊髓液、水腫 | 骨皮質、纖維 | 病灶、水腫、囊腫 |
| FLAIR | 水腫、病灶（腦脊髓液被抑制成暗） | 腦脊髓液 | 腦室旁病灶（多發性硬化）、腦白質病變 |
| DWI / ADC | DWI 亮 + ADC 暗 = 擴散受限 | — | 急性腦梗塞（數分鐘內即可見）、膿瘍、高細胞密度腫瘤 |
| 脂肪抑制（STIR、fat-sat） | 去除脂肪訊號後的水腫 | 脂肪 | 骨髓水腫、肌肉骨骼發炎 |
| SWI / T2* GRE | — | 出血、鈣化、鐵沉積 | 微出血、靜脈構造 |

> 記法：T1 看「解剖」與「顯影」、T2 看「水」。同一個病灶在 T1 暗、T2 亮，通常代表含水量高（水腫、囊腫）。

## 進階技術

| 技術 | 量什麼 | 應用 |
| --- | --- | --- |
| fMRI（BOLD） | 腦血氧變化 → 間接反映神經活動 | 腦功能定位、術前語言區定位、神經科學研究 |
| DTI | 水分子擴散方向 | 白質纖維束追蹤 (tractography) |
| MRS | 組織代謝物濃度（NAA、膽鹼、乳酸…） | 腫瘤、代謝疾病 |
| MRA | 血管（可不打顯影劑） | 動脈瘤、狹窄 |
| 灌流 (perfusion) | 局部血流 | 腫瘤分級、中風缺血區 |

## 顯影劑與安全

| 項目 | 說明 |
| --- | --- |
| 釓 (gadolinium) 顯影劑 | 縮短 T1，使富血流或血腦屏障破壞的區域變亮 |
| 腎功能 | 重度腎功能不全者使用部分釓劑有腎因性全身纖維化 (NSF) 風險；巨環類 (macrocyclic) 釓劑風險較低 |
| 釓沉積 | 重複使用後腦部可有少量沉積，臨床意義尚不明確，依需要使用 |
| 金屬與植入物 | 依標示分 MR Safe / MR Conditional / MR Unsafe；心律調節器、人工耳蝸、金屬碎片必須事先篩檢 |
| 其他 | 噪音（需耳塞）、幽閉恐懼、掃描時間長（數十分鐘）；兒童常需鎮靜 |

## 資料分析時的注意

| 問題 | 說明 | 對策 |
| --- | --- | --- |
| 沒有絕對單位 | 訊號強度受機器、線圈、參數影響，不像 CT 的 HU | 每張影像做 z-score、histogram matching 或 WhiteStripe 等標準化 |
| 偏場 (bias field) | 線圈造成的低頻強度不均 | N4 bias field correction（SimpleITK / ANTs） |
| 多中心差異 | 1.5 T vs 3 T、不同廠牌 | ComBat 類方法校正影像特徵，或納入場地作為共變數 |
| 多序列配準 | T1、T2、FLAIR 切片位置與解析度不同 | 先 registration 到同一空間，見 [Registration](../../data-science/image-analysis/biomedical-image-analysis.md#registration-與空間轉換) |
| 腦影像 | 研究常需去頭骨 (skull stripping) 與配準到標準腦（MNI） | FSL、FreeSurfer、ANTs；資料常用 NIfTI、BIDS 目錄結構 |

相關：[X 光與 CT](x-ray-ct.md)、[PET](pet.md)（PET-MRI）、[生醫影像分析](../../data-science/image-analysis/biomedical-image-analysis.md)。
