# coding: utf-8

import datetime

import requests

from core.py.zzquant.logger.logger import log
from . import *


class KaipanWatcher(object):
    def __init__(self):
        # 缓存发过的id
        self.cids = []

    g_token = '679e7a62a07fa8fc30e7998fa485761f'  # 有些需要权限的需要抓手机得到eab7d7db70666f2c29f2960f9becb6eb
    g_user_id = 103935  # iphone:103935 android 275940
    g_device_id_mobile = 'ffffffff-d167-a1bf-677a-1ad100000000'  # 设备ID
    g_user_id_mobile = 103935  #
    g_token_mobile = '679e7a62a07fa8fc30e7998fa485761f'

    g_url_now = 'https://pchq.kaipanla.com/w1/api/index.php'  # 实时接口
    g_url_his = 'https://pchis.kaipanla.com/w1/api/index.php'  # 历史接口
    # 统一模拟请求头
    my_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Content-Length': '112',
        'Pragma': 'no-cache',
        'Origin': 'https://www.kaipanla.com',
        'Referer': 'https://www.kaipanla.com/index.php/quotes/plates',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    my_headers_his = {'Host': 'pchis.kaipanla.com'}
    my_headers_his.update(my_headers)
    my_headers_now = {'Host': 'pchq.kaipanla.com'}
    my_headers_now.update(my_headers)

    g_url_now_mobile = 'https://hq.kaipanla.com/w1/api/index.php'  # 实时接口
    g_url_his_mobile = 'https://his.kaipanla.com/w1/api/index.php'  # 实时接口
    my_headers_mobile = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; ZTE C2016 Build/KOT49H)',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip',
    }
    my_headers_now_mobile = {'Host': 'hq.kaipanla.com'}
    my_headers_now_mobile.update(my_headers_mobile)
    my_headers_his_mobile = {'Host': 'his.kaipanla.com'}
    my_headers_his_mobile.update(my_headers_mobile)

    '''
    统一请求
    '''

    def post(self, url, headers, body, attr=None, timeout=5):
        for i in range(3):
            try:
                r = requests.post(url, headers=headers, data=body, timeout=timeout)
                if r.status_code == 200:
                    rs_json = r.json()
                    if attr is not None:
                        return rs_json[attr]
                    else:
                        return rs_json
            except Exception as e:
                print("kaipan http post exception try %s times" % (i + 1), e, body)
                if i >= 2:
                    return None

    def get_msg(self):
        params = {"c": "PCNewsFlash", "a": "GetList", "Index": 0, "st": 8, "UserID": self.g_user_id, "Token": self.g_token}
        url = 'https://pcarticle.kaipanla.com/w1/api/index.php'
        headers_now = {'Host': 'pcarticle.kaipanla.com', "Referer": "https://www.kaipanla.com/index.php/capital/ranking"}
        headers_now.update(self.my_headers)
        response = self.post(url, headers_now, params)
        return response

    def watch_task(self):
        """外部调用定时任务"""
        try:
            msgs = self.get_msg()['List']
            for msg in msgs:
                cid = msg['CID']
                if cid in self.cids:
                    continue
                self.cids.append(cid)

                title = msg['Title']
                content = msg['Content']
                stocks = msg['Stocks']
                # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), title)

                stock_info = ''
                is_importent_news = False
                for stock in stocks:
                    stock_info += "%s （%s" % (stock[1], stock[2]) + "） "
                    pct_str = stock[2]  # -0.46%
                    pct = float(pct_str[:pct_str.index('%')])
                    if pct > 3:
                        is_importent_news = True
                    elif pct < -5:
                        is_importent_news = True
                if len(stock_info) > 0 and is_importent_news:
                    msg = "%s\n相关：%s" % (content, stock_info)
                    log.info(datetime.datetime.now().strftime('%H:%M') + " " + msg)
                else:
                    log.debug("忽略消息：%s" % content)
        except Exception as e:
            log.exception(e)


kaipan_watch = KaipanWatcher()

if __name__ == "__main__":
    kaipan_watch.watch_task()
