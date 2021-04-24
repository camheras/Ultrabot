import time
from datetime import datetime
from time import sleep

from binance.client import Client
from loguru import logger

from front import Front
from indicateurs.Indicateur import Indicateur
from OrderBook import OrderBook
from res import binancekey

try:

    logger.add("res/file.log")
    cryptos = ["BTC", "ETH"]
    front = Front(cryptos)
    client = Client(binancekey.KEY, binancekey.SECRET)
    indicateur = Indicateur(client, cryptos[0])

    orderBook = OrderBook(indicateur=indicateur)
    # TODO faire une simulation sur les données passées
    while True:
        sleep(5.0)
        start = time.process_time()
        prices = []
        for crypto in cryptos:

            indicateur = Indicateur(client, crypto)
            result = indicateur.result()
            # logger.info(result)
            prices.append(indicateur.getPrice())
            if result:
                orderBook.addBuyOrder(crypto)
            elif result == False:
                orderBook.addSellOrder(crypto)

        end = time.process_time()
        front.write(orderBook.compteur.getOrders(), orderBook.compteur.getAmountInTrades(), prices, orderBook.compteur.getNbTradeCrypto())

        logger.info(f"{orderBook.compteur.getNbTrade(), indicateur.getBollinger(), indicateur.getRSI()} ")

except KeyboardInterrupt:
    logger.info(orderBook.compteur.getNbTrade())
    print('interrupted!')
