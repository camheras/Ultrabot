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


class MainSimulation:

    def __init__(self, cryptos, time_range):
        logger.add("res/log_test.log")
        self.time_range = time_range
        self.cryptos = cryptos
        self.front = Front(cryptos)
        self.client = Client(binancekey.KEY, binancekey.SECRET)
        self.tab = []
        self.orderBook = OrderBook(cryptos)

    def start(self):
        for crypto in self.cryptos:
            df = Indicateur(self.client, crypto, periode=self.time_range).df
            bin = BinanceTS(df)
            df['rsi'] = bin.RSI()
            bin.bollinger()
            df = df[['close', 'rsi', 'Upper', 'Lower']]
            self.tab.append(df)

        for id, crypto in enumerate(self.cryptos):
            df = self.tab[id]

            for index, row in df.iterrows():
                price, rsi, Upper, Lower = row
                date = index
                val = (price * 2 - Upper - Lower) / (Upper - Lower)
                boll = self.getBoll(val)
                rsi_index = self.getRsi(rsi)
                result = self.getResult(boll, rsi_index)

                if result and self.orderBook.compteur.canBuyDown(crypto):
                    logger.info(f"BUY {crypto, price, Type.DOWN}")
                    self.orderBook.addBuyOrder(crypto, price, Type.DOWN)
                elif result and self.orderBook.compteur.canSellUp(crypto):
                    logger.info(f"SELL {crypto, price, Type.UP}")
                    self.orderBook.addSellOrder(crypto, price, Type.UP)
                elif result == False and self.orderBook.compteur.canSellDown(crypto):
                    logger.info(f"SELL {crypto, price, Type.DOWN}")
                    self.orderBook.addSellOrder(crypto, price, Type.DOWN)
                elif result == False and self.orderBook.compteur.canBuyUp(crypto):
                    logger.info(f"BUY {crypto, price, Type.UP}")
                    self.orderBook.addBuyOrder(crypto, price, Type.UP)

                # logger.info(f"{crypto} - {self.orderBook.compteur.getNbTrade(), boll, rsi_index} ")

                self.front.write([], self.orderBook.compteur.getAmountInTrades(), [0, 0], self.orderBook.compteur.getCryptoBook(), self.orderBook.compteur.getPlusValues(),
                                 date=date)
        logger.info(self.orderBook.compteur.getPlusValues())

    def getRsi(self, rsi):
        if rsi > 65.0:
            return 1
        elif rsi < 35.0:
            return -1
        else:
            return 0

    def getBoll(self, boll):
        if boll > 0.80:
            return 1
        elif boll < -0.8:
            return -1
        else:
            return 0

    def getResult(self, boll, rsi):
        if rsi + boll == 2:
            return True
        elif rsi + boll == -2:
            return False
        else:
            return None
