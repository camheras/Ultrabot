import datetime
from decimal import *
from Compteur import Compteur, Type
from loguru import logger
from traders.TraderSimulation import Simulation
from traders.TraderBinance import TraderBinance


class OrderBook:
    trader = None
    compteur = None
    balances = {}

    def __init__(self, cryptos: list, trader="simulation"):
        self.cryptos = cryptos
        if trader == "simulation":
            self.trader = Simulation(cryptos)
        elif trader == "kraken":
            self.trader = TraderKraken()
        elif trader == "binance":
            self.trader = TraderBinance()
        self.compteur = Compteur(cryptos)
        for crypto in cryptos:
            self.balances[f"{crypto}"] = self.trader.getBalance() / len(cryptos)

    def addBuyOrder(self, crypto, price, type: Type):
        value = self.balances[f"{crypto}"]
        amount = Decimal(value) / Decimal(price)
        self.trader.buy(crypto, Decimal(amount), Decimal(price))
        self.compteur.buyOrder(crypto, price, value, datetime.datetime.now(), amount, type)
        self.compteur.addAmountInTrades(value)

    def addSellOrder(self, crypto, price, type: Type):
        previous = self.balances[f"{crypto}"]
        amount = self.trader.getAmount(crypto)
        value = Decimal(price) * Decimal(amount)

        if type == Type.DOWN:
            value = previous + (previous - value)

        try:
            if value > 0:
                self.trader.sell(crypto, Decimal(amount), Decimal(price))
                self.compteur.sellOrder(crypto, value)
                self.balances[f"{crypto}"] = value
                self.compteur.removeAmountInTrades(value)
            else:
                logger.error(f"Can't sell, {crypto} balance is not enough.")

        except TypeError:
            logger.error(f"{amount, price}")
