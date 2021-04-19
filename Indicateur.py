from datetime import datetime

from binance.client import Client
import pandas as pd
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

    def __getRSI(self):
        rsi_df = self.ts.RSI()
        val = rsi_df[-1]
        if val > 65.0:
            return 1
        elif val < 35.0:
            return -1
        else:
            return 0

    def __getBollinger(self):
        upper, lower, current = self.ts.bollinger()[["Upper", "Lower", "close"]].iloc[-1]

        val = (current * 2 - upper - lower) / (upper - lower)

        if val > 0.80:
            return 1
        elif val < -0.8:
            return -1
        else:
            return 0

    def result(self):
        if self.__getRSI() + self.__getBollinger() == 2:
            logger.critical("peut acheter")
        elif self.__getRSI() + self.__getBollinger() == -2:
            logger.critical("peut vendre")
        else:
            logger.info("pas le bon moment")
