from decimal import Decimal
from enum import Enum
from loguru import logger
from strategies.strategies import Levier


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Type(Enum):
    DOWN = "Down"
    UP = "Up"


class Compteur:
    __orders = []
    __nbBuy = 0
    __nbSell = 0
    __nbSellFees = 0
    __nbBuyFees = 0
    __amountInTrades = 0
    __cryptoBook = {}

    def __init__(self, cryptos, levier: Levier):
        self.levier = levier
        self.cryptos = cryptos
        for crypto in cryptos:
            self.__cryptoBook[f"{crypto}"] = {'nbBuy': 0, 'nbSell': 0, 'currentTrade': {}, 'plusvalue': Decimal(0)}

    def buyOrder(self, crypto, buyPrice, value, timestamp, amount, type: Type):
        self.__cryptoBook[f"{crypto}"]["nbBuy"] += 1
        initValue = value
        value = initValue * self.levier.value
        amount = amount * self.levier.value
        loanValue = value - initValue
        realValue = value - (value * Decimal(0.0004))
        realAmount = amount - (amount * Decimal(0.0004))
        self.__cryptoBook[f"{crypto}"]["currentTrade"] = {'timestamp': timestamp, 'buyPrice': buyPrice, 'amount': realAmount, 'type': type, 'value': realValue,
                                                          'initValue': initValue,
                                                          'loanValue': loanValue}
        self.__nbBuy += 1

    def sellOrder(self, crypto, value):
        self.__cryptoBook[f"{crypto}"]["nbSell"] += 1
        plusvalue = value - self.__cryptoBook[f"{crypto}"]["currentTrade"]["initValue"]
        self.__cryptoBook[f"{crypto}"]["plusvalue"] += Decimal(Decimal(plusvalue).quantize(Decimal('.00000000')))
        self.__cryptoBook[f"{crypto}"]["currentTrade"] = {}
        self.__nbSell += 1

    def buyFees(self, cost):
        self.__nbBuyFees += cost

    def sellFees(self, cost):
        self.__nbSellFees += cost

    def addOrder(self, json):
        self.__orders.append(json)

    def getOrders(self):
        return self.__orders

    def getNbTrade(self):
        return self.__nbBuy + self.__nbSell

    def getTotalFees(self):
        return self.__nbBuyFees + self.__nbSellFees

    def addAmountInTrades(self, value):
        value = value - (value * Decimal(0.0004))
        self.__amountInTrades += value

    def removeAmountInTrades(self, value):
        self.__amountInTrades -= value

    def getAmountInTrades(self):
        return self.__amountInTrades

    def getCryptoBook(self) -> dict:
        return self.__cryptoBook

    def canBuyUp(self, crypto):
        return self.__cryptoBook[f"{crypto}"]["currentTrade"] == {}

    def canBuyDown(self, crypto):
        return self.__cryptoBook[f"{crypto}"]["currentTrade"] == {}

    def canSellUp(self, crypto):
        return not self.__cryptoBook[f"{crypto}"]["currentTrade"] == {} and self.__cryptoBook[f"{crypto}"]["currentTrade"]["type"] == Type.UP

    def canSellDown(self, crypto):
        return not self.__cryptoBook[f"{crypto}"]["currentTrade"] == {} and self.__cryptoBook[f"{crypto}"]["currentTrade"]["type"] == Type.DOWN

    def getPlusValues(self):
        return [float(self.__cryptoBook[f"{crypto}"]["plusvalue"]) for crypto in self.cryptos]
