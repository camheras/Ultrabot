from Indicateur import Indicateur
from OrderBook import OrderBook
from loguru import logger

try:
    logger.add("file.log")

    indicateur = Indicateur()
    orderBook = OrderBook(padding=0.5)

    cryptos = ["XETH", "BTC"]
    # orderBook.addBuyOrder("EOS")
    orderBook.addSellOrder("XLM")
    # while True:
    #     for crypto in cryptos:
    #         if indicateur.canBuy(crypto):
    #             orderBook.addBuyOrder(crypto)
    #         if indicateur.canSell(crypto):
    #             orderBook.addSellOrder(crypto)


except KeyboardInterrupt:
    print('interrupted!')
