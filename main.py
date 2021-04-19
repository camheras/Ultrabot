from binance.client import Client

import binancekey
from Indicateur import Indicateur
from OrderBook import OrderBook
from loguru import logger

try:
    logger.add("file.log")
    cryptos = ["XETH", "BTC"]
    client = Client(binancekey.KEY, binancekey.SECRET)
    indicateur = Indicateur(client, cryptos[1])
    logger.info(indicateur.getBollinger())

    # orderBook = OrderBook(padding=0.5)

    # orderBook.addBuyOrder("EOS")
    # orderBook.addSellOrder("XLM")
    # while True:
    #     for crypto in cryptos:
    #         if indicateur.canBuy(crypto):
    #             orderBook.addBuyOrder(crypto)
    #         if indicateur.canSell(crypto):
    #             orderBook.addSellOrder(crypto)


except KeyboardInterrupt:
    print('interrupted!')
