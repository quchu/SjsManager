#!/usr/bin/env python
# coding:utf-8
import requests
import time
import schedule
import hashlib
import config
from logger import logger

statusCodes = {
    0: '爬虫停止',
    1: '爬虫正在运行',
    3: '爬虫未启动',
    4: '爬虫出现异常',
    5: '爬虫停止中',
    6: '爬虫启动中',
    7: '爬虫已删除'
}

def send_request(action, crawlerId):
    api = config.API_BASE + action
    timeStamp = "%d" % time.time()
    md5 = hashlib.md5()
    md5.update(config.USER_KEY + timeStamp + config.USER_SECRET)
    signature = md5.hexdigest()
    params = {
        "user_key": config.USER_KEY,
        "timestamp": timeStamp,
        "sign": signature,
        "crawler_id": crawlerId
    }
    r = None
    try:
        r = requests.get(api, params=params)
    except Exception, e:
        pass
    count = 0
    while count < 5:
        if not r or (not r.ok) or len(r.content) < 500:
            logger.debug('Re-attempting obtain valid response from [%s]: %d' % (api, count + 1))
            try:
                r = requests.get(api, params=params)
            except Exception, e:
                pass
            count += 1
        else:
            break

    jsonObj =  r.json()
    while int(jsonObj["error_code"]) != 0:
        logger.warn("Failed to request [" + action + "] crawler " + crawlerId + ": " + jsonObj["reason"])
        logger.warn("Request again in %d seconds" % config.REQUEST_INTERVAL)
        time.sleep(config.REQUEST_INTERVAL)
        r = requests.get(api, params=params)
        jsonObj = r.json()
    return jsonObj

def get_crawler_status(crawlerId):
    status = send_request("status", crawlerId)
    code = int(status["data"]["crawler_status"])
    logger.info("Status of crawler %s: %s" % (crawlerId, statusCodes[code]))
    return code


def start_crawler(crawlerId):
    code = get_crawler_status(crawlerId)
    if code == 1:
        logger.info("Crawler %s is already up and running" % crawlerId)
    else:
        logger.info("Starting crawler %s..." % crawlerId)
        status = send_request("start", crawlerId)
        code = int(status["data"]["crawler_status"])
        while code == 6:
            logger.info("Waiting for crawler %s to be fully started... (re-verify in %d secs)" %
                        (crawlerId, config.REQUEST_INTERVAL))
            time.sleep(config.REQUEST_INTERVAL)
            code = get_crawler_status(crawlerId)
        if code == 1:
            logger.info("Successfully started crawler %s" % crawlerId)

    if code != 1:
        logger.warn("Unexpected crawler status: %s" % statusCodes[code])

def stop_crawler(crawlerId):
    code = get_crawler_status(crawlerId)
    if code == 0:
        logger.info("Crawler %s is already stopped" % crawlerId)
    else:
        logger.info("Stopping crawler %s..." % crawlerId)
        status = send_request("stop", crawlerId)
        code = int(status["data"]["crawler_status"])
        while code == 5:
            logger.info("Waiting for crawler %s to be fully stopped... (re-verify in %d secs)" %
                        (crawlerId, config.REQUEST_INTERVAL))
            time.sleep(config.REQUEST_INTERVAL)
            code = get_crawler_status(crawlerId)
        if code == 0:
            logger.info("Successfully stopped crawler %s" % crawlerId)

    if code != 0:
        logger.warn("Unexpected crawler status: %s" % statusCodes[code])

def run_all():
    #stop_all()
    logger.info("Initiating crawler start module...")
    logger.info("%d crawlers are located: %s" % (len(config.CRAWLER), config.CRAWLER))
    for crawlerId in config.CRAWLER:
        # Start crawler
        start_crawler(crawlerId)

def stop_all():
    logger.info("Initiating crawler stop module...")
    logger.info("%d crawlers are located: %s" % (len(config.CRAWLER), config.CRAWLER))
    for crawlerId in config.CRAWLER:
        # Stop crawler
        stop_crawler(crawlerId)

if __name__ == "__main__":
    schedule.every().day.at("22:00").do(run_all)
    while True:
        schedule.run_pending()
        time.sleep(10)

