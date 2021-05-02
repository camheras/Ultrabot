from datetime import datetime

from loguru import logger


class Front:

    def __init__(self, cryptos: list):
        self.cryptos = cryptos
        self.file = open("res/grafana.txt", "a")
        self.file.seek(0)
        self.file.truncate()
        pricecrypto = str(["price " + crypto for crypto in cryptos]).replace("]", "").replace("[", "").replace("\'", "").replace(",", ";").replace("; ", ";")
        nbtradecrypto = str(["nbtrades " + crypto for crypto in cryptos]).replace("]", "").replace("[", "").replace("\'", "").replace(",", ";").replace("; ", ";")
        pvs = str(["pv " + crypto for crypto in cryptos]).replace("]", "").replace("[", "").replace("\'", "").replace(",", ";").replace("; ", ";")
        self.header = f"timestamp;orders;{pricecrypto};{nbtradecrypto};amountintrade;{pvs}"
        self.file.write(f'{self.header}\n')
        self.file.close()

    def write(self, orders: list, amountInTrades: int, prices: list, nbTrades: dict, pvs: list, date=None):
        self.file = open("res/grafana.txt", "a")
        pricecrypto = ""
        plusvalues = ""
        nbTradesCrypto = []
        for id, crypto in enumerate(self.cryptos):
            nbTradesCrypto.append("0;")
        try:
            for i, _ in enumerate(self.cryptos):
                pricecrypto += str(prices[i]) + ";"
                plusvalues += str(pvs[i]) + ";"
        except IndexError as e:
            logger.info(e)

        if not nbTrades == {}:

            for id, crypto in enumerate(nbTrades):
                nb = 0
                try:
                    nb += int(nbTrades[crypto]["nbSell"])
                except KeyError:
                    pass
                try:
                    nb += int(nbTrades[crypto]["nbBuy"])
                except KeyError:
                    pass

                nbTradesCrypto[id] = str(nb) + ";"

        else:
            for id, i in enumerate(self.cryptos):
                nbTradesCrypto[id] = "0;"
                logger.error(nbTradesCrypto)
        if date == None:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tab = ""

        for i in nbTradesCrypto:
            tab += i
        self.file.write(f"{date};{orders};{pricecrypto}{tab.strip(';')};{amountInTrades};{plusvalues.strip(';')}\n")
        self.file.close()
