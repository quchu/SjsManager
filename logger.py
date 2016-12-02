#!/usr/bin/env python
# coding:utf-8
import logging
from config import LOG_CONFIG


def get_logger():
    logger = logging.getLogger('SjsManager')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        # logging format
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
        # file handler
        if LOG_CONFIG['LOG_TO_FILE']:
            fh = logging.FileHandler(LOG_CONFIG['PATH'])
            fh.setFormatter(fmt)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
        # stream handler
        if LOG_CONFIG['LOG_TO_PRINT']:
            ch = logging.StreamHandler()
            ch.setFormatter(fmt)
            ch.setLevel(logging.INFO)
            logger.addHandler(ch)
    return logger


logger = get_logger()