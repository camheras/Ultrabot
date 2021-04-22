import btalib


class BinanceTS:
    df = None

    def __init__(self, df):
        self.df = df

    def bollinger(self):
        self.df['MA20'] = self.df['close'].rolling(window=20).mean()
        self.df['20dSTD'] = self.df['close'].rolling(window=20).std()

        self.df['Upper'] = self.df['MA20'] + (self.df['20dSTD'] * 2)
        self.df['Lower'] = self.df['MA20'] - (self.df['20dSTD'] * 2)
        # self.df[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
        # plt.grid(True)
        # plt.title(' Bollinger Bands')
        # plt.axis('tight')
        # plt.ylabel('Price')
        # plt.savefig('apple.png', bbox_inches='tight')
        return self.df

    def RSI(self, n=14):
        return btalib.rsi(self.df['close'], period=n).df.rsi

    def getPrice(self):
        return self.df['close'].iloc[-1]
