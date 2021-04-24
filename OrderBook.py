import datetime

from Compteur import Compteur

from loguru import logger

from traders.TraderSimulation import Simulation
from traders.TraderBinance import TraderBinance


class OrderBook:
    trader = None
    compteur = None
    padding = 0

    def __init__(self, indicateur=None, trader="simulation", padding=0.2, ):

        if trader == "simulation":
            self.trader = Simulation()
        elif trader == "kraken":
            self.trader = TraderKraken()
        elif trader == "binance":
            self.trader = TraderBinance()
        self.indicateur = indicateur
        self.compteur = Compteur()
        self.balance = self.trader.getBalance()
        self.padding = padding

    def addBuyOrder(self, crypto):
        value = self.__getAvailableMoney()
        if self.trader.__class__ == Simulation:
            currentPrice = self.indicateur.getPrice()
            self.trader.buy(crypto, value)
        else:
            # currentPrice = self.trader.buy(crypto, amount)
            pass
        val = float(value) / float(currentPrice)
        self.compteur.buyOrder(crypto)
        self.compteur.addAmountInTrades(val)
        self.compteur.addOrder({
            'crypto': f'{crypto}',
            'buyPrice': currentPrice,
            'sellPrice': '',
            'amount': f'{val}',
            'value': f'{float(value)}$',
            'timestamp': f'{datetime.datetime.now()}',
        })

    def addSellOrder(self, crypto):
        currentPrice = 0
        amount = self.trader.getAmount(crypto)

        if self.trader.__class__ == Simulation:
            currentPrice = self.indicateur.getPrice()
        else:
            # currentPrice = self.trader.sell(crypto, amount)
            pass
        try:
            self.trader.sell(crypto, float(amount) / float(currentPrice))
            if amount > 0:
                value = float(amount) / float(currentPrice)
                # currentPrice = self.trader.sell(crypto, amount)
                # currentPrice = self.trader.getPrice(crypto)
                self.compteur.sellOrder(crypto)
                self.compteur.removeAmountInTrades(value)
                self.compteur.addOrder({
                    'crypto': f'{crypto}',
                    'buyPrice': '',
                    'sellPrice': currentPrice,
                    'value': f'{value}$',
                    'timestamp': f'{datetime.datetime.now()}',
                })
            else:
                logger.error(f"Can't sell, {crypto} balance is not enough.")

        except TypeError:
            logger.error(f"{amount, currentPrice}")

    def __getAvailableMoney(self):
        # TODO changer pour mettre en fonction du nombre de crypto
        return (self.compteur.getAmountInTrades() + float(self.balance)) * self.padding

    def getTokens(self):
        return self.trader.getTokens()
