import talib

from Stock import Stock


class StockTest:
    PERIOD_LIST = {Stock.DAY: "day", Stock.WEEK: "week", Stock.MONTH: "month"}

    def __init__(self, stock_number, period=Stock.DAY):
        # 初始化
        self.stock_number = stock_number
        self.period = period
        stock = Stock(stock_number)
        # 指定获取指定K线
        self.data = stock.get_stock_data(period)
        # 转为DataFrame
        self.df = Stock.to_dataframe(self.data)
        print(self.df)

    def get_data(self):
        return self.data

    def get_dataframe(self):
        return self.df

    def to_csv(self):
        # 写入csv
        self.df.to_csv(f'{self.stock_number}_{self.PERIOD_LIST[self.period]}.csv')

    def test_ma(self):
        ma_5 = talib.MA(self.df['close'], 5)
        for i, j in zip(self.df['date'].values, ma_5):
            print(f'{i} {j:10.2f}')

    def test_macd(self):
        diff, dea, macd = talib.MACD(self.df['close'])
        macd = macd * 2
        for date, i, j, k in zip(self.df['date'], diff.values, dea.values, macd.values):
            print(f'{date}   diff:{i:.2f}   dea:{j:.2f}   macd:{k:.2f}')


if __name__ == '__main__':
    stock_number = 'sz000001'
    s = StockTest(stock_number)
    s.test_ma()
    s.test_macd()
