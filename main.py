import time
from datetime import datetime
from time import sleep

from binance.client import Client
from loguru import logger

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
            prices.append(indicateur.getPrice())
            if result and orderBook.compteur.canBuy(crypto):
                orderBook.addBuyOrder(crypto,indicateur.getPrice())
            elif result == False and orderBook.compteur.canSell(crypto):
                orderBook.addSellOrder(crypto,indicateur.getPrice())
            logger.info(f"{crypto} - {orderBook.compteur.getNbTrade(), indicateur.getBollinger(), indicateur.getRSI()} ")

        end = time.process_time()
        front.write(orderBook.compteur.getOrders(), orderBook.compteur.getAmountInTrades(), prices, orderBook.compteur.getCryptoBook())

except KeyboardInterrupt:
    logger.info(orderBook.compteur.getNbTrade())
    print('interrupted!')
