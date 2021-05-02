from datetime import datetime

from binance.client import Client
import pandas as pd
from binanceTS import BinanceTS
from loguru import logger


class Indicateur:
    values = {}
    ts = None
    df = ""

    def __init__(self, client, crypto, periode="3 hours ago UTC"):
        klines = client.get_historical_klines(f"{crypto}USDT", Client.KLINE_INTERVAL_1MINUTE,periode)

        self.df = pd.DataFrame.from_dict(klines)
        self.df = self.df.rename(
            columns={0: "open_time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "ignore", 6: "close_time", 7: "ignore", 8: "nb_bisic", 9: "ignore", 10: "ignore",
                     11: "ignore", })
        self.df["open_time"] = self.df["open_time"].map(lambda x: datetime.fromtimestamp(int(str(x)[:-3])))
        self.df['open_time'] = pd.to_datetime(self.df['open_time'])
        self.df["close_time"] = self.df["close_time"].map(lambda x: datetime.fromtimestamp(int(str(x)[:-3])))
        self.df['close_time'] = pd.to_datetime(self.df['close_time'])
        self.df['close'] = pd.to_numeric(self.df['close'])
        self.df['open'] = pd.to_numeric(self.df['open'])
        self.df['high'] = pd.to_numeric(self.df['high'])
        self.df['low'] = pd.to_numeric(self.df['low'])

        self.df = self.df.set_index("open_time")

        self.ts = BinanceTS(self.df)

    def getRSI(self):
        rsi_df = self.ts.RSI()
        val = rsi_df[-1]
        if val > 65.0:
            return 1
        elif val < 35.0:
            return -1
        else:
            return 0

    def getBollinger(self):
        upper, lower, current = self.ts.bollinger()[["Upper", "Lower", "close"]].iloc[-1]

        val = (current * 2 - upper - lower) / (upper - lower)

        if val > 0.80:
            return 1
        elif val < -0.8:
            return -1
        else:
            return 0

    def result(self):
        if self.getRSI() + self.getBollinger() == 2:
            return True
        elif self.getRSI() + self.getBollinger() == -2:
            return False
        else:
            return None

    def getPrice(self):
        return self.ts.getPrice()
