import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import MetaTrader5 as mt5


mt5.initialize()
mt5.symbol_select("EURUSD", True)
bars_a_day = 24 * 4          
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M15, 0, bars_a_day*7 )


df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)
df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low',
    'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)


mpf.plot(
    df,
    type='candle',
    mav=(20,50),         
    volume=True,
    style='yahoo',
    title=f'EURUSD candle graph for 1 weeks ',
    ylabel='Price',
    ylabel_lower='Volume')

mt5.shutdown() 

plt.show()
