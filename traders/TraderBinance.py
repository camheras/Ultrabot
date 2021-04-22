from binance.client import Client

from res import binancekey

from Compteur import Compteur
from traders.Trader import Trader


class TraderBinance(Trader):
    compteur = None
    client = None

    def __init__(self):
        self.client = Client(binancekey.KEY, binancekey.SECRET)
        self.compteur = Compteur()

    def buy(self, crypto, value):
        return None

    def sell(self, crypto, value):
        return None

    # donne le nombre de tokens avec la valeur en $
    def montant(self, crypto, amount):
        pass

    # recupere le prix de la crypto
    def getPrice(self, crypto):
        pass

    # Recupere le nombre de tokens possédé
    def getAmount(self, crypto):
        pass

    def getBalance(self):
        return 1000
