import requests
import json
import numpy as np

from pandas import Series, DataFrame, to_datetime


class Stock:
    # 一些常量
    # 数据的结构顺序
    DATE = 0
    OPEN = 1
    CLOSE = 2
    HIGH = 3
    LOW = 4
    VOLUME = 5
    CHANGE_RATE = 7
    VOLUME_CNY = 8

    # 时间段
    DAY = 0
    WEEK = 1
    MONTH = 2

    PERIOD_LIST = {DAY: "day", WEEK: "week", MONTH: "month"}

    def __init__(self, stock_number):
        self.stock_number = stock_number
        self.stock_data = None
        self.session = None

    def get_stock_url(self, period=DAY):
        """获取对应时段的url

        :param period: 时间段,传入Stock.DAY,Stock.WEEK或Stock.MONTH
        :return: 对应时段的url
        """
        return f'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?' \
               f'_var=kline_{self.PERIOD_LIST[period]}qfq&' \
               f'param={self.stock_number},{self.PERIOD_LIST[period]},,,320,qfq&' \
               f'r={np.random.rand()}'

    def get_stock_data(self, period=DAY):
        """获取api数据

        :param period: 时间段,传入Stock.DAY,Stock.WEEK或Stock.MONTH
        :return: 返回从api响应后初步提取的数据,类型为numpy.ndarray
        """
        # 设置会话
        if self.session is None:
            self.session = requests.Session()
        # 生成url
        url = self.get_stock_url(period)
        # 发送请求
        _responses = self.session.get(url)

        # 提取请求数据,返回numpy.ndarray
        # 根据时间段设置置换文本
        _data = _responses.text.replace(f'kline_{self.PERIOD_LIST[period]}qfq=', '')
        _data = json.loads(_data)
        self.stock_data = np.array(_data['data']
                                   [f'{self.stock_number}']
                                   [f'qfq{self.PERIOD_LIST[period]}'])
        return self.stock_data

    @staticmethod
    def to_dataframe(data):
        """ 将Stock.get_stock_data的数据转化为DataFrame,且符合mplfinance的格式

        :param data: 接受从Stock.get_stock_data返回的数据
        :return: DataFrame
        """
        _df = DataFrame({'date': data[:, Stock.DATE],
                         'open': data[:, Stock.OPEN].astype('float'),
                         'high': data[:, Stock.HIGH].astype('float'),
                         'low': data[:, Stock.LOW].astype('float'),
                         'close': data[:, Stock.CLOSE].astype('float'),
                         'volume': data[:, Stock.VOLUME].astype('float'),
                         'volume_cny': data[:, Stock.VOLUME_CNY].astype('float')})
        _df.set_index(['date'], inplace=True)
        _df.index = to_datetime(Series(_df.index))
        return _df
