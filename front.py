from datetime import datetime

from loguru import logger


class Front:

    def __init__(self, cryptos: list):
        self.cryptos = cryptos
        self.file = open("res/graphana.txt", "a")
        self.file.seek(0)
        self.file.truncate()
        pricecrypto = str(["price " + crypto for crypto in cryptos]).replace("]", "").replace("[", "").replace("\'", "").replace(",", ";").replace("; ", ";")
        nbtradecrypto = str(["nbtrades " + crypto for crypto in cryptos]).replace("]", "").replace("[", "").replace("\'", "").replace(",", ";").replace("; ", ";")
        self.header = f"timestamp;orders;{pricecrypto};{nbtradecrypto};amountintrade"
        self.file.write(f'{self.header}\n')
        self.file.close()

    def write(self, orders: list, amountInTrades: int, prices: list, nbTrades: dict):
        self.file = open("res/graphana.txt", "a")
        pricecrypto = ""
        nbTradesCrypto = ""
        try:
            for i, _ in enumerate(self.cryptos):
                logger.error(f"{i, prices[i]}")
                pricecrypto += str(prices[i]) + ";"
        except IndexError as e:
            logger.info(e)

        if not nbTrades == {}:
            for crypto in nbTrades:
                nbTradesCrypto += str(int(nbTrades[crypto]["nbBuy"]) + int(nbTrades[crypto]["nbSell"])) + ";"
        else:
            for i in self.cryptos:
                nbTradesCrypto += "0;"
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logger.info(pricecrypto)
        self.file.write(f"{date};{orders};{pricecrypto}{amountInTrades};{nbTradesCrypto.strip(';')}\n")
        self.file.close()
