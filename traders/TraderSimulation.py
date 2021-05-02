from traders.Trader import Trader
from loguru import logger
from decimal import *


class Simulation(Trader):
    compteur = None
    client = None
    balance = 1000
    cryptos = {}

    def __init__(self, cryptos):
        for crypto in cryptos:
            self.cryptos[f"{crypto}"] = {'amount': 0}

    def buy(self, crypto, amount: Decimal, price: Decimal):
        value = amount * price
        value = value.quantize(Decimal('.00'))
        self.cryptos[f"{crypto}"]["amount"] += amount
        self.balance -= value

    def sell(self, crypto, amount: Decimal, price: Decimal):
        value = amount * price
        value = value.quantize(Decimal('.00'))
        if not Decimal(self.cryptos[f"{crypto}"]["amount"] - amount).quantize(Decimal('.00')) >= 0:
            logger.error(f"Attempt to sell not owned crypto ({amount} {crypto} worth {value})")
        else:
            self.cryptos[f"{crypto}"]["amount"] = Decimal(self.cryptos[f"{crypto}"]["amount"] - amount).quantize(Decimal('.000000'))
        self.balance += value

    # Recupere le nombre de tokens possédé
    def getAmount(self, crypto):
        return self.cryptos[f"{crypto}"]["amount"]

    def getBalance(self):
        return Decimal(self.balance)
