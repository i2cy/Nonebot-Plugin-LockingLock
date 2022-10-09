#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: config
# Created on: 1/10/2022

"""
config.i2ll_host
config.i2ll_port
config.i2ll_psk
config.i2ll_devices
"""

from pydantic import BaseSettings, BaseModel, Extra
from typing import List


class Devices(BaseModel, extra=Extra.ignore):

    alias: List[str] = []
    root_topic: str
    permitted_group: List[int]


class Config(BaseSettings, extra=Extra.ignore):

    i2ll_host: str = "127.0.0.1"
    i2ll_port: int = 8421
    i2ll_psk: str = "i2tcppsk"
    i2ll_clt_buffer: int = 20
    i2ll_timeout: int = 15
    i2ll_devices: List[Devices] = []
