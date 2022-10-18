#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: handler
# Created on: 9/10/2022

from . import LL_CONFIG, LL_CLT
from .nlp import NlpUnit
from .config import Devices
from nonebot import on_message
from nonebot.adapters.mirai2 import Bot, GroupMessage, MessageSegment
from i2llservice.utils import dyn16ToDec

matcher = on_message()

GROUP_INDEX_TREE = {}
for dev in LL_CONFIG.i2ll_devices:
    for group_id in dev.permitted_group:
        if group_id in GROUP_INDEX_TREE:
            GROUP_INDEX_TREE[group_id].append(dev)
        else:
            GROUP_INDEX_TREE.update({group_id: [dev]})

NLP_PROC = NlpUnit()


@matcher.handle()
async def unlock_by_group_member(bot: Bot, event: GroupMessage):
    group_id = event.get_user_id()
    msg = event.get_plaintext()
    if NLP_PROC.is_calling(msg) and group_id in GROUP_INDEX_TREE.keys():

        # unlock
        if NLP_PROC.is_unlock(msg):
            if len(GROUP_INDEX_TREE[group_id]) > 1:  # 当有多个设备时
                which = NLP_PROC.which_lock(msg)
                if which is None:
                    name = ""
                    for i, dev in enumerate(GROUP_INDEX_TREE[group_id]):
                        assert isinstance(dev, Devices)
                        name += "{}. {}\n".format(i + 1, dev.alias[0])

                    await matcher.send(MessageSegment.plain(
                        "当前群组有多个可控LL设备：\n{}".format(name)
                    ))
                    await matcher.send(MessageSegment.plain(
                        "请指定要控制的设备，\n例如“打开{}的门”".format(
                            GROUP_INDEX_TREE[group_id][0].alias[0])
                    ))
                    return

                dev = None
                for ele in GROUP_INDEX_TREE[group_id]:
                    if which in ele.alias:
                        dev = ele
                        break

                if dev is None:
                    name = ""
                    for i, dev in enumerate(GROUP_INDEX_TREE[group_id]):
                        assert isinstance(dev, Devices)
                        name += "{}. {}\n".format(i + 1, dev.alias[0])

                    await matcher.send(MessageSegment.plain(
                        "当前群组有多个可控LL设备：\n{}".format(name)
                    ))
                    await matcher.send(MessageSegment.plain(
                        "但没有任何一个设备的别名叫“{}”，请重新指定".format(which)
                    ))
                    return

            else:
                dev = GROUP_INDEX_TREE[group_id][0]

            assert isinstance(dev, Devices)

            if dev.dev_clt.isOnline():
                dev.dev_clt.unlock()
                await matcher.send(MessageSegment.plain(
                    "已提交开门申请，请前往目标设备所控制的门，自然敲击3次以上确认开锁"
                ))
                await matcher.send(MessageSegment.plain(
                    "开门申请20秒内有效，请在20秒内执行确认"
                ))
                await matcher.send(MessageSegment.plain(
                    "当开锁申请确认后，电机会发出微弱提示声，此时代表正在开门"
                ))

            else:
                code = dev.dev_clt.unlock()
                code = dyn16ToDec(code, 4)

                await matcher.send(MessageSegment.plain(
                    "门锁设备当前不在线，若门锁通电，可通过敲击出以下密码序列开门：\n{}".format(
                        ", ".join(code)
                    )
                ))
                await matcher.send(MessageSegment.plain(
                    "当敲击序列正确识别后，电机会发出微弱提示声，此时代表正在开门"
                ))
