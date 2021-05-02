from enum import Enum


class Indicateur(Enum):
    RSI = "RSI"
    Bollinger = "Bollinger"


class Levier(Enum):
    X1 = 1
    X5 = 5
    X10 = 10
    X15 = 15
    X20 = 20
    x25 = 25
    x30 = 30
