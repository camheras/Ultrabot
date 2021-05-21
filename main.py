import itertools
from time import sleep

from loguru import logger

from mains.mainSimulation import MainSimulation
from strategies.strategies import Levier, IndicateurE

cryptos = ["BTC", "ETH"]
# time_range = "4 hours ago UTC"
time_range = ['1 Apr, 2021', '8 Apr, 2021']
validationPercent = 0.80

levier = Levier.X5

# logger.info(MainSimulation(cryptos, time_range, [IndicateurE.MACD, IndicateurE.Boll70, IndicateurE.RSI30], validationPercent, levier).start())

for indicts in list(itertools.combinations(IndicateurE, 1)):
    sleep(2)
    res = MainSimulation(cryptos, time_range, list(indicts), validationPercent, levier).start()
    logger.info(f"{indicts, res}")

for indicts in list(itertools.combinations(IndicateurE, 2)):
    sleep(2)
    res = MainSimulation(cryptos, time_range, list(indicts), validationPercent, levier).start()
    logger.info(f"{indicts, res}")

for indicts in list(itertools.combinations(IndicateurE, 3)):
    sleep(2)
    res = MainSimulation(cryptos, time_range, list(indicts), validationPercent, levier).start()
    logger.info(f"{indicts, res}")
