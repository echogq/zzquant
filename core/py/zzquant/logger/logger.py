# coding: utf-8

import os
from logging.handlers import RotatingFileHandler
import logging.handlers

# 日志系统配置
# 1
file_log = os.path.dirname(os.path.abspath(__file__))+".log"
# print(file_log)

# fmt = '%(asctime)s - %(filename)s:%(lineno)s - func: [%(name)s] - %(message)s'
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s'
formatter = logging.Formatter(fmt)

handler_file = RotatingFileHandler(file_log, maxBytes=1024 * 1024 * 10, backupCount=10, encoding='utf-8')  #滚动文件输出
handler_file.setFormatter(formatter)

#
handler_console = logging.StreamHandler()  #往屏幕上输出
handler_console.setFormatter(formatter)  #设置屏幕上显示的格式

log = logging.getLogger(__name__)

# log.addHandler(handler_file)
log.addHandler(handler_console)
log.setLevel(logging.DEBUG)
