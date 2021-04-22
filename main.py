from time import sleep

from binance.client import Client

from res import binancekey
from Indicateur import Indicateur
from OrderBook import OrderBook
from loguru import logger
import time
import dash
import dash_core_components as dcc
import dash_html_components as html

from traders.Simulation import Simulation

try:

    logger.add("res/file.log")
    cryptos = ["ETH", "BTC"]
    client = Client(binancekey.KEY, binancekey.SECRET)
    indicateur = Indicateur(client, cryptos[1])

    orderBook = OrderBook(indicateur=indicateur)
    # TODO faire une simulation sur les données passées
    while True:
        sleep(5.0)
        start = time.process_time()
        for crypto in cryptos:
            indicateur = Indicateur(client, crypto)
            result = indicateur.result()
            # logger.info(result)
            if result:
                orderBook.addBuyOrder(crypto)
            elif result == False:
                orderBook.addSellOrder(crypto)

        end = time.process_time()
        logger.info(orderBook.compteur.getNbTrade())

except KeyboardInterrupt:
    logger.info(orderBook.compteur.getOrders())
    print('interrupted!')
