import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

mt5.initialize()

symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_D1
bars = 200

rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

mt5.shutdown()

data = pd.DataFrame(rates)
data['time'] = pd.to_datetime(data['time'])
data.set_index('time', inplace=True)

window = 20
data['SMA'] = data['close'].rolling(window=window).mean()
data['STD'] = data['close'].rolling(window=window).std()
data['Upper Band'] = data['SMA'] + 2 * data['STD']
data['Lower Band'] = data['SMA'] - 2 * data['STD']

data['above_upper'] = data['close'] > data['Upper Band']
data['below_lower'] = data['close'] < data['Lower Band']

data['outlier_signal'] = 0
data.loc[(data['above_upper']) & (~data['above_upper'].shift(1).fillna(False)), 'outlier_signal'] = 1
data.loc[(data['below_lower']) & (~data['below_lower'].shift(1).fillna(False)), 'outlier_signal'] = -1

upper_outliers = data[data['outlier_signal'] == 1]
lower_outliers = data[data['outlier_signal'] == -1]

plt.figure(figsize=(18, 10))
plt.plot(data.index, data['close'], label='Fiyat', color='black', linewidth=1)
plt.plot(data.index, data['SMA'], label='SMA', color='blue', linestyle='--')
plt.plot(data.index, data['Upper Band'], label='Upper Band', color='red')
plt.plot(data.index, data['Lower Band'], label='Lower Band', color='green')
plt.fill_between(data.index, data['Lower Band'], data['Upper Band'], color='gray', alpha=0.2)

# Outlier noktalarını ekle
plt.scatter(upper_outliers.index, upper_outliers['close'], color='red', label='Upper Outlier', marker='^', s=100)
plt.scatter(lower_outliers.index, lower_outliers['close'], color='green', label='Lower Outlier', marker='v', s=100)

plt.title(f'{symbol} Bollinger Bands')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
