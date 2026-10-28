# Supply Chain Optimization

supply chain analytics 常常不是先問「預測值是多少」，而是先問「在需求、容量、運輸與設施成本都存在時，系統該怎麼配置才最好」。這就是 optimization 真正切入的地方。

Key point: supply chain optimization 的本質是把 network decision 寫成 `decision variables + objective + constraints`。如果這三件事沒有分清楚，模型通常只會算出一個數字，卻沒有真的代表決策。

## What A Supply Chain Model Is Trying To Do

supply chain 不只是倉庫或貨運，而是所有和 fulfilment 有關的參與者與流程，例如:

- suppliers
- internal manufacturing
- warehouses
- outsourced logistics providers
- regional demand points or customers

optimization 要做的，不是把每個環節都模擬得很像現實，而是找出在既定約束下的最佳配置。

## Linear Programming As The Default Starting Point

這份課程的核心語言是 linear programming, LP。它之所以常用，不是因為 supply chain 問題一定線性，而是因為很多重要的第一版決策問題都能先用線性近似。

一個 LP 模型至少有三塊:

- decision variables: 我們能控制什麼
- objective function: 我們想 maximize 或 minimize 什麼
- constraints: 哪些規則、容量或邏輯不能被違反

在 supply chain 情境裡，典型對應會是:

- variables: 生產量、出貨量、是否開廠、是否開倉
- objective: 最小化總成本，或最大化總利潤
- constraints: demand fulfillment、capacity、material balance、logical rules

## Decision Variables Need A Clean Index Structure

一旦模型從單產品、單工廠走向多產品、多地點、多期間，手工寫變數通常很快失控。

這也是為什麼像 `LpVariable.dicts()` 這種 indexed variable 建立方式很重要。真正的重點不是工具本身，而是你是否清楚定義索引:

- product `p`
- time `t`
- warehouse or plant `w`
- market `j`
- facility size `s`

大多數 supply chain 模型的可維護性，往往取決於索引設計是否乾淨，而不是 solver 呼叫本身。

## Transportation Problems Are The First Useful Network Model

最基本的 network optimization 通常是 transportation problem。

典型問題長這樣:

- 幾個 warehouses 或 plants
- 幾個 customers 或 regions
- 每條 route 有不同運輸成本
- 需求必須被滿足
- 每個供給點有出貨上限

這種模型的核心不是路徑圖，而是 allocation:

- 每個供給點應該送多少到每個需求點？
- 要如何在滿足需求下，把總運輸成本降到最低？

這是很多更大 network design 問題的起點。

## Facility Location Adds Fixed-Cost Decisions

當模型從「既有設施怎麼分配」走到「哪些設施應該開」，問題就進一步變成 facility location。

這裡通常會同時出現兩種決策:

- continuous or integer flow variables: 送多少
- binary open / close variables: 開不開某個 plant 或倉庫

典型 trade-off 包括:

- 小型、分散設施: 較低運輸成本，但可能失去規模經濟
- 少數大型設施: 固定成本與規模效率較好，但運輸、tariff 或服務半徑可能變差

這也是 supply chain network design 常見的真實 tension: local responsiveness 與 scale efficiency 很少能同時最大化。

## Capacitated Plant Location Is A Canonical Form

這份材料反覆出現的一個重要模型，是 capacitated plant location model。

它通常同時包含:

- 哪些地點開廠
- 開 low-capacity 還是 high-capacity 版本
- 各市場需求由哪些廠供應
- 每個廠的總出貨不能超過 capacity

這類模型非常適合用來練習如何把商業語句翻成數學限制，例如:

- 每個市場需求必須完全被滿足
- 若某 plant 沒有被打開，就不能出貨
- 某 plant 若選 high-capacity，就不應同時再選 low-capacity

這些都不是「額外細節」，而是模型是否忠於決策邏輯的關鍵。

## Constraint Design Is Where Most Modeling Errors Happen

很多 optimization 錯誤不在 objective，而在 constraint。

這份課程很有價值的一點，是它強調常見 constraint mistake，例如:

- dependent demand relation 方向寫反
- 用 `=` 寫死本來應該是 `>=` 或 `<=` 的限制
- 多維索引的加總範圍漏掉一層
- 把 logical condition 寫成數學上可解、但商業上不合理的式子

例如如果每單位 `B` 需要至少 3 單位 `A` 作為投入，重點不是只會寫公式，而是知道:

- 「至少」代表不一定要剛好等於
- 方向和單位必須一致
- 代入具體數值檢查，通常比盯著公式更容易抓錯

## A Good Habit: Plug In A Feasible Example By Hand

在正式求解前，先拿一組小數字檢查 constraint 是否符合語意，通常非常有效。

你應該能回答:

- 如果 `B = 2`，`A` 至少該是多少？
- 如果某市場 demand 是 100，模型是否真的會要求總出貨等於 100？
- 如果某 plant closed，flow 變數是否真的被壓成 0？

這種手動 sanity check 往往比直接跑 solver 更能提早發現問題。

## Logical Constraints Are Business Rules In Algebra Form

supply chain model 很少只有容量限制，還常帶有 logical constraints，例如:

- 開了高產能廠就不能同時開低產能廠
- 沒有開設施就不能出貨
- 某些產品只能從特定倉庫配送
- 某組決策只能二選一

這些限制很重要，因為很多真實決策其實不是連續調整，而是開關式、互斥式或 conditional 的。

換句話說，logical constraints 是把 business policy 寫進模型的地方。

## Objective Functions Should Match The Real Question

模型能算，不代表算的是對的問題。

常見 objective 包括:

- minimize production + transportation cost
- minimize fixed + variable network cost
- maximize profit under capacity and demand constraints

若目標其實是 service reliability、response time 或 resilience，卻只寫成 cost minimization，模型就可能給出數學上漂亮、營運上危險的解。

Tip: objective function 不是單純 technical choice，它其實是在定義「系統認為什麼叫做好」。

## Shadow Prices Identify Which Constraints Really Matter

求解完之後，最有分析價值的往往不是最佳解本身，而是 constraints 的敏感度。

shadow price 可以先用直覺理解成:

- 某 constraint 的 right-hand side 若增加一單位
- objective value 會改善或惡化多少

在 supply chain 裡，這通常能幫你回答:

- 哪個 region 的額外 demand 最貴？
- 哪個 capacity constraint 最值得投資放寬？
- 哪些限制目前根本不是 bottleneck？

如果某 constraint 的 shadow price 很高，代表那個資源或限制在目前解附近非常稀缺。

## Sensitivity Analysis Is Not Optional

很多供應鏈模型的輸入本來就是 estimate，不是 certainty，例如:

- regional demand forecast
- transportation cost
- fixed facility cost
- usable capacity

因此一個單點最佳解通常不夠，還要再問:

- demand 增加時，產能配置會不會改？
- 成本小幅變動時，開廠決策會不會翻轉？
- 哪些 plant 仍有 slack capacity 可以吸收未來需求？

這也是為什麼 shadow price analysis 和 scenario testing 幾乎是同一條工作流上的下一步。

## Simulation Testing Helps Stress-Test The Network

這份內容最後把 simulation 接進 optimization，這很實用。

核心想法是:

- 先有一個 deterministic optimization model
- 再對 demand 或 cost 加入隨機擾動
- 重複求解，觀察決策與成本如何變動

這樣做的目的不是把模型變華麗，而是檢查:

- 最佳解是否穩定
- 哪些地區或設施最容易受擾動影響
- 單一最優解是否其實非常脆弱

當 deterministic optimum 對小幅輸入變動就非常敏感時，通常代表模型需要更多 robustness thinking。

## A Practical Modeling Workflow

一個健康的 supply chain optimization workflow 通常像這樣:

1. 先畫出 network 與 decision scope。
2. 定義索引、variables、objective 與 units。
3. 逐條寫 constraints，並用小例子驗證語意。
4. 求解後先檢查 feasibility、flows 與 open / close decisions。
5. 再看 shadow prices、binding constraints 與 slack。
6. 最後做 scenario 或 simulation testing，而不是直接把單次結果當真理。

這個節奏比「一口氣把模型寫完再交給 solver」安全很多。

## Common Failure Modes

- 把 forecast 當成精確值，沒有做 sensitivity analysis
- constraint 方向寫反，卻只看 solver 有沒有回傳 optimal
- 索引集合寫錯，導致少加總或重複加總
- 只優化 cost，卻忽略 service 或 policy requirement
- binary open / close logic 沒有和 flow 變數正確連動
- 把影子價格當成全域真理，而不是局部邊際資訊

如果 solver 回傳 `optimal`，那只是代表「在你寫的模型裡最優」，不代表「在你真正想表達的世界裡最優」。
