#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: handler
# Created on: 9/10/2022

from . import LL_CONFIG, LL_CLT
from nonebot import on_message
from nonebot.adapters.mirai2 import Bot, GroupMessage, MessageSegment

matcher = on_message()

group_index = {}
for dev in LL_CONFIG.i2ll_devices:
    group_index.update({})

@matcher.handle()
async def unlock_by_group_member(bot: Bot, event: GroupMessage):
    group_id = event.get_user_id()
    for dev in LL_CONFIG.i2ll_devices:
        pass

    await matcher.send(MessageSegment.plain("xxx"))


