[Data Science](../../README.md) › [應用領域](../README.md) › [Finance](README.md) › 保險與年金估值

# 保險與年金估值 (Insurance and Annuity Valuation)

保險與年金估值和一般債券最大的不同，是現金流會不會發生取決於人是否存活、何時死亡，以及契約是否有保證期或遞延條件。可以把它想成「狀態依賴的折現現金流」：折現率處理時間價值，存活 / 死亡機率決定哪些現金流真的會發生。

> 壽命表的 $p_x$、$q_x$、${{kmid}_k p_x$ 就是離散時間的存活函數與風險函數 (hazard)，見 [存活與風險函數](../../statistics/survival-analysis/survival-hazard-functions.md)；從資料估計存活曲線見 [Kaplan-Meier](../../statistics/survival-analysis/kaplan-meier.md)。

## 壽命表

| 符號 | 意義 |
| --- | --- |
| $q_x$ | 年齡 x 的人在一年內死亡的機率 |
| $p_x = 1 - q_x$ | 一年存活機率 |
| $l_x$ | 存活到年齡 x 的人數 |
| $e_x$ | 年齡 x 的剩餘預期壽命 |
| ${{kmid}_k p_x = p_x p_{x+1{kmid} \cdots p_{x+k-1{kmid}$ | 從 x 歲起存活 k 年的機率 |
| ${{kmid}_{kmid}\|{kmid} q_x = {{kmid}_k p_x \cdot q_{x+k{kmid}$ | 存活 k 年後、在下一年內死亡的機率（遞延死亡機率） |
| $v^k = (1+i)^{-k{kmid}$ | 第 k 期的折現因子 |

## 期望現值 (EPV)

年齡 x 的人未來壽命是隨機變數，估值從現值 (PV) 變成期望現值：

$$EPV = \sum_k \text{benefit{kmid}_k \cdot v^k \cdot \text{probability{kmid}_k$$

| 給付條件 | 乘上的機率 | 例子 |
| --- | --- | --- |
| 活著才付 | ${{kmid}_k p_x$ | 年金 |
| 死亡才付（死亡年度末給付） | ${{kmid}_{kmid}\|{kmid} q_x$，折現到 $v^{kmid}+1{kmid}$ | 壽險 |
| 保證給付 | 不乘機率（一般 PV） | 保證期內的年金 |

```python
import numpy as np

# qx：從年齡 x 開始的一年死亡機率向量（取自壽命表）
i = 0.03
px = 1 - qx
kpx = np.concatenate([[1.0], np.cumprod(px)[:-1]])     # k = 0, 1, 2, ... 年存活機率
kqx = kpx * qx                                         # k 年後的下一年內死亡
k = np.arange(len(qx))
v = (1 + i) ** -k

# 1. 終身期初年金（每年 1，活著才付，第一筆立即支付）
annuity_due = np.sum(1 * v * kpx)

# 2. 10 年保證 + 之後終身：保證部分用 PV，之後用 EPV
guaranteed = np.sum(v[:10])
life_part = np.sum((v * kpx)[10:])
annuity_10_certain = guaranteed + life_part

# 3. 定期壽險 20 年（死亡年度末給付 100 萬）
term = 1_000_000 * np.sum((kqx * (1 + i) ** -(k + 1))[:20])

# 4. 遞延 u 年的終身壽險：benefit 向量前 u 期為 0
u = 10
deferred = 1_000_000 * np.sum(np.where(k >= u, kqx * (1 + i) ** -(k + 1), 0))

# 5. 保費：精算等價——保費的 EPV = 給付的 EPV；保費只在活著時繳 → 本身是一筆年金
premium = term / np.sum((v * kpx)[:20])                # 20 年期每年期初繳費
```

## 產品形狀

| 產品 | benefit 向量 |
| --- | --- |
| 終身壽險 (whole life) | 每個未來期別都有死亡給付 |
| 定期壽險 (term life) | 只有前 n 期有 |
| 遞延終身壽險 | 前 u 期為 0，之後才有 |
| 終身年金 | 活著的每一期都有 |
| 保證期年金 | 前 n 期確定給付，之後活著才給 |
| 退休年金 | 退休年齡前為 0（遞延） |

真實保單常同時包含某段期間的死亡保障、某年齡後的年金與保證期。不要死背封閉公式，而是模組化：

1. 把產品拆成多個給付成分
2. 各自寫出 benefit 向量
3. 判斷每段要乘存活機率、死亡機率，還是不乘
4. 分別計算 PV / EPV 後加總

## 在保險以外的用途

這是一種一般化的建模方式：估值 = 金額 × 時點 × 狀態機率，機率可以來自人口或事件模型而非市場價格。

| 應用 | 狀態機率來自 |
| --- | --- |
| 信用商品的違約時點現金流 | 違約風險（PD 期限結構） |
| 顧客終身價值 (CLV) | 流失 / 留存模型 |
| 醫療利用與退休金負債推估 | 存活與疾病轉移機率 |
| 衛生經濟的成本效益分析 | 疾病狀態轉移（Markov 模型）、QALY 折現 |

R 寫法相同：從壽命表取 `qx`、`px`，`cumprod()` 算存活機率，`rep()` / `c()` 定義 benefit 向量，`sum(benefits * discount_factors * probabilities)` 算 EPV。重要的不是語法，而是把契約條件翻成正確的向量。

## 常見錯誤

| 錯誤 | 檢查 |
| --- | --- |
| 保證現金流與條件現金流混在一起 | 分開計算後相加 |
| 存活機率與遞延死亡機率用錯 | 活著才付用 ${{kmid}_k p_x$，死亡才付用 ${{kmid}_{kmid}\|{kmid} q_x$ |
| 折現期數錯位一格 | 期初 vs 期末、死亡年度末給付多折一期 |
| 給付起訖時點沒對齊 | 遞延期、保證期的邊界 |
| 只看期望值 | 結果高度依賴壽命表與利率假設；做敏感度分析，且壽命表會隨世代改善（長壽風險） |

估值結果怪怪的，先檢查現金流時點與機率的對齊，而不是公式。
