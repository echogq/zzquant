# coding: utf-8


def str2int(date):
    """
    日期字符串 '2011-09-11' 变换成 整数 20110911
    日期字符串 '2018-12-01' 变换成 整数 20181201
    :param date: str日期字符串
    :return: 类型int
    """
    # return int(str(date)[0:4] + str(date)[5:7] + str(date)[8:10])
    if isinstance(date, str):
        return int(str().join(date.split('-')))
    elif isinstance(date, int):
        return date


def int2str(int_date):
    """
    类型datetime.datatime
    :param date: int 8位整数
    :return: 类型str
    """
    date = str(int_date)
    if len(date) == 8:
        return str(date[0:4] + '-' + date[4:6] + '-' + date[6:8])
    elif len(date) == 10:
        return date