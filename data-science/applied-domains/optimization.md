[Data Science](../README.md) › [應用領域](README.md) › 最佳化

# Optimization

作業研究 (operations research) 偏 prescriptive 的一側：問題不是「會發生什麼」，而是「在約束下應該怎麼做」。核心是把決策寫成 `decision variables + objective + constraints`，再交給 solver。

## 概觀

### 這個模組回答什麼問題

- 在容量、需求、成本與邏輯限制之下，最佳決策是什麼？
- 哪些約束是真正卡住系統的 bottleneck？
- 若需求或成本改變，最佳解會不會一起改變？

### 與其他章節的關係

- [Statistics](../statistics/README.md): 幫你判斷需求、成本、處理時間與其他輸入是否可信。
- [Machine Learning](../machine-learning/README.md): ML 常回答「會發生什麼」，OR 則接著回答「應該怎麼做」。
- [Process Analytics](process-mining.md): 若 bottleneck 已被找出，OR 常負責後續的資源配置與改善方案。

### 實務提醒

- solver 找到的最優解，只對你給進去的目標、限制與假設成立。
- 若輸入資料很不穩定，先做 sensitivity analysis，比直接追求唯一最佳解更重要。
- OR 最有價值的地方通常不是數學炫技，而是把 trade-off 說清楚。

## Optimization in Python

optimization 問的不是「資料長什麼樣」，而是「在目標與限制都明確時，哪些決策值最好」。

Key point: 一個 optimization 問題最少要拆成三件事:

- decision variables: 你可以調什麼
- objective function: 你想 maximize 或 minimize 什麼
- constraints: 哪些條件不能被違反

如果這三塊沒有先分清楚，後面的 solver 只是幫你把模糊問題算得更快。

### A Simple Mental Model

可以先把 optimization 想成:

1. 寫出一個輸入到分數的函數
2. 定義哪些輸入是可行的
3. 讓 solver 在可行範圍裡找最高分或最低分

例如:

- 最小化成本
- 最大化利潤
- 在容量、預算、時間或政策限制下找最佳組合

### Unconstrained Optimization

如果輸入值沒有額外限制，只需要對目標函數找最小值或最大值，可以先從 `scipy.optimize` 開始。

#### One Variable: `minimize_scalar()`

```python
from scipy.optimize import minimize_scalar

def objective(x):
    return x**2 - 12*x + 4

result = minimize_scalar(objective)

print(result.x)    # argmin
print(result.fun)  # minimum value
```

常看的欄位有:

- `result.x`: 最佳輸入值
- `result.fun`: 該點的目標函數值
- `result.success`: 是否成功收斂
- `result.nit`: iteration 次數
- `result.nfev`: 函數評估次數

Warning: 不要只看 `x`。若 `success=False` 或 `message` 顯示沒有正常收斂，數值結果可能不能直接相信。

#### Maximization by Negation

很多 SciPy API 預設做 minimization。若你要 maximize `f(x)`，常見做法是最小化 `-f(x)`。

```python
from scipy.optimize import minimize_scalar

def revenue(x):
    return -(x - 4)**2 + 10

result = minimize_scalar(lambda x: -revenue(x))
best_x = result.x
best_value = revenue(best_x)
```

Key point: maximize `f` 等價於 minimize `-f`。這是最常見也最容易忘的轉換。

#### Multiple Variables: `minimize()`

```python
import numpy as np
from scipy.optimize import minimize

def objective(q):
    x, y = q
    return (x - 2)**2 + (y - 3)**2

initial_guess = np.array([0.0, 0.0])
result = minimize(objective, initial_guess)

print(result.x)
```

Tip: 多變數最適化通常需要 `initial_guess`。如果目標函數不是凸的，不同起點可能會導向不同 local optimum。

### Bounds Are The First Useful Constraint

很多問題不是完全自由，而是每個變數有上下界。

```python
from scipy.optimize import minimize, Bounds

bounds = Bounds([5, 10], [25, 30])
result = minimize(objective, initial_guess, method="L-BFGS-B", bounds=bounds)
```

這很適合表達:

- 產量至少多少、至多多少
- 價格不能低於某門檻
- 投入比例要落在合法區間

Bounds 很常是從 unconstrained 問題走向 constrained 問題的第一步。

### Constrained Optimization

當限制不只是各變數自己的上下界，而是多個變數之間有聯合條件時，可以用 constraint 物件。

#### Linear Constraints

如果限制是線性的，例如:

- `x + y <= 90`
- 原料消耗不能超過容量
- 某些加總必須小於預算

可以用 `LinearConstraint`:

```python
import numpy as np
from scipy.optimize import minimize, Bounds, LinearConstraint

def profit(q):
    x, y = q
    return 3*x + 5*y

bounds = Bounds([0, 0], [90, 90])
constraint = LinearConstraint([1, 1], lb=-np.inf, ub=90)

result = minimize(
    lambda q: -profit(q),
    x0=np.array([10.0, 10.0]),
    bounds=bounds,
    constraints=constraint,
)
```

#### Nonlinear Constraints

如果可行域本身是非線性的，例如:

- `x^2 + y^2 <= 25`
- 生產、效用或風險限制不是線性關係

可以用 `NonlinearConstraint`:

```python
from scipy.optimize import NonlinearConstraint

constraint = NonlinearConstraint(lambda q: q[0] + q[1], lb=92, ub=np.inf)
```

Tip: 如果限制明明是線性的，優先用 `LinearConstraint`。這樣語意更清楚，也通常更穩。

### Convexity Changes How Much You Can Trust The Result

凸問題的好處是:

- 可行域比較容易描述
- local optimum 通常就是 global optimum
- solver 的數值結果更容易解釋

這也是為什麼很多教學會先從凸的 constrained optimization 開始。

Warning: 若問題非凸，solver 找到的可能只是某個局部最優解，而不是全域最優解。

### Linear And Mixed-Integer Programming

當 objective 與 constraints 都是線性的，而且有些變數必須是整數或 0/1，問題就會進入 LP / MILP。

SciPy 也有這類工具:

```python
from scipy.optimize import milp, Bounds, LinearConstraint

result = milp(
    c=[-5, -4],
    bounds=Bounds([0, 0], [20, 12]),
    constraints=LinearConstraint([[6, 4], [3, 1]], ub=[40, 20]),
)
```

這類模型很適合:

- 產品組合
- 資源分配
- binary open / close 決策
- facility location 與 network design

### When Nonlinear Problems Need Reformulation

不是每個真實問題都能直接交給線性工具。

有時候真正重要的技巧不是換 solver，而是先問:

- 能不能做變數替換？
- 能不能把非線性項改寫成線性形式？
- 能不能接受一個可解的近似版本？

例如若某個目標含有平方根項，原始形式可能不能直接交給線性建模工具，但透過替代變數有時可以改寫成可求解的線性或整數模型。

Key point: 很多實務 optimization 工作不是「按下 solver」，而是把原始商業問題 reformulate 成 solver 真正能理解的形式。

### SciPy vs Algebraic Modeling Tools

可以先用這個粗略分法:

| Tool direction | Better for |
| --- | --- |
| `scipy.optimize` | 連續變數、數值最適化、直接寫 Python 函數 |
| algebraic modeling tools such as `PuLP` | 線性 / 整數規劃、明確的變數索引、商業規則很多的模型 |

如果你的問題比較像:

- 寫一個數值函數，找最小值
- 少量變數、偏數值分析

那 `scipy.optimize` 通常很直接。

如果你的問題比較像:

- 產品、地點、期間都有索引
- 約束很多，而且每條都有商業語意
- 需要 binary / integer decision variables

那像 `PuLP` 這種 algebraic modeling 介面通常更好維護。

### A Practical Workflow

1. 先明確定義 decision variables。
2. 寫出 objective，確認它真的代表 business goal。
3. 把 constraints 一條條翻成數學與程式。
4. 先用小例子檢查可行域是否符合語意。
5. 再看 solver 結果、`success`、binding constraints 與 sensitivity。

如果 solver 回傳一個答案，不代表模型就對。它只代表 solver 在你給的問題描述裡找到了一個解。

### Related Notes

- [Supply Chain Optimization](#supply-chain-optimization)
- [Linear Regression](../machine-learning/supervised-learning/regression/linear.md): both involve optimization, but regression optimizes model fit while operations research optimizes a decision under explicit constraints.

## Supply Chain Optimization

supply chain analytics 常常不是先問「預測值是多少」，而是先問「在需求、容量、運輸與設施成本都存在時，系統該怎麼配置才最好」。這就是 optimization 真正切入的地方。

Key point: supply chain optimization 的本質是把 network decision 寫成 `decision variables + objective + constraints`。如果這三件事沒有分清楚，模型通常只會算出一個數字，卻沒有真的代表決策。

### What A Supply Chain Model Is Trying To Do

supply chain 不只是倉庫或貨運，而是所有和 fulfilment 有關的參與者與流程，例如:

- suppliers
- internal manufacturing
- warehouses
- outsourced logistics providers
- regional demand points or customers

optimization 要做的，不是把每個環節都模擬得很像現實，而是找出在既定約束下的最佳配置。

### Linear Programming As The Default Starting Point

這份課程的核心語言是 linear programming, LP。它之所以常用，不是因為 supply chain 問題一定線性，而是因為很多重要的第一版決策問題都能先用線性近似。

一個 LP 模型至少有三塊:

- decision variables: 我們能控制什麼
- objective function: 我們想 maximize 或 minimize 什麼
- constraints: 哪些規則、容量或邏輯不能被違反

在 supply chain 情境裡，典型對應會是:

- variables: 生產量、出貨量、是否開廠、是否開倉
- objective: 最小化總成本，或最大化總利潤
- constraints: demand fulfillment、capacity、material balance、logical rules

### Decision Variables Need A Clean Index Structure

一旦模型從單產品、單工廠走向多產品、多地點、多期間，手工寫變數通常很快失控。

這也是為什麼像 `LpVariable.dicts()` 這種 indexed variable 建立方式很重要。真正的重點不是工具本身，而是你是否清楚定義索引:

- product `p`
- time `t`
- warehouse or plant `w`
- market `j`
- facility size `s`

大多數 supply chain 模型的可維護性，往往取決於索引設計是否乾淨，而不是 solver 呼叫本身。

### Transportation Problems Are The First Useful Network Model

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

### Facility Location Adds Fixed-Cost Decisions

當模型從「既有設施怎麼分配」走到「哪些設施應該開」，問題就進一步變成 facility location。

這裡通常會同時出現兩種決策:

- continuous or integer flow variables: 送多少
- binary open / close variables: 開不開某個 plant 或倉庫

典型 trade-off 包括:

- 小型、分散設施: 較低運輸成本，但可能失去規模經濟
- 少數大型設施: 固定成本與規模效率較好，但運輸、tariff 或服務半徑可能變差

這也是 supply chain network design 常見的真實 tension: local responsiveness 與 scale efficiency 很少能同時最大化。

### Capacitated Plant Location Is A Canonical Form

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

### Constraint Design Is Where Most Modeling Errors Happen

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

### A Good Habit: Plug In A Feasible Example By Hand

在正式求解前，先拿一組小數字檢查 constraint 是否符合語意，通常非常有效。

你應該能回答:

- 如果 `B = 2`，`A` 至少該是多少？
- 如果某市場 demand 是 100，模型是否真的會要求總出貨等於 100？
- 如果某 plant closed，flow 變數是否真的被壓成 0？

這種手動 sanity check 往往比直接跑 solver 更能提早發現問題。

### Logical Constraints Are Business Rules In Algebra Form

supply chain model 很少只有容量限制，還常帶有 logical constraints，例如:

- 開了高產能廠就不能同時開低產能廠
- 沒有開設施就不能出貨
- 某些產品只能從特定倉庫配送
- 某組決策只能二選一

這些限制很重要，因為很多真實決策其實不是連續調整，而是開關式、互斥式或 conditional 的。

換句話說，logical constraints 是把 business policy 寫進模型的地方。

### Objective Functions Should Match The Real Question

模型能算，不代表算的是對的問題。

常見 objective 包括:

- minimize production + transportation cost
- minimize fixed + variable network cost
- maximize profit under capacity and demand constraints

若目標其實是 service reliability、response time 或 resilience，卻只寫成 cost minimization，模型就可能給出數學上漂亮、營運上危險的解。

Tip: objective function 不是單純 technical choice，它其實是在定義「系統認為什麼叫做好」。

### Shadow Prices Identify Which Constraints Really Matter

求解完之後，最有分析價值的往往不是最佳解本身，而是 constraints 的敏感度。

shadow price 可以先用直覺理解成:

- 某 constraint 的 right-hand side 若增加一單位
- objective value 會改善或惡化多少

在 supply chain 裡，這通常能幫你回答:

- 哪個 region 的額外 demand 最貴？
- 哪個 capacity constraint 最值得投資放寬？
- 哪些限制目前根本不是 bottleneck？

如果某 constraint 的 shadow price 很高，代表那個資源或限制在目前解附近非常稀缺。

### Sensitivity Analysis Is Not Optional

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

### Simulation Testing Helps Stress-Test The Network

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

### A Practical Modeling Workflow

一個健康的 supply chain optimization workflow 通常像這樣:

1. 先畫出 network 與 decision scope。
2. 定義索引、variables、objective 與 units。
3. 逐條寫 constraints，並用小例子驗證語意。
4. 求解後先檢查 feasibility、flows 與 open / close decisions。
5. 再看 shadow prices、binding constraints 與 slack。
6. 最後做 scenario 或 simulation testing，而不是直接把單次結果當真理。

這個節奏比「一口氣把模型寫完再交給 solver」安全很多。

### Common Failure Modes

- 把 forecast 當成精確值，沒有做 sensitivity analysis
- constraint 方向寫反，卻只看 solver 有沒有回傳 optimal
- 索引集合寫錯，導致少加總或重複加總
- 只優化 cost，卻忽略 service 或 policy requirement
- binary open / close logic 沒有和 flow 變數正確連動
- 把影子價格當成全域真理，而不是局部邊際資訊

如果 solver 回傳 `optimal`，那只是代表「在你寫的模型裡最優」，不代表「在你真正想表達的世界裡最優」。
