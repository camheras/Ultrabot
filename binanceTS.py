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

    def bollinger(self):
        self.df['MA20'] = self.df['close'].rolling(window=20).mean()
        self.df['20dSTD'] = self.df['close'].rolling(window=20).std()

        self.df['Upper'] = self.df['MA20'] + (self.df['20dSTD'] * 2)
        self.df['Lower'] = self.df['MA20'] - (self.df['20dSTD'] * 2)
        self.df[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
        plt.grid(True)
        plt.title(' Bollinger Bands')
        plt.axis('tight')
        plt.ylabel('Price')
        plt.savefig('apple.png', bbox_inches='tight')
        return self.df

    def RSI(self):
        pass

    # bollinger(df)[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
    # plt.grid(True)
    # plt.title(' Bollinger Bands')
    # plt.axis('tight')
    # plt.ylabel('Price')
    # plt.savefig('apple.png', bbox_inches='tight')
    # logger.info(df)
