import pandas as pd

data = pd.read_csv(r"C:\Users\jejos\OneDrive\Documents\Backtest\Latency Arbitrage\NAS100.csv")
data.pop('Unnamed: 0')
data.drop_duplicates(keep="first", subset=['FXCM Time'] ,inplace=True)

data.to_csv('Test2.csv')

print(data)