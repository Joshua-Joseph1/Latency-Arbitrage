from statistics import median
from numpy import average, minimum
import pandas as pd
import numpy as np

data = pd.read_csv(r'C:\Users\jejos\OneDrive\Documents\Backtest\Latency Arbitrage\TickData.csv')

data['Time Lag'] = pd.to_datetime(data['FxPro Time'])-pd.to_datetime(data['FXCM Time'])

data['Profit'] = data['FxPro bidopen'] - data['FXCM Ask']

print(type(data['Time Lag'][0]))

print(min(data['Time Lag']), max(data['Time Lag']))

print(data)

print(pd.to_timedelta(pd.Series(data['Time Lag'])).mean())