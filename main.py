from mains.mainSimulation import MainSimulation
from strategies.strategies import Levier, Indicateur

cryptos = ["BTC", "ETH"]
time_range = "8 hours ago UTC"
strat = {'indicateurs': [Indicateur.RSI, Indicateur.Bollinger], 'levier': Levier.X5}

MainSimulation(cryptos, time_range).start()
