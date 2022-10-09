#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: handler
# Created on: 9/10/2022

from . import LL_CONFIG
from nonebot import on_message
from nonebot.adapters.mirai2 import Bot, GroupMessage, MessageSegment
from i2llservice.client import I2LLClient

i2ll_clt = I2LLClient(LL_CONFIG.i2ll_host, LL_CONFIG.i2ll_port, LL_CONFIG.i2ll_psk,
                      watchdog_timeout=LL_CONFIG.i2ll_timeout,
                      max_buffer_size=LL_CONFIG.i2ll_clt_buffer)

msging = on_message()

@msging.handle()
async def unlock_by_group_member(bot: Bot, event: GroupMessage):
    group_id = event.get_user_id()
    for dev in LL_CONFIG.i2ll_devices.keys():
        if dev[]

    await msging.send(MessageSegment.plain("xxx"))


