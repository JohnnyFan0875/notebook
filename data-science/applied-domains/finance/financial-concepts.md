[Data Science](../../README.md) › [應用領域](../README.md) › [Finance](README.md) › 金融基本概念

# 金融基本概念 (Financial Concepts)

很多金融問題的骨架是同一套：時間 (time)、現金流 (cash flow)、利率 (rate) 如何一起作用。本篇依序是貨幣時間價值、債券估值與利率風險、金融資料特有的清理問題。一般的 CSV / dtype / 日期處理見 [匯入資料](../../python-foundations/importing-data.md)、[Datetime](../../python-foundations/datetime.md)。

## 貨幣時間價值 (Time Value of Money)

今天的一塊錢比未來的一塊錢更有價值，因為它反映機會成本、通膨、不確定性與流動性偏好。所以估值問題都變成：把未來現金流折回今天（discounting），或把今天的資金投影到未來（compounding）。

| 概念 | 公式 | 說明 |
| --- | --- | --- |
| 報酬率 | $(V_T - V_0)/V_0$ | 沒說明花多久、中間有無現金流 |
| 終值 (FV) | $PV \cdot (1 + r)^n$ | 複利：利息再生利息，成長是乘法累積 |
| 現值 (PV) | $FV / (1 + r)^n$ | 折現：與終值互為對偶 |
| 每期利率 | 年利率 12%、按月計息 → 每期 $0.12/12 = 1\%$ | 先對齊利率頻率與付款頻率 |
| 有效年利率 (EAR) | $(1 + r_{nom}/m)^m - 1$ | 按月複利的名目 12% → EAR 12.68% |
| 淨現值 (NPV) | $\sum_t CF_t / (1 + r)^t$ | 增加多少價值；> 0 才值得做 |
| 內部報酬率 (IRR) | 使 NPV = 0 的 r | 隱含報酬率；現金流正負號多次改變時可能有多個解 |
| 等值年金 (EAA) | 把 NPV 攤成每年等額 | 比較壽命不同的專案 |

```python
import numpy as np
import numpy_financial as npf          # pip install numpy-financial（NumPy 已移除 np.npv 等函式）

cf = np.array([-1000, 300, 400, 500])  # t = 0, 1, 2, 3
npf.npv(0.08, cf)                      # 17.63：npf.npv 的第一筆不折現（t = 0）
npf.irr(cf)                            # 0.0889

# 房貸：30 年、年利率 6%、按月付款
rate, n, principal = 0.06 / 12, 30 * 12, 500_000
pmt = -npf.pmt(rate, n, principal)     # 每月 2997.75
interest_1 = principal * rate          # 第一期利息 2500：早期大部分付利息，後期才多還本金
```

> 注意 Excel 的 `NPV()` 從第 1 期開始折現，與 `numpy_financial.npv` 不同；要把 t = 0 的投入另外加上。

| 概念 | 要點 |
| --- | --- |
| 資本成本 (cost of capital) | 折現率不是憑感覺；公司層級常用 WACC：依資本結構加權的債務成本（稅後）與股東要求報酬 |
| 債務 vs 權益 | 債權人先拿固定承諾的現金流（下檔保護高）；股東拿剩餘索取權（上檔參與大） |
| 房貸與房屋淨值 | 房價路徑與貸款攤還是兩條不同的動態；房價低於剩餘貸款時為 underwater mortgage |
| 財富累積 | 收入成長、支出、緊急預備金、稅、通膨、投資複利一起作用的多期預算問題 |
| 成長預測 | 跨期成長是乘法：年成長 5% 十年是 ×1.629，不是 +50% |

| 常見錯誤 | |
| --- | --- |
| 用總報酬比較不同持有期間 | 先年化 |
| 沒對齊複利頻率就套用利率 | 年利率直接當月利率 |
| 名目現金流直接相加 | 沒先折現 |
| 只看房貸月付金額 | 沒看本金與利息的分解 |
| 用單一高報酬說服自己 | 沒把風險與資本成本放進來 |

## 債券估值與利率風險

債券估值的本質是把一串已知的現金流用適當的殖利率折現，再分析價格對利率變化有多敏感。以下假設固定票息、固定到期、沒有嵌入選擇權（可贖回、可賣回、可轉換債的現金流時點與金額不固定，分析更複雜）。

| 元素 | 意義 |
| --- | --- |
| 發行人 (issuer) | 誰借錢 |
| 面額 (par / face value) | 到期返還的本金 |
| 票面利率 (coupon rate) | 承諾支付的利息率 |
| 付息頻率 | 年付、半年付、季付 |
| 到期日 (maturity) | 本金何時返還 |

### 價格與殖利率

| 債券 | 價格 |
| --- | --- |
| 零息債 | 只有到期一筆面額的現值：$P = F/(1+y)^T$ |
| 附息債 | 每筆票息與到期本金各自折現後加總（可視為一組零息債） |

殖利率 (yield to maturity, YTM) 是以目前價格買入持有到期的隱含年化報酬率。零息債可代數反推，附息債要用數值求根。殖利率可拆成無風險利率（相近到期的公債）+ 信用利差 + 其他風險溢酬（流動性、可贖回）；沒有流動交易價格的債券，常參考相同信評、相近到期的可比債券殖利率。

```python
from scipy.optimize import brentq

def bond_price(y, face=100, coupon=0.05, years=10, freq=2):
    t = np.arange(1, years * freq + 1)
    cf = np.full(t.size, face * coupon / freq); cf[-1] += face
    return np.sum(cf / (1 + y / freq) ** t)

bond_price(0.05)                                    # 100.0：票面利率 = 殖利率 → 平價
bond_price(0.06)                                    # 92.56：殖利率上升，價格下跌（折價債）
ytm = brentq(lambda y: bond_price(y) - 95, 1e-6, 1)  # 從價格反推殖利率：0.0566
```

| 價格 vs 面額 | 條件 |
| --- | --- |
| 溢價 (premium) | 票面利率 > 殖利率 |
| 平價 (par) | 票面利率 ≈ 殖利率 |
| 折價 (discount) | 票面利率 < 殖利率 |

### Duration 與 Convexity

價格–殖利率曲線是彎的，所以用一階與二階近似：

$$\frac{\Delta P}{P} \approx -D_{mod}\,\Delta y + \tfrac{1}{2}\,C\,(\Delta y)^2$$

| 指標 | 意義 | 何時變大 |
| --- | --- | --- |
| Modified duration | 殖利率變動 1%（100 bp）時價格變動約幾 %；一階斜率 | 到期越長、票息越低、殖利率越低 |
| Macaulay duration | 現金流的加權平均回收時間（年） | 同上 |
| DV01 | 殖利率變動 1 bp 時價格變動的金額 | 部位越大、duration 越長 |
| Convexity | 曲率；二階效果 | 同上 |

```python
def duration_convexity(y, dy=1e-4, **kw):
    p0, up, dn = bond_price(y, **kw), bond_price(y + dy, **kw), bond_price(y - dy, **kw)
    D = (dn - up) / (2 * p0 * dy)                 # modified duration（數值近似）
    C = (up + dn - 2 * p0) / (p0 * dy ** 2)
    dv01 = (dn - up) / 2                          # 每 1 bp
    return D, C, dv01

D, C, dv01 = duration_convexity(0.05)             # D ≈ 7.79、C ≈ 73.6、DV01 ≈ 0.078（每 100 面額）
```

| 觀察 | 說明 |
| --- | --- |
| 小幅變動 | duration 的線性近似就夠，上升與下降效果接近對稱 |
| 大幅變動 | 只用 duration 會失準；正 convexity 讓殖利率下降時漲得比線性預測多、上升時跌得比預測少 |
| 避險 | 用 DV01 而不是面額：避險部位數 = 投組 DV01 / 避險工具 DV01；只消除一階暴露 |

| 常見錯誤 | |
| --- | --- |
| 混淆票面利率與殖利率 | 複利頻率與付息頻率沒對齊 |
| 有嵌入選擇權仍套用一般債券直覺 | 沒區分無風險基準與信用利差 |
| 用 duration 預測大幅利率變動 | 沒加 convexity 調整 |
| 避險只看面額 | 應看 DV01 |

## 金融資料的清理問題

金融分析常常不是從模型開始出錯，而是從資料開始：價格欄位、日期、缺值、代號對應、頻率，只要一處沒處理好，後面的報酬、風險、因子暴露都會被帶偏。

| 資料類型 | 來源例子 | 主軸 | 用途 |
| --- | --- | --- | --- |
| 價格歷史（OHLCV） | Yahoo Finance、交易所 | 日期 | 時間序列分析 |
| 總經與利率 | FRED、World Bank、OECD、Eurostat | 日期（月、季） | 無風險利率、景氣變數 |
| 匯率 | OANDA 等 | 日期 | 跨幣別換算 |
| 參考 metadata | 交易所掛牌資料 | 證券 | 產業、市值、上市年，用於橫斷面分組 |

真正的研究常要把兩者接起來：先用 metadata 挑出某產業的股票 → 抓價格 → 在時間序列上算報酬與暴露。

| 欄位 | 意義 | 用途 |
| --- | --- | --- |
| Open / High / Low / Close | 期間內不同位置的價格 | 技術指標、日內區間、執行路徑 |
| Volume | 成交量 | 流動性 |
| Adjusted Close | 納入股票分割與股利調整 | 長期總報酬比較 |

```python
import pandas as pd

px = pd.read_csv("prices.csv", parse_dates=["date"], index_col="date")
px = px.sort_index()
assert px.index.is_unique                                   # 無重複時間戳
px = px.apply(pd.to_numeric, errors="coerce")               # object 欄（"1,234"、"-"）轉數值

ret = px["adj_close"].pct_change().dropna()                 # 簡單報酬；用調整後價格
log_ret = np.log(px["adj_close"]).diff().dropna()           # 對數報酬：多期可相加

# 多資產：寬表（每檔一欄）便於做報酬矩陣與共變異
wide = long.pivot(index="date", columns="ticker", values="adj_close")

# 不同頻率對齊：日價格 + 月總經資料 → 用「當時已公布」的值
macro = macro.reindex(wide.index, method="ffill")           # 注意公布日 vs 參考期間（避免 look-ahead）
```

| 注意 | 說明 |
| --- | --- |
| 時間索引 | 排序、無重複、頻率差異是預期的而非漏資料；合併不同來源前先定義曆法與對齊規則（股市休市日 vs 總經發布日） |
| 不規則觀測 | 成交、事件、稀疏的財報更新本來就不等距；補成規則網格前先說明缺口代表沒有交易、資料源缺值，還是頻率比原始資料密 |
| 公司行動 | 分割與除息讓原始價格出現結構性跳點；算長期報酬用調整後價格，否則假的崩跌會被當成真的 |
| 分析單位 | 一檔資產的時間序列、同一天多資產的橫斷面、或 panel：沒先講清楚，`groupby`、`stack`、`pivot`、`resample` 會搞混 |
| 存活者偏差 | 只用現在還在交易的股票回測，會遺漏下市的公司，高估歷史報酬 |
| 缺值的意義 | 停牌、尚未上市、資料源缺漏是不同的事 |
