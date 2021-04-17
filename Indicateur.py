class Indicateur:
    values = {}

    def __init__(self, values):
        self.values = values

    def __getRSI(self, crypto):
        return 0

    def __getBallinger(self, crypto):
        return 0

    def canBuy(self, crypto):
        if self.__getRSI(crypto) + self.__getBallinger(crypto) == 2:
            print("peu acheter")

    def canSell(self, crypto):
        if self.__getRSI(crypto) + self.__getBallinger(crypto) == -2:
            print("peu vendre")
