#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: __init__
# Created on: 1/10/2022

from nonebot import get_driver
from i2llservice.client import I2LLClient
from .config import Config
from i2cylib.utils.logger import Logger

DRIVER = get_driver()
GLOBAL_CONFIG = DRIVER.config
LL_CONFIG = Config.parse_obj(GLOBAL_CONFIG)

if LL_CONFIG.i2ll_debug:
    print("test i2ll config:")
    print(" i2ll_host: {}".format(LL_CONFIG.i2ll_host))
    print(" i2ll_port: {}".format(LL_CONFIG.i2ll_port))
    print(" i2ll_psk: {}".format(LL_CONFIG.i2ll_psk))
    print(" i2ll_timeout: {}".format(LL_CONFIG.i2ll_timeout))
    print(" i2ll_buffer_size: {}".format(LL_CONFIG.i2ll_clt_buffer))
    print(" i2ll_devices: {}".format(LL_CONFIG.i2ll_devices))
    logger = Logger(level="DEBUG")
else:
    logger = Logger(level="INFO")

LL_CLT = I2LLClient(LL_CONFIG.i2ll_host, LL_CONFIG.i2ll_port, LL_CONFIG.i2ll_psk,
                    watchdog_timeout=LL_CONFIG.i2ll_timeout,
                    max_buffer_size=LL_CONFIG.i2ll_clt_buffer)


def i2ll_init():
    global LL_CLT
    LL_CLT.connect(15)
    len(LL_CLT)


def i2ll_stop():
    global LL_CLT
    LL_CLT.reset()


DRIVER.on_startup(i2ll_init)
DRIVER.on_shutdown(i2ll_stop)

from .handler import *
