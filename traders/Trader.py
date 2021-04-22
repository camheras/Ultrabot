class Trader:
    compteur = None
    client = None

    def buy(self, crypto, value):
        pass

    def sell(self, crypto, value):
        pass

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
        pass
