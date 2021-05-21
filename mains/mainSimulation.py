import time
from datetime import datetime
from time import sleep

from binance.client import Client
from loguru import logger

from Compteur import Type
from binanceTS import BinanceTS
from front.front import Front
from indicateurs.Indicateur import Indicateur
from OrderBook import OrderBook
from res import binancekey
from strategies.strategies import Levier, IndicateurE


class MainSimulation:

    def __init__(self, cryptos, time_range, indicateurs: list, validationPercent: float, levier: Levier = Levier.X1):
        logger.add("res/log_test.log")
        self.time_range = time_range
        self.cryptos = cryptos
        self.indicateurs = indicateurs
        self.validationPercent = validationPercent
        self.levier = levier
        self.front = Front(cryptos)
        self.client = Client(binancekey.KEY, binancekey.SECRET)
        self.tab = []
        self.t = {}

        self.orderBook = OrderBook(cryptos, levier)

    def start(self):
        for crypto in self.cryptos:
            df = Indicateur(self.client, crypto, periode=self.time_range).df
            bin = BinanceTS(df)
            df['rsi'] = bin.RSI()
            df['signal'] = bin.MACD()[1].series
            df['macd'] = bin.MACD()[0].series
            df['ema'] = bin.EMA200()[0]
            bin.bollinger()
            # bin.donchian()
            df = df[['close', 'rsi', 'Upper', 'Lower', 'signal', 'macd', 'ema']]
            # df.to_csv(f"{crypto}.csv")
            self.tab.append(df)

        for id, obj in enumerate(self.tab[0].iterrows()):
            index, _ = obj
            date = index
            prices = []
            for i, crypto in enumerate(self.cryptos):
                price, rsi, upper, lower, signal, macd, ema = self.tab[i].iloc[id][['close', 'rsi', 'Upper', 'Lower', 'signal', 'macd', 'ema']]
                bol = (price * 2 - upper - lower) / (upper - lower)

                result = self.calculIndicateurs(self.indicateurs, self.validationPercent, [price, rsi, upper, lower, signal, macd, ema, bol])

                if result and self.orderBook.compteur.canBuyDown(crypto):
                    # logger.info(f"BUY {crypto, price, Type.DOWN}")
                    self.orderBook.addBuyOrder(crypto, price, Type.DOWN)
                elif result and self.orderBook.compteur.canSellUp(crypto):
                    # logger.info(f"SELL {crypto, price, Type.UP}")
                    self.orderBook.addSellOrder(crypto, price, Type.UP)
                elif result == False and self.orderBook.compteur.canSellDown(crypto):
                    # logger.info(f"SELL {crypto, price, Type.DOWN}")
                    self.orderBook.addSellOrder(crypto, price, Type.DOWN)
                elif result == False and self.orderBook.compteur.canBuyUp(crypto):
                    # logger.info(f"BUY {crypto, price, Type.UP}")
                    self.orderBook.addBuyOrder(crypto, price, Type.UP)

                prices.append(price)

            self.front.write([], self.orderBook.compteur.getAmountInTrades(), prices, self.orderBook.compteur.getCryptoBook(), self.orderBook.compteur.getPlusValues(),
                             date=date)
        # logger.info(f"{self.orderBook.compteur.getPlusValues(), self.orderBook.compteur.getNbTrade()}")
        return self.orderBook.compteur.getPlusValues(), self.orderBook.compteur.getNbTrade()

    def getRsi30(self, rsi):
        if rsi > 70.0:
            return 1
        elif rsi < 30.0:
            return -1
        else:
            return 0

    def getRsi25(self, rsi):
        if rsi > 75.0:
            return 1
        elif rsi < 25.0:
            return -1
        else:
            return 0

    def getRsi35(self, rsi):
        if rsi > 65.0:
            return 1
        elif rsi < 35.0:
            return -1
        else:
            return 0

    def getBoll80(self, boll):
        if boll > 0.8:
            return 1
        elif boll < -0.8:
            return -1
        else:
            return 0

    def getBoll70(self, boll):
        if boll > 0.7:
            return 1
        elif boll < -0.7:
            return -1
        else:
            return 0

    def getBoll60(self, boll):
        if boll > 0.6:
            return 1
        elif boll < -0.6:
            return -1
        else:
            return 0

    def getMACDzeroed(self, macd, signal):
        if macd > signal > 0:
            return 1
        elif macd < signal < 0:
            return -1
        else:
            return 0

    def getMACD(self, macd, signal):
        if macd > signal:
            return 1
        elif macd < signal:
            return -1
        else:
            return 0

    def getEMA(self, price, ema):
        if price > ema:
            return 1
        elif price < ema:
            return -1
        else:
            return 0

    def getDonchian(self, highest, lowest):
        pass

    def calculIndicateurs(self, indicateurs, validationPercent, values):
        price, rsi, upper, lower, signal, macd, ema, bol = values
        size = len(indicateurs)
        nb = 0

        for indicateur in indicateurs:
            if indicateur == IndicateurE.RSI25:
                nb += self.getRsi25(rsi)
            if indicateur == IndicateurE.RSI30:
                nb += self.getRsi30(rsi)
            if indicateur == IndicateurE.RSI35:
                nb += self.getRsi35(rsi)
            if indicateur == IndicateurE.Boll60:
                nb += self.getBoll60(bol)
            if indicateur == IndicateurE.Boll70:
                nb += self.getBoll70(bol)
            if indicateur == IndicateurE.Boll80:
                nb += self.getBoll80(bol)
            if indicateur == IndicateurE.MACD:
                nb += self.getMACD(macd, signal)
            if indicateur == IndicateurE.EMA200:
                nb += self.getEMA(price, ema)
            if indicateur == IndicateurE.MACDzeroed:
                nb += self.getMACDzeroed(price, ema)
            if indicateur == IndicateurE.Donchian:
                # nb += self.getDonchian()
                pass
        if nb / size >= validationPercent:
            return True
        else:
            return False
