from binance.client import Client
import binancekey
from loguru import logger
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class BinanceTS:
    df = None

    def __init__(self):
        client = Client(binancekey.KEY, binancekey.SECRET)
        klines = client.get_historical_klines("NANOBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

        self.df = pd.DataFrame.from_dict(klines)
        self.df = self.df.rename(
            columns={0: "open_time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "ignore", 6: "close_time", 7: "ignore", 8: "nb_bisic", 9: "ignore", 10: "ignore",
                     11: "ignore", })
        self.df = self.df.set_index("open_time")

    def bollinger(self, df):
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['20dSTD'] = df['close'].rolling(window=20).std()

        df['Upper'] = df['MA20'] + (df['20dSTD'] * 2)
        df['Lower'] = df['MA20'] - (df['20dSTD'] * 2)
        return df

    def RCI(self,df):
        pass
    
    # bollinger(df)[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
    # plt.grid(True)
    # plt.title(' Bollinger Bands')
    # plt.axis('tight')
    # plt.ylabel('Price')
    # plt.savefig('apple.png', bbox_inches='tight')
    # logger.info(df)
