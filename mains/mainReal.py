import time
from datetime import datetime
from time import sleep

from binance.client import Client
from loguru import logger

from Compteur import Type
from front.front import Front
from indicateurs.Indicateur import Indicateur
from OrderBook import OrderBook
from res import binancekey

try:
    logger.add("res/file.log")
    cryptos = ["BTC", "ETH"]
    front = Front(cryptos)
    client = Client(binancekey.KEY, binancekey.SECRET)

    orderBook = OrderBook(cryptos)

    # TODO faire une simulation sur les données passées
    while True:
        sleep(7.0)
        # TODO ajouter un truc pour le timeout ?
        start = time.process_time()
        prices = []
        for crypto in cryptos:
            indicateur = Indicateur(client, crypto)
            result = indicateur.result()
            # logger.info(result)
            price = indicateur.getPrice()
            prices.append(price)

            if result and orderBook.compteur.canBuyDown(crypto):  # Si le cours est HAUT
                logger.info(f"BUY {crypto, price, Type.DOWN}")
                orderBook.addBuyOrder(crypto, price, Type.DOWN)
            elif result and orderBook.compteur.canSellUp(crypto):
                logger.info(f"SELL {crypto, price, Type.UP}")
                orderBook.addSellOrder(crypto, price)
            elif result == False and orderBook.compteur.canSellDown(crypto):  # Si le cours est BAS
                logger.info(f"SELL {crypto, price, Type.DOWN}")
                orderBook.addSellOrder(crypto, price)
            elif result == False and orderBook.compteur.canBuyUp(crypto):
                logger.info(f"BUY {crypto, price, Type.UP}")
                orderBook.addBuyOrder(crypto, price, Type.UP)

            logger.info(f"{crypto} - {orderBook.compteur.getNbTrade(), indicateur.getBollinger(), indicateur.getRSI()} ")

        end = time.process_time()
        front.write(orderBook.compteur.getOrders(), orderBook.compteur.getAmountInTrades(), prices, orderBook.compteur.getCryptoBook())

except KeyboardInterrupt:
    logger.info(orderBook.compteur.getNbTrade())
    print('interrupted!')
