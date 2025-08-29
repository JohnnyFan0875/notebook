import statsmodels.api as sm
sm.OLS(y, x).fit()

pd.ols(y, x)

from scipy import stats
stats.linregress(x, y)

np.polyfit(x, y, deg=1)

import statsmodels.api as sm
df['SPX_Ret'] = df['SPX_Prices'].pct_change()
df['R2000_Ret'] = df['R2000_Prices'].pct_change()
df = sm.add_constant(df)

results = sm.OLS(df['R2000_Ret'],df[['const','SPX_Ret']]).fit()

results.params[0]
results.params[1]