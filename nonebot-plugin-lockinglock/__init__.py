#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: __init__
# Created on: 1/10/2022

from nonebot import get_driver

from .config import Config

GLOBAL_CONFIG = get_driver().config
LL_CONFIG = Config.parse_obj(GLOBAL_CONFIG)

# validate config
device_dict = LL_CONFIG.i2ll_devices
for dev in device_dict.keys():
    assert dict(device_dict[dev])

from .handler import *
