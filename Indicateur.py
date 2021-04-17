from binance.client import Client
import pandas as pd
import binancekey
from binanceTS import BinanceTS


class Indicateur:
    values = {}
    ts = None

    def __init__(self, values):
        client = Client(binancekey.KEY, binancekey.SECRET)
        klines = client.get_historical_klines("NANOBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

        df = pd.DataFrame.from_dict(klines)
        df = df.rename(
            columns={0: "open_time", 1: "open", 2: "high", 3: "low", 4: "close", 5: "ignore", 6: "close_time", 7: "ignore", 8: "nb_bisic", 9: "ignore", 10: "ignore",
                     11: "ignore", })
        df = df.set_index("open_time")
        self.ts = BinanceTS(df)
        self.values = values

    def __getRSI(self, crypto):
        self.ts.bollinger()

    def __getBallinger(self, crypto):
        return 0

    def canBuy(self, crypto):
        if self.__getRSI(crypto) + self.__getBallinger(crypto) == 2:
            print("peu acheter")

    def canSell(self, crypto):
        if self.__getRSI(crypto) + self.__getBallinger(crypto) == -2:
            print("peu vendre")
