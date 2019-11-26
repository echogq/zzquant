# coding: utf-8

"""
上证交易所，深圳交易所获取数据

融资融券：
http://www.sse.com.cn/market/othersdata/margin/sum/
http://www.szse.cn/disclosure/margin/margin/index.html

"""
from core.py.zzquant.util import date_util
import pandas as pd

_sh_url = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk{}.xls'
_sz_url = 'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1837_xxpl&txtDate=2019-11-25&tab2PAGENO=1&random=0.14609649785655132&TABKEY=tab2'


def get_sh_margin(date):
    """return shanghai margin data

    Arguments:
        date {str YYYY-MM-DD} -- date format

    Returns:
        pandas.DataFrame -- res for margin data
    """
    data = pd.read_excel(_sh_url.format(date_util.str2int(date)), 1).assign(date=date).assign(sse='sh')
    # data.columns = ['code', 'name', 'leveraged_balance', 'leveraged_buyout', 'leveraged_payoff', 'margin_left', 'margin_sell', 'margin_repay', 'date', 'sse']
    return data


def get_sz_margin(date):
    """return shenzhen margin data

    Arguments:
        date {str YYYY-MM-DD} -- date format

    Returns:
        pandas.DataFrame -- res for margin data
    """

    return pd.read_excel(_sz_url.format(date)).assign(date=date).assign(sse='sz')


if __name__ == "__main__":
    print(get_sh_margin('2019-11-25'))
    print(get_sz_margin('2019-11-25'))
