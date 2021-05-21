from strategies.strategies import Levier
from traders.Trader import Trader
from loguru import logger
from decimal import *


class Simulation(Trader):
    compteur = None
    client = None
    balance = 1000
    cryptos = {}

    def __init__(self, cryptos, levier: Levier):
        self.levier = levier
        for crypto in cryptos:
            self.cryptos[f"{crypto}"] = {'amount': 0, 'loanValue': 0, 'loanAmount': 0}

    def buy(self, crypto, amount: Decimal, price: Decimal):
        value = amount * price
        realValue = value - (value * Decimal(0.0004))
        realAmount = amount - (amount * Decimal(0.0004))
        self.cryptos[f"{crypto}"]["loanValue"] = Decimal(realValue) * Decimal(self.levier.value) - realValue
        self.balance -= value
        self.cryptos[f"{crypto}"]["loanAmount"] = Decimal(realAmount) * Decimal(self.levier.value) - realAmount
        self.cryptos[f"{crypto}"]["amount"] += realAmount * Decimal(self.levier.value)

    def sell(self, crypto, amount: Decimal, price: Decimal):
        value = amount * price
        if not Decimal(self.cryptos[f"{crypto}"]["amount"] - amount) >= 0:
            logger.error(f"Attempt to sell not owned crypto ({amount} {crypto} worth {value})")
        else:
            self.cryptos[f"{crypto}"]["amount"] = Decimal(self.cryptos[f"{crypto}"]["amount"] - amount - self.cryptos[f"{crypto}"]["loanAmount"])
            self.balance += value
            self.cryptos[f"{crypto}"]["loanValue"] = 0

    def getAmount(self, crypto):
        return self.cryptos[f"{crypto}"]["amount"]

    def getBalance(self):
        return Decimal(self.balance)
