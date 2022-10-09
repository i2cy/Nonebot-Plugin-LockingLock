#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: __init__
# Created on: 1/10/2022

from nonebot import get_driver
from nonebot.matcher import Matcher
from i2llservice.client import I2LLClient

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


