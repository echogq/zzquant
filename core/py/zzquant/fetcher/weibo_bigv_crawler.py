# coding: utf-8

import requests
import datetime
import numpy as np
import pandas as pd
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from core.py.zzquant.logger.logger import log


def is_work_time():
    now = datetime.datetime.now()
    #     print(now.day)
    day = now.weekday()
    if day in [5, 6]:
        return False
    hour = now.hour
    minute = now.minute
    if 8 <= hour <= 20:
        return True
    #     elif hour == 10:
    #         return True
    #     elif hour == 11:
    #         return minute <= 40
    #     elif hour == 13:
    #         return True
    #     elif hour == 14:
    #         return True
    #     elif hour == 15:
    #         return minute <10
    return False

class WeiBoWatcher():
    cids = []
    base_url = 'https://m.weibo.cn/api/container/getIndex?'

    headers = {
        'Host': 'm.weibo.cn',
        'Referer': 'https://m.weibo.cn/u/2145291155',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # https://m.weibo.cn/u/1216826604 里面点击微博，然后控制台搜索 containerid 找第二个链接如下(containerid1076开头)
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1896820725&containerid=1076031896820725
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=5828706619&containerid=1076035828706619
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1216826604&containerid=1076031216826604
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=5447592608&containerid=1076035447592608
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=3714420514&containerid=1076033714420514 股市狼头哥
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1908364672&containerid=1076031908364672 老妖观察
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=2272536674&containerid=1076032272536674 佛系复利
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1525844264&containerid=1076031525844264 胡斐-戊午
    # https://m.weibo.cn/statuses/extend?id=4354125455913122
    # 拼接url
    def get_page(self, page, uid, containerid):
        #     print('Hi')
        # 查询字符串
        params = {
            'type': 'uid',
            'value': uid,
            'containerid': containerid,
            'page': page
        }
        # 调用urlencode() 方法将params参数转化为 URL 的 GET请求参数
        url = self.base_url + urlencode(params)
        print(url)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError as e:
            print('Error', e.args)

    # 获取全文数据
    def get_text_full(self, t_id):
        url = 'https://m.weibo.cn/statuses/extend?id=' + str(t_id)
        #     print(url)
        response = requests.get(url, headers=self.headers).json()
        longText = response.get('data')['longTextContent']
        return longText

    # 解析数据
    def parse_page(self, json):
        if json:
            items = json.get('data').get('cards')
            for index, item in enumerate(items):
                if item.get('card_type') != 9:
                    continue
                item = item.get('mblog')
                weibo = dict()
                weibo['created_at'] = item.get('created_at')
                weibo['id'] = item.get('id')
                #                 weibo['text'] = pq(item.get('text')).text()

                weibo['text'] = item.get('text')
                if 'page_info' in item:
                    page_info = item.get('page_info')
                    #                 print(page_info.get('page_url'))
                    weibo['text'] = weibo['text'] + ":" + page_info.get('page_url')
                if 'status' in weibo['text']:
                    soup = BeautifulSoup(weibo['text'], 'html.parser')
                    a = soup.find_all('a')
                    if len(a) > 0:
                        #                     print('get_text_full:',a[0]['href'])
                        if '/status' in a[0]['href'] and weibo['created_at'] == '刚刚':
                            #                     if '/status' in a[0]['href']:
                            text_full = self.get_text_full(a[0]['href'][8:])
                            #                         print(text_full)
                            weibo['text'] = text_full
                weibo['text'] = pq(weibo['text']).text()
                weibo['attitudes_count'] = item.get('attitudes_count')
                weibo['comments_count'] = item.get('comments_count')
                weibo['reposts_count'] = item.get('reposts_count')
                yield weibo

    def get_weibo_msg_bingchuan(self, debug=False):
        json = self.get_page(1, '5447592608', '1076035447592608')
        user_name = '冰'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_guxia(self, debug=False):
        json = self.get_page(1, '1896820725', '1076031896820725')
        user_name = '股侠'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_longge(self, debug=False):
        json = self.get_page(1, '5828706619', '1076035828706619')
        user_name = '龙'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_wu(self, debug=False):
        json = self.get_page(1, '1216826604', '1076031216826604')
        user_name = 'wu'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_feierchaogu(self, debug=False):
        json = self.get_page(1, '6502768427', '1076036502768427')
        user_name = '菲'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_yu(self, debug=False):
        json = self.get_page(1, '2821710245', '1076032821710245')
        user_name = '雨'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_bjchaojia(self, debug=False):
        json = self.get_page(1, '5994598191', '1076035994598191')
        user_name = '北'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_foxifuli(self, debug=False):
        json = self.get_page(1, '2272536674', '1076032272536674')
        user_name = '佛系'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def get_weibo_msg_hufei(self, debug=False):
        json = self.get_page(1, '1525844264', '1076031525844264')
        user_name = '胡斐'
        cards = self.parse_page(json)
        self.analyze_msg(cards, user_name, debug)

    def analyze_msg(self, cards, user_name, debug=False):
        idx = 0
        for card in cards:
            if card is None:
                continue
            idx += 1
            if idx > 3:
                break
            cid = card['id']
            if not debug and cid in self.cids:
                continue
            self.cids.append(cid)
            msg = card['text']
            created_at = card['created_at']
            msg_for_send = user_name + ":" + msg
            print(created_at, msg_for_send)
            if created_at == '刚刚' and len(msg) > 10 and '没有任何Q群' not in msg:
                if not debug:
                    if user_name in ['wu', '龙', '冰', '北', '佛系', '胡斐']:
                        if user_name in ['胡斐']:
                            if "股票操盘宝典" in msg:
                                continue
                        log.info(msg_for_send)
                    elif user_name in ['狼', '股侠', '雨', '菲']:
                        log.debug(msg_for_send)
                else:
                    print("忽略", 'user_name', msg_for_send)

    def watch_task(self):
        """外部调用定时任务"""
        try:
            self.get_weibo_msg_longge()
            if is_work_time():
                self.get_weibo_msg_wu()
            self.get_weibo_msg_bingchuan()
            self.get_weibo_msg_yu()
            self.get_weibo_msg_guxia()
            self.get_weibo_msg_bjchaojia()
            self.get_weibo_msg_feierchaogu()
            self.get_weibo_msg_foxifuli()
            self.get_weibo_msg_hufei()
        except Exception as e:
            log.exception(e)


weibo_watch = WeiBoWatcher()

if __name__ == "__main__":
    weibo_watch.get_weibo_msg_foxifuli()
