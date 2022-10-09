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

from .handler import *
