[Data Science](../README.md) › [應用領域](README.md) › 行銷反應與選擇模型

# 行銷反應與選擇模型 (Marketing Response and Choice Models)

行銷情境的資料建模：價格、促銷、陳列等**可操作的槓桿**如何改變銷量或購買機率（market response），在多個選項間怎麼取捨（choice model），以及一個 campaign 到底有沒有效（campaign measurement）。可遷移的方法：log-linear 模型與 GLM、多項 logit、邊際效應、[A/B 測試](../statistics/experimental-design/ab-testing.md)。生醫中對應的是病人偏好的離散選擇實驗 (discrete choice experiment, DCE) 與治療選擇分析。

> 行銷反應資料多半是觀察性的：模型係數不等於因果效果 (causal lift)。價格、促銷與陳列常一起變動，單看一個係數很容易誤解。

## Market Response Models

| 層級 | 單位 | 問題 | 模型 |
| --- | --- | --- | --- |
| 彙總銷量 | 週 × 店 × SKU、campaign 期間 | 銷量如何隨價格與促銷變動？ | 迴歸（log-linear） |
| 個體選擇 | 顧客、家戶的一次購買機會 | 這次會不會買？會選哪個品牌？ | logistic / probit、choice model |

### 彙總銷量：log-linear 模型

```python
import numpy as np
import statsmodels.formula.api as smf

df["price_lag1"] = df.groupby("store")["price"].shift(1)       # 結轉效果：依店分組再 shift
df["coupon_lag1"] = df.groupby("store")["coupon"].shift(1)

model = smf.ols("np.log(sales) ~ np.log(price) + display * coupon + price_lag1 + coupon_lag1",
                data=df).fit(cov_type="cluster", cov_kwds={"groups": df["store"]})
model.summary()
np.exp(model.params["display"]) - 1        # display 對銷量的比例變化
```

| 設計 | 理由 | 解讀 |
| --- | --- | --- |
| 銷量取 log | 右偏、變異大；乘法效果變成加法 | dummy 係數 β → 銷量變化 `exp(β) − 1`（β 小時 ≈ β） |
| 價格也取 log（log-log） | 係數直接是價格彈性 | 價格上漲 1%，銷量變化 β% |
| 交互作用 `display * coupon` | 促銷工具會互相放大或替代 | 沒有交互作用時，效果會被錯分到別的變數 |
| 落後項 (lag) | 促銷殘留記憶、囤貨後需求下滑、價格反應延遲 | 只有在資料頻率與行為機制相符時才有意義；日、週、月資料的結轉不能混用 |
| 依店分群的標準誤 | 同一店的週資料不獨立 | 否則標準誤低估 |

> `log(sales)` 不能處理 0 銷量；有很多 0 時改用 Poisson / 負二項 GLM（`smf.glm(..., family=sm.families.Poisson())`），係數同樣以 `exp(β)` 解讀為比例變化，見 [計數迴歸](../statistics/regression-analysis/README.md)。

### 個體選擇：二元反應

```text
Pr(purchase = 1) = f(price, promotion, competition)
```

| 模型 | 特性 |
| --- | --- |
| 線性機率模型 (LPM) | 係數直接是機率變化；但預測可能超出 0–1，價格反應被迫是直線 |
| Logistic | log-odds 解讀、odds ratio、與 ML 分類流程相容 |
| Probit | 潛在效用 (latent utility) 敘事較自然，與部分 choice model 傳統一致 |

logistic 與 probit 通常給出相近的預測機率；它們描述的是「刺激增加時購買機率如何平滑變化、在哪一段最敏感」的反應曲線，不只是分類器。競品情境下用**相對價格**（`np.log(price_a / price_b)`）通常比分別放兩個原始價格更貼近消費者的決策。

### 邊際效應比係數更接近決策語言

非線性模型中係數不等於機率變化。管理者想知道的是「相對價格上升 1%，購買機率下降多少百分點？」「開啟陳列，機率上升 1 個還是 10 個百分點？」

```python
logit = smf.logit("purchase ~ price_ratio + display + coupon", data=df).fit()
logit.get_margeff(at="overall").summary()     # average marginal effects (AME)
```

### 模型選擇

| 工具 | 用途 |
| --- | --- |
| 巢狀模型比較（likelihood ratio test）、AIC | 配適與精簡的取捨 |
| ROC / AUC | 二元反應的區辨力 |
| 預測機率曲線 | 檢查反應形狀是否合理 |
| 時間外驗證（新的促銷期間） | 能否外推 |

不要只因 AIC 稍低就採用：還要問係數方向是否合理、交互作用是否有業務意義、落後項是否只是吸收雜訊。逐步回歸 (stepwise) 會讓 p 值與信賴區間失真。

| 常見錯誤 | |
| --- | --- |
| 把 log-sales 係數當成絕對單位變化 | 忽略促銷交互作用，效果被平均掉 |
| 用二元模型的原始係數解釋機率改變 | 只看自家價格，不看相對價格 |
| 加入落後項卻沒確認資料頻率與機制 | 把觀察性係數當成因果 lift |

## Choice Modeling

choice model 處理「在一組選項中選哪一個」：不只是會不會買，而是多個候選方案之間怎麼取捨，描述**選項的相對吸引力**如何隨價格、特徵、通路或陳列改變。

| 問題 | 框架 |
| --- | --- |
| 顧客會不會買任一商品？ | 二元反應 |
| 顧客會在三台車、五個方案、十個品牌裡選哪個？ | choice model |
| 病人會選手術、藥物還是觀察等待？ | choice model（DCE） |

### 效用與多項 logit

每個選項 j 有潛在效用 `U_j = V_j + ε_j`，V 是可觀測特徵（價格、座位數、變速箱、是否敞篷；療效、副作用風險、費用、給藥方式）的線性組合。ε 服從 Gumbel 分布時得到多項 logit：

$$P(\text{choose } j) = \frac{e^{V_j}}{\sum_k e^{V_k}}$$

二元 logistic 是只有兩個選項的特例。

| 資料格式 | 結構 | 用途 |
| --- | --- | --- |
| Wide | 每題或每選項一組欄位 | 問卷原始匯出 |
| Long | 每列一個「受訪者 × 題目 × 選項」組合，含 `chosen` 0/1 | 建模（conditional / multinomial / mixed logit） |

```python
# long 格式：resp_id, task_id, alt_id, chosen, price, seats, convertible
import statsmodels.api as sm
# conditional logit：同一題（task）內比較選項
from statsmodels.discrete.conditional_models import ConditionalLogit
X = long[["price", "seats", "convertible"]]
res = ConditionalLogit(long["chosen"], X, groups=long["task_uid"]).fit()
res.params                                   # 每個屬性對效用的貢獻
-res.params["seats"] / res.params["price"]   # 願付價格 (WTP)：多一個座位值多少錢
```

R 中常用 `mlogit`、`logitr`；階層貝氏模型用 `ChoiceModelR` 或 Stan。

### 市占模擬 (Share Simulation)

choice model 最實用的產出是 what-if 模擬：

```python
V = X_new @ res.params                      # 每個候選產品的效用
share = np.exp(V) / np.exp(V).sum()         # 預測市占
```

可以回答：新產品價格提高，市占掉多少？加上某特徵能否補回價格劣勢？哪個設計組合的市占最大？

### 陳述 vs 顯示偏好

| 資料 | 捕捉 | 優點 | 風險 |
| --- | --- | --- | --- |
| 陳述偏好 (stated preference；conjoint、DCE 問卷) | 人們說會選什麼 | 上市前測試尚不存在的產品或屬性組合 | 假設偏差 (hypothetical bias)：說會選不保證真的買 |
| 顯示偏好 (revealed preference；交易紀錄) | 人們實際選了什麼 | 接近真實經濟行為 | 只限於實際存在過的選項 |

### IIA 與異質性

多項 logit 假設 IIA（independence of irrelevant alternatives）：兩選項的相對機率不因加入第三個選項而改變。加入一個和 A 幾乎相同的 A′ 時，現實中 A′ 主要搶 A 的市占，但 MNL 會讓它按比例從所有選項搶，替代模式不自然。

| 延伸 | 處理 |
| --- | --- |
| Nested logit | 相似選項放在同一巢內，巢內替代較強 |
| Mixed logit / random coefficients | 價格敏感度等係數因人而異 |
| 階層貝氏 choice model | 個體層級偏好，小樣本也能估 |
| 分群交互作用（價格 × segment） | 不同市場區隔的敏感度不同 |

延伸模型的替代模式更有彈性、保留個體差異，代價是較難估計、計算成本高、對資料量與實驗設計要求較高。

| 常見錯誤 | |
| --- | --- |
| 把多選項問題硬塞回二元分類 | 只有受訪者欄位，沒有選項層級屬性 |
| 把陳述偏好結果當成真實銷量 | 只看係數顯著，不做市占模擬 |
| 忽略族群異質性 | 把全體平均偏好當成每個人的偏好 |

## Campaign Measurement

衡量一個行銷活動是否產生想要的商業效果，以及效果在通路、漏斗階段、目標族群與戰術層級怎麼拆解。先回答問題（假期活動有沒有提升新客？新戰術在這個通路是否優於其他？延長一個月 ROI 會怎樣？），並記錄活動目標、目標族群、範圍內的通路與戰術、漏斗階段、最終要回到哪個商業結果，見 [形成分析問題](../data-communication/forming-analytical-questions.md)。

### KPI vs 輔助指標

| 層 | 用途 | 例子 |
| --- | --- | --- |
| KPI（商業健康） | 判斷是否真的影響業務 | ROI、LTV、新客數、留存、合格轉換 |
| 輔助指標（行銷健康） | 監控執行與最佳化 | CPC、CTR、互動率、開信率、頻次、預算消耗進度 |

> 每個活動最好只有 1–2 個主要 KPI；輔助指標可以很多，但不能取代 KPI。只看 CTR、互動率會把「通路很活躍」誤當成「活動成功」。

### 漏斗階段決定指標

| 階段 | 目標 | 常見通路 | 指標 |
| --- | --- | --- | --- |
| 知名度 (awareness) | 品牌曝光 | 電視、戶外、廣泛觸及的展示廣告 | 觸及、曝光、輔助認知度 |
| 考慮 (consideration) | 進入購買候選 | 社群、展示、研究型接觸點 | 互動、網站造訪、品牌搜尋提升 |
| 決策 (decision) | 實際轉換 | 付費搜尋、再行銷、直效通路 | 轉換、CAC、營收、合格名單 |

不要用下層漏斗的轉換 KPI 否定上層活動的價值，也不要用知名度指標假裝回答了 ROI。

### 歸因不等於因果

數位通路有細的使用者層級事件；線下通路多只有彙總報表；跨通路的身分串接通常不完整。可觀測的接觸點不等於完整的顧客旅程。

歸因 (attribution) 是**功勞分配**：轉換的功勞要分給哪個接觸點。它在營運上有用，但不是乾淨的因果估計：

| 偏差來源 | 說明 |
| --- | --- |
| 位置 | 某些通路靠近轉換只是因為它們在旅程尾端（last-click 偏差） |
| 角色 | 知名度通路本來就拿不到 last-click 功勞 |
| 意圖 | 曝光與使用者原本的購買意圖高度相關（搜尋品牌關鍵字的人本來就要買） |

### 活動生命週期

| 階段 | 工作 |
| --- | --- |
| 活動前 | 定義族群、選通路、設 KPI 目標（用預測模型或歷史基準） |
| 活動中 | 監控預算進度、KPI vs 目標、通路健康 |
| 活動後 | 評估 ROI、整理跨通路趨勢、記錄要重複 / 停止 / 重新設計的部分 |

> 最常見的失敗之一：開跑前沒有目標，結束後才挑指標做事後解釋。

| 問題 | 方法 |
| --- | --- |
| 誰該收到活動？ | 族群分群（地區、生命週期階段、年齡、產品組合），見 [Clustering](../machine-learning/unsupervised-learning/clustering/README.md) |
| 哪些族群最可能因優惠而購買？ | 反應模型；要估「因為優惠才買」的人，用 uplift model |
| 哪種訊息、優惠設計最有吸引力？ | choice model |
| 能否因果檢驗？ | 實驗；不可行時用準實驗 |

### A/B 測試不可行時

整合性活動常因成本、通路控制權有限、曝光單位難以隨機化、溢出效應或品牌效應強而無法做 A/B 測試。替代方案（由強到弱）：地區層級隨機化 (geo experiment) → 差異中的差異 (difference-in-differences)、合成控制 (synthetic control) → 配對比較 → 有強烈保留的前後比較；也可以用反應 / 選擇模型做模擬。行銷世界裡，能不能衡量本身就是設計的一部分，見 [Experimental Design](../statistics/experimental-design/README.md)。

| 常見錯誤 | |
| --- | --- |
| 把輔助指標當最終成功指標 | 不區分漏斗階段的衡量邏輯 |
| 把歸因結果當因果事實 | 沒有活動前目標 |
| 只看單一通路 | 忽略整合活動的跨通路交互作用 |

相關筆記：[Logistic Regression](../statistics/regression-analysis/logistic-regression.md)、[門檻與校準](../machine-learning/evaluation/classification-thresholds-and-calibration.md)、[ROC / AUC](../machine-learning/evaluation/roc-auc.md)。
