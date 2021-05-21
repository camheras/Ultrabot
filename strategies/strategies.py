from decimal import Decimal
from enum import Enum


class IndicateurE(Enum):
    Boll60 = "Bollinger60"
    Boll70 = "Bollinger70"
    Boll80 = "Bollinger80"
    MACD = "MACD"
    MACDzeroed = "MACDzeroed"
    EMA200 = "EMA200"
    Donchian = "Donchian"
    RSI30 = "RSI30"
    RSI35 = "RSI35"
    RSI25 = "RSI25"


class Levier(Enum):
    X1 = Decimal(1)
    X5 = Decimal(5)
    X10 = Decimal(10)
    X15 = Decimal(15)
    X20 = Decimal(20)
    X25 = Decimal(25)
    X30 = Decimal(30)
    X50 = Decimal(50)
