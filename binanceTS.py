import btalib
from btalib import ema
from btalib.meta.lines import Line
from pandas import DataFrame
import backtrader as bt


class BinanceTS:
    df: DataFrame = None

    def __init__(self, df: DataFrame):
        self.df = df

    def bollinger(self) -> DataFrame:
        self.df['MA20'] = self.df['close'].rolling(window=20).mean()
        self.df['20dSTD'] = self.df['close'].rolling(window=20).std()

        self.df['Upper'] = self.df['MA20'] + (self.df['20dSTD'] * 2)
        self.df['Lower'] = self.df['MA20'] - (self.df['20dSTD'] * 2)
        # self.df[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
        # plt.grid(True)
        # plt.title(' Bollinger Bands')
        # plt.axis('tight')
        # plt.ylabel('Price')
        # plt.savefig('apple.png', bbox_inches='tight')
        return self.df

    def RSI(self, n=14) -> DataFrame:
        return btalib.rsi(self.df['close'], period=n).df.rsi

    def getPrice(self):
        return self.df['close'].iloc[-1]

    def getPrices(self) -> DataFrame:
        return self.df['close']

    def MACD(self) -> Line:
        return btalib.macd(self.df.close)

    def EMA200(self) -> ema:
        return btalib.ema(self.df.close, period=200)

    def donchian(self, period=20):
        self.df['highest'] = bt.ind.Highest(self.df['high'], period=period)
        self.df['lowest'] = bt.ind.Lowest(self.df['low'], period=period)
        self.df['dcm'] = (self.df['highest'] + self.df['lowest']) / 2.0
