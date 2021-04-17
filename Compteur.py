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

    def buyOrder(self):
        self.__nbBuy += 1

    def sellOrder(self):
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
        return (self.__nbBuy - self.__nbSell) / self.__nbBuy

    def getTotalFees(self):
        return self.__nbBuyFees + self.__nbSellFees
