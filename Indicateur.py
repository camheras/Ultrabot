from binance.client import Client
import pandas as pd
import binancekey
from binanceTS import BinanceTS


class Indicateur:
    values = {}
    ts = None

    def __init__(self, crypto, periode=""):
        client = Client(binancekey.KEY, binancekey.SECRET)
        klines = client.get_historical_klines(f"{crypto}USDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

        df = pd.DataFrame.from_dict(klines)
        df = df.rename(
            columns={0: "open_time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "ignore", 6: "close_time", 7: "ignore", 8: "nb_bisic", 9: "ignore", 10: "ignore",
                     11: "ignore", })
        df = df.set_index("open_time")
        self.ts = BinanceTS(df)

    def __getRSI(self):
        return self.ts.RSI()

    def __getBollinger(self):
        return self.ts.bollinger()

    def canBuy(self):
        if self.__getRSI() + self.__getBollinger() == 2:
            print("peut acheter")

    def canSell(self):
        if self.__getRSI() + self.__getBollinger() == -2:
            print("peut vendre")
