#!/usr/bin/env python
# coding:utf-8
USER_KEY = "a335327920-NDUxOTUzNz"
USER_SECRET = "RhMzM1MzI3OTIwMj-28e7fd09cc45195"
API_BASE = "http://www.shenjianshou.cn/restv2/crawler/"
REQUEST_INTERVAL = 30   # Request every 30 seconds
CRAWLER = [
    "33561",    # YHouse
    "33510",    # Enjoy
    "33412",    # Into
    "31474"     # 鲜城
]

LOG_CONFIG = {
    'LOG_TO_FILE': True,
    'LOG_TO_PRINT': True,
    'FILE_PATH': './log/SjsManager.log'
}