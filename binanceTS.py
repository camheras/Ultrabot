from binance.client import Client
import binancekey
from loguru import logger
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class BinanceTS:
    df = None

    def __init__(self, df):
        self.df = df

    def bollinger(self, df):
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['20dSTD'] = df['close'].rolling(window=20).std()

        df['Upper'] = df['MA20'] + (df['20dSTD'] * 2)
        df['Lower'] = df['MA20'] - (df['20dSTD'] * 2)
        return df

    def RSI(self, df):
        pass

    # bollinger(df)[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
    # plt.grid(True)
    # plt.title(' Bollinger Bands')
    # plt.axis('tight')
    # plt.ylabel('Price')
    # plt.savefig('apple.png', bbox_inches='tight')
    # logger.info(df)
