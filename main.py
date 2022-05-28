import itertools
from time import sleep

from binance.client import Client
from loguru import logger

from binanceTS import BinanceTS
from indicateurs.Indicateur import Indicateur
from mains.mainSimulation import MainSimulation
from res import binancekey
from strategies.strategies import Levier, IndicateurE

cryptos = ["BTC", "EOS"]
# time_range = "4 hours ago UTC"
# time_range = ['16 Jun, 2020', '16 Jun, 2021']
time_range = ['1 Jun, 2021', '16 Jun, 2021']
validationPercent = 0.80

levier = Levier.X15
data = {}

client = Client(binancekey.KEY, binancekey.SECRET)

for crypto in cryptos:
    data[f"{crypto}"] = Indicateur(client, crypto, periode=time_range).df
    # df = Indicateur(self.client, crypto, periode=self.time_range).df
    df = data[f"{crypto}"]
    bin = BinanceTS(df)
    df['rsi'] = bin.RSI()
    df['signal'] = bin.MACD()[1].series
    df['macd'] = bin.MACD()[0].series
    df['ema'] = bin.EMA200()[0]
    bin.bollinger()
    # bin.donchian()
    df = df[['close', 'rsi', 'Upper', 'Lower', 'signal', 'macd', 'ema']]
    data[f"{crypto}"] = df

logger.info(MainSimulation(cryptos, time_range, [IndicateurE.EMA200, IndicateurE.Boll80, IndicateurE.RSI25], validationPercent, data, levier).start())

# for indicts in list(itertools.combinations(IndicateurE, 1)):
#     # sleep(2)
#     res = MainSimulation(cryptos, time_range, list(indicts), validationPercent, data, levier).start()
#     logger.info(f"{[i.value for i in indicts], res}")
#
# for indicts in list(itertools.combinations(IndicateurE, 2)):
#     # sleep(2)
#     res = MainSimulation(cryptos, time_range, list(indicts), validationPercent, data, levier).start()
#     logger.info(f"{[i.value for i in indicts], res}")
#
# for indicts in list(itertools.combinations(IndicateurE, 3)):
#     # sleep(2)
#     res = MainSimulation(cryptos, time_range, list(indicts), validationPercent, data, levier).start()
#     logger.info(f"{[i.value for i in indicts], res}")
