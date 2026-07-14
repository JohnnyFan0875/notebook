# Optimization in Python

optimization 問的不是「資料長什麼樣」，而是「在目標與限制都明確時，哪些決策值最好」。

Key point: 一個 optimization 問題最少要拆成三件事:

- decision variables: 你可以調什麼
- objective function: 你想 maximize 或 minimize 什麼
- constraints: 哪些條件不能被違反

如果這三塊沒有先分清楚，後面的 solver 只是幫你把模糊問題算得更快。

## A Simple Mental Model

可以先把 optimization 想成:

1. 寫出一個輸入到分數的函數
2. 定義哪些輸入是可行的
3. 讓 solver 在可行範圍裡找最高分或最低分

例如:

- 最小化成本
- 最大化利潤
- 在容量、預算、時間或政策限制下找最佳組合

## Unconstrained Optimization

如果輸入值沒有額外限制，只需要對目標函數找最小值或最大值，可以先從 `scipy.optimize` 開始。

### One Variable: `minimize_scalar()`

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

### Maximization by Negation

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

### Multiple Variables: `minimize()`

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

## Bounds Are The First Useful Constraint

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

## Constrained Optimization

當限制不只是各變數自己的上下界，而是多個變數之間有聯合條件時，可以用 constraint 物件。

### Linear Constraints

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

### Nonlinear Constraints

如果可行域本身是非線性的，例如:

- `x^2 + y^2 <= 25`
- 生產、效用或風險限制不是線性關係

可以用 `NonlinearConstraint`:

```python
from scipy.optimize import NonlinearConstraint

constraint = NonlinearConstraint(lambda q: q[0] + q[1], lb=92, ub=np.inf)
```

Tip: 如果限制明明是線性的，優先用 `LinearConstraint`。這樣語意更清楚，也通常更穩。

## Convexity Changes How Much You Can Trust The Result

凸問題的好處是:

- 可行域比較容易描述
- local optimum 通常就是 global optimum
- solver 的數值結果更容易解釋

這也是為什麼很多教學會先從凸的 constrained optimization 開始。

Warning: 若問題非凸，solver 找到的可能只是某個局部最優解，而不是全域最優解。

## Linear And Mixed-Integer Programming

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

## When Nonlinear Problems Need Reformulation

不是每個真實問題都能直接交給線性工具。

有時候真正重要的技巧不是換 solver，而是先問:

- 能不能做變數替換？
- 能不能把非線性項改寫成線性形式？
- 能不能接受一個可解的近似版本？

例如若某個目標含有平方根項，原始形式可能不能直接交給線性建模工具，但透過替代變數有時可以改寫成可求解的線性或整數模型。

Key point: 很多實務 optimization 工作不是「按下 solver」，而是把原始商業問題 reformulate 成 solver 真正能理解的形式。

## SciPy vs Algebraic Modeling Tools

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

## A Practical Workflow

1. 先明確定義 decision variables。
2. 寫出 objective，確認它真的代表 business goal。
3. 把 constraints 一條條翻成數學與程式。
4. 先用小例子檢查可行域是否符合語意。
5. 再看 solver 結果、`success`、binding constraints 與 sensitivity。

如果 solver 回傳一個答案，不代表模型就對。它只代表 solver 在你給的問題描述裡找到了一個解。

## Related Notes

- [Supply Chain Optimization](./supply-chain-optimization.md)
- [Linear Regression](../machine-learning/supervised-learning/regression/linear.md): both involve optimization, but regression optimizes model fit while operations research optimizes a decision under explicit constraints.
