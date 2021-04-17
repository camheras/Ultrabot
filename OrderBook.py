# ici on a toutes les stats
import datetime

import krakenex

from Compteur import Compteur
from TraderKraken import TraderKraken

from loguru import logger


class OrderBook:
    trader = None
    compteur = None
    padding = 0
    balance = 0

    def __init__(self, padding):

        self.trader = TraderKraken()
        self.compteur = Compteur()
        self.balance = self.trader.getBalance()
        self.padding = padding

    def addBuyOrder(self, crypto):

        amount = self._getAvailableMoney()
        currentPrice = self.trader.buy(crypto, amount)
        self.compteur.buyOrder()
        self.compteur.addOrder({
            'crypto': f'{crypto}',
            'buyPrice': currentPrice,
            'sellPrice': '',
            'value': f'{float(amount) * float(currentPrice)}$',
            'timestamp': f'{datetime.datetime.now()}',
        })

    def addSellOrder(self, crypto):

        amount = self.trader.getAmount(crypto)
        logger.info(f'Selling {amount} {crypto}')
        if amount > 0:
            currentPrice = self.trader.sell(crypto, amount)
            self.compteur.sellOrder()
            self.compteur.addOrder({
                'crypto': f'{crypto}',
                'buyPrice': '',
                'sellPrice': currentPrice,
                'value': f'{float(amount) * float(currentPrice)}$',
                'timestamp': f'{datetime.datetime.now()}',
            })
        else:
            logger.error(f"Can't sell, {crypto} balance is not enough.")

    def _getAvailableMoney(self):
        amount_in_orders = 0
        for order in self.compteur.getOrders():
            if order['open']:
                amount_in_orders += order['value']
        return (float(amount_in_orders) + float(self.balance)) * self.padding
