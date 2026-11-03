[基因體學](../README.md) › [癌症基因體](README.md) › 腫瘤臨床終點

# 腫瘤臨床終點 (Oncology Clinical Endpoints)

評估治療或生物標記（突變、ctDNA、PRS）的臨床價值時，要先講清楚「結果」是什麼。終點的種類決定了資料結構與統計方法：時間到事件用存活分析，反應率用比例與邏輯斯迴歸。

## 終點總表

| 終點 | 全名 | 事件 / 定義 | 起點 | 資料型態 |
| --- | --- | --- | --- | --- |
| OS | Overall survival，整體存活 | 任何原因死亡 | 隨機分派 / 診斷 / 治療開始 | 時間到事件 |
| PFS | Progression-free survival，無惡化存活 | 疾病惡化或死亡，先發生者 | 隨機分派 / 治療開始 | 時間到事件 |
| DFS | Disease-free survival，無病存活 | 復發、新原發癌或死亡（依試驗定義） | 根治性治療（手術）後 | 時間到事件 |
| RFS | Recurrence-free survival，無復發存活 | 復發或死亡；是否含新原發癌依試驗而異 | 根治性治療後 | 時間到事件 |
| EFS | Event-free survival，無事件存活 | 惡化而無法手術、復發或死亡等預先定義事件 | 隨機分派（常用於術前治療試驗） | 時間到事件 |
| TTP | Time to progression | 只計惡化，死亡視為設限 | 治療開始 | 時間到事件 |
| ORR | Objective response rate，客觀反應率 | CR + PR 的比例（依 RECIST） | — | 二元 / 比例 |
| DCR | Disease control rate | CR + PR + SD 的比例 | — | 二元 / 比例 |
| DoR | Duration of response | 從達到反應到惡化或死亡 | 首次 CR / PR | 時間到事件（只在反應者中） |
| pCR | Pathological complete response，病理完全反應 | 術前治療後手術標本無殘存侵襲性癌（乳癌常用 ypT0/Tis ypN0） | — | 二元 |

> DFS、RFS、EFS 的事件定義在不同試驗間並不一致（例如是否計入新原發癌、非癌症死亡）；跨研究比較前先讀試驗的定義。乳癌輔助治療試驗可參考 STEEP 標準化定義。

## RECIST 1.1：反應怎麼判定

實體腫瘤以影像量測目標病灶的**最長徑總和**判定反應：

| 反應 | 條件 |
| --- | --- |
| CR（完全反應） | 所有目標病灶消失；淋巴結短徑 < 10 mm |
| PR（部分反應） | 總和比基線減少 ≥ 30% |
| PD（疾病惡化） | 總和比**最低點 (nadir)** 增加 ≥ 20% 且絕對值增加 ≥ 5 mm，或出現新病灶 |
| SD（疾病穩定） | 介於 PR 與 PD 之間 |

免疫治療可能出現先變大再縮小的假性惡化 (pseudoprogression)，因此另有 iRECIST，需再次影像確認惡化。影像模態見 [醫學影像](../../medical-imaging/README.md)。

## 終點比較

| 終點 | 優點 | 限制 |
| --- | --- | --- |
| OS | 客觀、臨床意義最明確 | 需要長追蹤、大樣本；受後續治療與交叉治療 (crossover) 稀釋 |
| PFS / DFS / EFS | 比 OS 早出結果、不受後續治療影響 | 影像評估時程與判讀者會造成偏差（常用獨立中央判讀 BICR）；不一定轉換成 OS 獲益 |
| ORR | 單臂試驗即可評估、反應快 | 不等於存活獲益；需搭配 DoR |
| pCR | 術前治療後數月就有結果 | 個人層級與預後相關，但試驗層級的 pCR 提升不一定轉換成 EFS / OS 獲益（Cortazar et al., *Lancet* 2014） |

> PFS、DFS、pCR、ORR 常作為 OS 的**替代終點 (surrogate endpoint)**；替代終點要在「試驗層級」證實能預測 OS 改善，才算有效。

## 統計方法

| 終點類型 | 描述 | 比較 / 調整 | 筆記 |
| --- | --- | --- | --- |
| OS、PFS、DFS、EFS、DoR | Kaplan-Meier 曲線、中位存活時間 | log-rank 檢定、Cox 迴歸 → HR | [Kaplan-Meier](../../../data-science/statistics/survival-analysis/kaplan-meier.md)、[log-rank](../../../data-science/statistics/survival-analysis/log-rank-test.md)、[Cox 模型](../../../data-science/statistics/survival-analysis/cox-ph-model.md) |
| ORR、DCR、pCR | 比例 + 95% CI | 卡方 / Fisher 檢定、邏輯斯迴歸 → OR | [邏輯斯迴歸](../../../data-science/statistics/regression-analysis/logistic-regression.md) |
| 設限與競爭風險 | 失去追蹤、非癌症死亡 | 設限處理、Fine-Gray | [核心概念與設限](../../../data-science/statistics/survival-analysis/core-concepts.md) |

| 常見陷阱 | 說明 | 對策 |
| --- | --- | --- |
| 依反應分組比較 OS | 反應者必須先活到被評估反應（immortal time bias），存活自然較長 | 地標分析 (landmark analysis) 或把反應當時間相依變數 |
| 中位追蹤時間太短 | KM 尾端只剩少數人，中位數不穩 | 報告中位追蹤時間與各時間點的 at-risk 人數 |
| 混用定義 | 不同研究的 DFS 事件定義不同 | 統一定義後再比較或做統合分析 |

基因變異與這些終點的分析設計（遺傳模型、病例–對照 vs 世代）見 [研究設計：基因變異與臨床終點分析](../../../data-science/statistics/experimental-design/designs.md#三基因變異與臨床終點分析)；以 ctDNA / MRD 作為早期反應指標見 [液態切片](../sequencing-techniques/liquid-biopsy.md)。
