import datetime
from decimal import *
from Compteur import Compteur, Type
from loguru import logger

from strategies.strategies import IndicateurE, Levier
from traders.TraderSimulation import Simulation
from traders.TraderBinance import TraderBinance


class OrderBook:
    trader = None
    compteur = None
    balances = {}

    def __init__(self, cryptos: list, levier: Levier, trader="simulation"):
        self.cryptos = cryptos
        self.levier = levier
        if trader == "simulation":
            self.trader = Simulation(cryptos, levier)
        elif trader == "binance":
            self.trader = TraderBinance()
        self.compteur = Compteur(cryptos, levier)
        for crypto in cryptos:
            self.balances[f"{crypto}"] = self.trader.getBalance() / len(cryptos)

    def addBuyOrder(self, crypto, price, type: Type):
        value = self.balances[f"{crypto}"]
        amount = Decimal(value) / Decimal(price)
        self.trader.buy(crypto, Decimal(amount), Decimal(price))
        self.compteur.buyOrder(crypto, price, value, datetime.datetime.now(), amount, type)
        self.compteur.addAmountInTrades(Decimal(value))

    def addSellOrder(self, crypto, price, type: Type):
        previous = self.balances[f"{crypto}"]
        amount = Decimal(self.trader.getAmount(crypto)) / self.levier.value
        realAmount = amount - (amount * Decimal(0.0004))
        realValue = Decimal(price) * Decimal(realAmount)
        value = Decimal(price) * Decimal(realAmount)

        if type == Type.DOWN:
            value = previous + (previous - realValue)

        try:
            if value > 0:
                self.trader.sell(crypto, Decimal(realAmount), Decimal(price))
                self.compteur.sellOrder(crypto, realValue)
                self.balances[f"{crypto}"] = value
                self.compteur.removeAmountInTrades(value)
            else:
                logger.error(f"Can't sell, {crypto} balance is not enough. RealAmount : {realAmount} RealValue : {realValue} Previous : {previous}")
        except TypeError:
            logger.error(f"{amount, price}")

