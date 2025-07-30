series1 = pd.Series(['a','b','c','d'], index=['1','2','3','4'])
pd.concat([series1, series2], ignore_index=True) #combine two series, ignore index
