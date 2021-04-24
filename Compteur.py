from loguru import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Compteur(metaclass=Singleton):
    __orders = []
    __nbBuy = 0
    __nbSell = 0
    __nbSellFees = 0
    __nbBuyFees = 0
    __amountInTrades = 0
    __nbTrades = {}

    def buyOrder(self, crypto):
        try:
            self.__nbTrades[f"{crypto}"]["nbBuy"] += 1
        except KeyError:
            self.__nbTrades[f"{crypto}"] = {"nbBuy": 0}
            self.__nbTrades[f"{crypto}"]["nbBuy"] += 1
        self.__nbBuy += 1
        logger.info(self.__nbTrades)

    def sellOrder(self, crypto):
        try:
            self.__nbTrades[f"{crypto}"]["nbSell"] += 1
        except KeyError:
            self.__nbTrades[f"{crypto}"] = {"nbSell": 0}
            self.__nbTrades[f"{crypto}"]["nbSell"] += 1
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

    def addAmountInTrades(self, amount):
        self.__amountInTrades += amount

    def removeAmountInTrades(self, amount):
        self.__amountInTrades -= amount

    def getAmountInTrades(self):
        return self.__amountInTrades

    def getNbTradeCrypto(self) -> dict:
        logger.info(self.__nbTrades)
        return self.__nbTrades
