import mplfinance as mpf

from Stock import Stock

if __name__ == '__main__':
    # 初始化
    stock_number = 'sz000001'
    stock = Stock(stock_number)
    # 指定时间段
    period = Stock.DAY
    data = stock.get_stock_data(period)
    # 转为DataFrame
    df = Stock.to_dataframe(data)
    # 写入csv
    # df.to_csv(f'{stock_number}_{Stock.PERIOD_LIST[period]}.csv')

    # 设置K线样式
    my_colors = mpf.make_marketcolors(up='r',
                                      down='g',
                                      edge='inherit',
                                      wick='inherit',
                                      volume='inherit')
    my_style = mpf.make_mpf_style(marketcolors=my_colors)

    # 绘制
    mpf.plot(df,
             type='candle',
             mav=(5, 10, 20),
             volume=True,
             datetime_format='%Y-%m-%d',
             style=my_style)
