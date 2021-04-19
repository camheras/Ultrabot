from datetime import datetime

from binance.client import Client
import pandas as pd
import binancekey
from binanceTS import BinanceTS
from loguru import logger


class Indicateur:
    values = {}
    ts = None

    def __init__(self, client, crypto, periode=""):
        klines = client.get_historical_klines(f"{crypto}USDT", Client.KLINE_INTERVAL_1MINUTE, "3 hours ago UTC")

        df = pd.DataFrame.from_dict(klines)
        df = df.rename(
            columns={0: "open_time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "ignore", 6: "close_time", 7: "ignore", 8: "nb_bisic", 9: "ignore", 10: "ignore",
                     11: "ignore", })
        df["open_time"] = df["open_time"].map(lambda x: datetime.fromtimestamp(int(str(x)[:-3])))
        df['open_time'] = pd.to_datetime(df['open_time'])
        df["close_time"] = df["close_time"].map(lambda x: datetime.fromtimestamp(int(str(x)[:-3])))
        df['close_time'] = pd.to_datetime(df['close_time'])
        df['close'] = pd.to_numeric(df['close'])
        df['open'] = pd.to_numeric(df['open'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])

        df = df.set_index("open_time")

        self.ts = BinanceTS(df)

    def getRSI(self):
        rsi_df = self.ts.RSI()
        value_rsi = rsi_df[-1]
        if value_rsi > 65.0:
            return 1
        elif value_rsi < 35.0:
            return -1
        else:
            return 0

    def getBollinger(self):
        upper, lower, current = self.ts.bollinger()[["Upper", "Lower", "close"]].iloc[-1]
        up_dist = upper - current
        low_dist = current - lower

        return self.ts.bollinger()[["Upper", "Lower", "close"]].iloc[-1]

    def canBuy(self):
        value_rsi = self.getRSI()
        value_boll = self.getBollinger()

        if value_rsi > 65.0:
            rsi = 1
        elif value_rsi < 35.0:
            rsi = -1
        else:
            rsi = 0

        if value_boll:
            boll = 1
        elif value_boll:
            boll = -1
        else:
            boll = 0

    def result(self):
        if self.getRSI() + self.getBollinger() == 2:
            print("peut acheter")
        elif self.getRSI() + self.getBollinger() == -2:
            print("peut vendre")
