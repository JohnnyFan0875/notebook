# Campaign Measurement

campaign measurement 處理的是「一個 marketing campaign 到底有沒有產生想要的商業效果」，以及這個效果應該如何被拆成 channel、funnel stage、target audience 與 tactic 層級來看。

Key point: marketing measurement 不是蒐集越多 metrics 越好，而是要先分清楚哪些是 **business-impact KPI**，哪些只是 **supporting metrics**，否則團隊很容易優化了一堆 activity signal，卻沒有真的改善業務結果。

## Marketing Analytics Starts With The Question

Marketing analytics 問題通常不是抽象的「數據告訴我什麼」，而是像這些具體決策：

- 這次 holiday campaign 有沒有提升 acquisition？
- 某個新 tactic 在這個 channel 裡有沒有優於其他 tactic？
- 如果 campaign 延長一個月，預期 ROI 會怎麼變？
- 某個國家增加 spend，是否真的改善該 channel 的結果？

這類問題很適合先回到 [Forming Analytical Questions](../data-communication/forming-analytical-questions.md) 的框架，但 marketing 場景通常還要再補上：

- campaign goal 是什麼
- target audience 是誰
- 哪個 channel 或 tactic 在 scope 內
- funnel stage 在哪裡
- 成功最後要回到哪個 business outcome

## KPI And Supporting Metrics Are Not The Same Thing

在 campaign measurement 裡，很重要的一個分層是：

- **KPI**: 用來看 marketing 是否真的影響 business
- **supporting metric**: 用來監控 tactic 或 channel health

典型差異：

| Layer | What It Is For | Examples |
| --- | --- | --- |
| KPI | judge business impact | ROI, LTV, acquisition, retention, qualified conversions |
| Supporting metric | monitor execution and optimization | CPC, CTR, engagement rate, open rate, frequency, pacing |

Practical rule:

- 每個 campaign 最好只有 `1-2` 個主 KPI
- supporting metrics 可以有很多，但它們不該取代 KPI

Warning: 如果團隊只看 click-through rate、engagement rate 或 open rate，常會把「channel 活躍」誤當成「campaign 成功」。

## Common KPI Themes In Marketing

高層常會把 marketing metrics 粗分成兩類：

- **business health**
- **marketing health**

Business health 常見指標：

- ROI
- LTV
- overall acquisition
- overall retention

Marketing health 常見指標：

- acquisition cost
- cost per click
- conversion rate
- engagement rate

Key point: 這兩類都重要，但回答的問題不同。Business health 問的是「有沒有產生真正價值」，marketing health 問的是「執行過程是否健康」。

## Funnel Stage Should Drive Metric Choice

同一個 campaign，如果在不同 funnel stage，衡量方式也應該不同。

常見三層 funnel：

- **awareness / upper funnel**: 讓更多人知道品牌
- **consideration / mid funnel**: 讓品牌進入購買候選集合
- **decision / lower funnel**: 推動實際轉換或購買

對應的 channel 與衡量直覺通常不同：

| Funnel Stage | Main Goal | Common Channels | Example Metrics |
| --- | --- | --- | --- |
| Awareness | brand exposure | TV, billboard, broad-reach display | reach, impressions, aided awareness |
| Consideration | brand evaluation | social, display, research-touch channels | engagement, site visits, branded search lift |
| Decision | direct conversion | paid search, retargeting, direct response channels | conversion, CAC, revenue, qualified leads |

Tip: 不要用 lower-funnel conversion KPI 去否定 upper-funnel activity 的價值，但也不要用 awareness metrics 假裝自己回答了 ROI 問題。

## Channel Measurement Is About Access And Observability

不同 marketing channels 的 measurement 條件不一樣。

常見差異包括：

- digital channels 通常有更細的 user-level event data
- offline channels 常較依賴 aggregated reporting
- some channels are direct, others depend on platforms or partners
- identity stitching across channels is often incomplete

這會直接影響你能不能做：

- user-level attribution
- cross-channel path analysis
- clean incremental lift evaluation

Warning: 可觀測到的 channel touchpoint 不等於完整 customer journey。measurement design 必須承認這個限制。

## Attribution Is About Credit Assignment, Not Causality By Default

當團隊問「哪個 channel 帶來轉換」時，常常其實是在問 attribution。

attribution 的核心是：

- conversion credit 要分給哪個 touchpoint
- 在 multi-channel path 下，各 channel 貢獻如何分配

但 attribution 不是自動等於 causal effect，因為：

- 某些 channel 更接近最後轉換，只是因為它們出現在旅程尾端
- 某些 channel 主要做 awareness，本來就不會拿到 last-click credit
- channel exposure 與 user intent 常常高度共變

Key point: attribution is a credit-assignment framework. It is useful operationally, but it is not the same thing as a clean causal estimate.

## Integrated Campaigns Need A Lifecycle View

integrated campaigns 通常跨多個 channels、tactics 與 funnel stages，所以不該只在 campaign 結束後看一張 summary table。

一個更實務的 lifecycle 會是：

1. **before campaign**
   - define audience
   - choose channels
   - set KPI targets
   - use predictive modeling or historical benchmarks
2. **during campaign**
   - monitor pacing
   - watch KPI vs target
   - track channel health and execution issues
3. **after campaign**
   - evaluate ROI
   - summarize cross-channel trends
   - document what to repeat, stop, or redesign

Tip: campaign measurement 最常見的失敗之一，是 campaign 開跑前沒有 target，結束後才用臨時選的 metrics 做事後解釋。

## Marketing Models Plug Into Different Campaign Questions

Campaign planning 常會連到不同分析方法：

- **audience segmentation**
  - who should receive the campaign?
  - geography, lifecycle stage, age group, product set
- **response models**
  - which segments are most likely to purchase given an offer?
  - best for discount or offer response probability
- **choice models**
  - what message, offer design, or value proposition is most attractive?
  - best for alternative comparison and share simulation
- **experimentation**
  - can we test this campaign causally?
  - if not, what observational or causal-inference alternative is realistic?

這個 mapping 很重要，因為很多團隊其實不是缺模型，而是把問題丟到錯的方法上。

## A/B Testing Is Not Always Operationally Feasible

對 integrated marketing campaign，A/B testing 不一定總是能做，原因可能包括：

- 成本太高
- channel 控制權有限
- 曝光單位難以乾淨隨機化
- spillover 或 brand effects 很強

這時候仍然可以做比較成熟的 measurement：

- pre/post with strong caveats
- matched comparisons
- quasi-experimental design
- causal inference models
- simulation based on response / choice models

這不是說 experiment 不重要，而是要承認：在 marketing 世界，measurement feasibility 本身就是設計的一部分。

## A Practical Workflow

1. 先定義 campaign goal 與 funnel stage。
2. 為每個 campaign 設定 `1-2` 個主 KPI。
3. 再補 supporting metrics 來監控 channel health。
4. 明確記錄 audience、channels、geographies 與 time window。
5. 依問題選 segmentation、response model、choice model 或 experimentation。
6. 在 campaign 中持續看 pacing，而不是等結束才分析。
7. campaign 後回到 ROI、retention, acquisition 或 LTV 層級驗證是否真的有 business impact。

## Common Mistakes

- 把 supporting metrics 當成 campaign 的最終成功指標。
- 不區分 awareness、consideration、decision 的不同衡量邏輯。
- 把 attribution 結果直接當成 causal truth。
- 沒有 pre-campaign target，導致 post-campaign 評估失焦。
- 只看單一 channel，忽略 integrated campaign 的 cross-channel interaction。

## Related Topics

- [Market Response Models](market-response-models.md)
- [Choice Modeling](choice-modeling.md)
- [A/B Testing](../statistics/experimental-design/ab-testing.md)
- [Forming Analytical Questions](../data-communication/forming-analytical-questions.md)
