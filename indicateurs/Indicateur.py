from datetime import datetime

from binance.client import Client
import pandas as pd
from binanceTS import BinanceTS
from loguru import logger


class Indicateur:
    values = {}
    ts = None
    df = ""

    def __init__(self, client, crypto, periode):
        if len(periode) > 1 and type(periode) == list:
            klines = client.get_historical_klines(f"{crypto}USDT", Client.KLINE_INTERVAL_30MINUTE, periode[0], periode[1])
        else:
            klines = client.get_historical_klines(f"{crypto}USDT", Client.KLINE_INTERVAL_30MINUTE, periode)

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

    def getPrice(self):
        return self.ts.getPrice()
