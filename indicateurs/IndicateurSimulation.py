from binance.client import Client

from indicateurs.Indicateur import Indicateur
from res import binancekey

client = Client(binancekey.KEY, binancekey.SECRET)
df = Indicateur(client=client, crypto="BTC")

