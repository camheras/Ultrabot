import datetime

from Compteur import Compteur

from loguru import logger

from traders.TraderSimulation import Simulation
from traders.TraderBinance import TraderBinance


class OrderBook:
    trader = None
    compteur = None
    padding = 0

    def __init__(self, cryptos: list, trader="simulation", padding=0.2):
        self.cryptos = cryptos
        if trader == "simulation":
            self.trader = Simulation()
        elif trader == "kraken":
            self.trader = TraderKraken()
        elif trader == "binance":
            self.trader = TraderBinance()
        self.compteur = Compteur(cryptos)
        self.balance = self.trader.getBalance()
        self.padding = padding

    def addBuyOrder(self, crypto, price):
        value = self.__getAvailableMoney()
        if self.trader.__class__ == Simulation:

            self.trader.buy(crypto, value)
        else:
            # currentPrice = self.trader.buy(crypto, amount)
            pass
        val = float(value) / float(price)
        self.compteur.buyOrder(crypto, price, value, datetime.datetime.now(), val)
        self.compteur.addAmountInTrades(value)
        # self.compteur.addOrder({
        #     'crypto': f'{crypto}',
        #     'buyPrice': currentPrice,
        #     'sellPrice': '',
        #     'amount': f'{val}',
        #     'value': f'{float(value)}$',
        #     'timestamp': f'{datetime.datetime.now()}',
        # })

    def addSellOrder(self, crypto, price):

        amount = self.trader.getAmount(crypto)

        if self.trader.__class__ == Simulation:
            pass
        else:
            # currentPrice = self.trader.sell(crypto, amount)
            pass
        try:
            self.trader.sell(crypto, float(amount) / float(price))
            if amount > 0:
                value = float(amount) / float(price)
                # currentPrice = self.trader.sell(crypto, amount)
                # currentPrice = self.trader.getPrice(crypto)
                self.compteur.sellOrder(crypto, value)
                self.compteur.removeAmountInTrades(value)
                # self.compteur.addOrder({
                #     'crypto': f'{crypto}',
                #     'buyPrice': '',
                #     'sellPrice': currentPrice,
                #     'value': f'{value}$',
                #     'timestamp': f'{datetime.datetime.now()}',
                # })
            else:
                logger.error(f"Can't sell, {crypto} balance is not enough.")

        except TypeError:
            logger.error(f"{amount, price}")

    def __getAvailableMoney(self):
        # TODO changer pour mettre en fonction du nombre de crypto
        logger.error(f"amount in trades : {self.compteur.getAmountInTrades()}")
        return (self.compteur.getAmountInTrades() + float(self.balance)) / len(self.cryptos)

    def getTokens(self):
        return self.trader.getTokens()
