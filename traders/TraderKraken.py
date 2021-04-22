from requests.exceptions import HTTPError
from loguru import logger
import krakenex

from Compteur import Compteur
from traders.Trader import Trader


class TraderKraken(Trader):
    compteur = None
    k = krakenex.API()

    def __init__(self):
        self.k.load_key('kraken.key')
        self.compteur = Compteur()

    def buy(self, crypto, value):
        cost = ""
        self.compteur.buyFees(cost)
        amount = self.montant(crypto, value)
        params = {
            'pair': f'{crypto}USDT',
            'type': 'buy',
            'ordertype': 'market',
            'volume': amount
        }
        logger.info(self.k.query_private('AddOrder', params))

        return self.montant(crypto, amount)

    def sell(self, crypto, value):
        # ++ compteur fees

        amount = self.montant(crypto, value)
        params = {
            'pair': f'{crypto}USDT',
            'type': 'sell',
            'ordertype': 'market',
            'volume': amount
        }
        logger.info(self.k.query_private('AddOrder', params))

        return self.montant(crypto, amount)

    # donne le nombre de tokens avec la valeur en $
    def montant(self, crypto, amount):
        current_price = self.getPrice(crypto)
        return round(float(amount) / float(current_price), 6)

    # recupere le prix de la crypto
    def getPrice(self, crypto):
        return self.k.query_public('Ticker', {'pair': f'{crypto}USDT'})['result'][f'{crypto}USDT']['a'][0]

    # Recupere le nombre de tokens possédé
    def getAmount(self, crypto):
        try:
            logger.info(f"{crypto}, {self.k.query_private('Balance')['result'][f'{crypto}']}")
            return self.k.query_private('Balance')['result'][f'{crypto}']
        except KeyError:
            logger.warning(f"{crypto} balance is empty")
            return 0

    def getBalance(self):
        return self.k.query_private('Balance')['result']['USDT']
