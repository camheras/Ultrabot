from traders.Trader import Trader
from loguru import logger


class Simulation(Trader):
    compteur = None
    client = None
    balance = 1000
    tokens = []

    def __init__(self):
        pass

    def buy(self, crypto, value):
        logger.info(f"BUY {crypto, value}")
        done = False
        for token in self.tokens:
            if token["token"] == crypto:
                token["amount"] += value
                done = True
                break
        if not done:
            self.tokens.append(
                {'token': crypto,
                 'amount': value})
        self.balance -= value

    def sell(self, crypto, value):
        logger.info(f"SELL {crypto, value}")
        done = False
        for token in self.tokens:
            if token["token"] == crypto:
                if token["amount"] - value > 0:
                    token["amount"] -= value
                    done = True
                    break
        if not done:
            logger.error(f"Attempt to sell not owned crypto ({value} {crypto})")
        self.balance += value

    # donne le nombre de tokens avec la valeur en $
    def montant(self, crypto, amount):
        for token in self.tokens:
            if token["token"] == crypto:
                return amount / float(token["amount"])

        logger.error("Token not owned")

    # Recupere le nombre de tokens possédé
    def getAmount(self, crypto):
        for token in self.tokens:
            if token["token"] == crypto:
                return float(token["amount"])

    def getBalance(self):
        return self.balance

    def getTokens(self):
        return self.tokens
