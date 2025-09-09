divorce.corr(numeric_only=True)

Pearson correlation coefficient
plot example

Autocorrelation serial correlation
df['ABC'].autocorr()

Mean Reversion - Negative autocorrelation
Momentum, or Trend Following - Positive autocorrelation

# Convert index to datetime
df.index = pd.to_datetime(df.index)
# Downsample from daily to monthly data
df = df.resample(rule='M').last()
# Compute returns from prices
df['Return'] = df['Price'].pct_change()
# Compute autocorrelation
autocorrelation = df['Return'].autocorr()
print("The autocorrelation is: ",autocorrelation)