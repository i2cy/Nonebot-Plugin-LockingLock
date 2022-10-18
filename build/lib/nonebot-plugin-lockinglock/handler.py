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
import time
import random

NOTE_COOLDOWN = 120
CALLING_COOLDOWN = 20

matcher = on_message()

GROUP_INDEX_TREE = {}
for dev in LL_CONFIG.i2ll_devices:
    if LL_CONFIG.i2ll_debug:
        print("loaded device config: ")
        print("   root_topic: {}".format(dev.root_topic))
        print("   alias: {}".format(dev.alias))
        print("   permitted_group: {}".format(dev.permitted_group))
    for group_id in dev.permitted_group:
        if group_id in GROUP_INDEX_TREE:
            GROUP_INDEX_TREE[group_id].append(dev)
        else:
            GROUP_INDEX_TREE.update({group_id: [dev]})

if LL_CONFIG.i2ll_debug:
    print("loaded permitted groups: {}".format(GROUP_INDEX_TREE.keys()))

NLP_PROC = NlpUnit()

CALLING_TS = 0
CALLING_RESPOND_FLAG = False

NOTE_UNLOCK_BY_CMD_TS = 0
NOTE_UNLOCK_BY_PWD_TS = 0


@matcher.handle()
async def unlock_by_group_member(bot: Bot, event: GroupMessage):
    global CALLING_TS, NOTE_UNLOCK_BY_CMD_TS, NOTE_UNLOCK_BY_PWD_TS, CALLING_RESPOND_FLAG
    group_id = event.sender.group.id
    msg = event.get_plaintext()
    if LL_CONFIG.i2ll_debug:
        print("event group id: {}".format(group_id))
        print("NLP calling check: {}".format(NLP_PROC.is_calling(msg)))
        print("NLP unlocking check: {}".format(NLP_PROC.is_unlock(msg)))

    if NLP_PROC.is_calling(msg):
        CALLING_RESPOND_FLAG = False
        CALLING_TS = time.time()

    if CALLING_TS and group_id in GROUP_INDEX_TREE.keys():

        # 解锁
        if NLP_PROC.is_unlock(msg):
            # 当有多个设备时
            if len(GROUP_INDEX_TREE[group_id]) > 1:
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
            # 当只有一个设备时
            else:
                dev = GROUP_INDEX_TREE[group_id][0]

            assert isinstance(dev, Devices)
            dev_clt = LL_CLT.getDeviceClient(dev.root_topic)
            if dev_clt is None:
                await matcher.send(MessageSegment.plain(
                    "服务器上没有查询到主题为”{}“的设备，请管理员检查配置文件".format(dev.root_topic)
                ))
                return

            if dev_clt.isOnline():
                dev_clt.unlock()
                if time.time() - NOTE_UNLOCK_BY_CMD_TS > NOTE_COOLDOWN:
                    NOTE_UNLOCK_BY_CMD_TS = time.time()
                    await matcher.send(MessageSegment.plain(
                        "已提交开门申请，请前往目标设备所控制的门，自然敲击3次以上确认开锁"
                    ))
                    await matcher.send(MessageSegment.plain(
                        "开门申请20秒内有效，请在20秒内执行确认"
                    ))
                    await matcher.send(MessageSegment.plain(
                        "当开锁申请确认后，电机会发出微弱提示声，此时代表正在开门"
                    ))
                    await matcher.send(MessageSegment.plain(
                        "门锁电机拉力略微弱，若锁舌被卡住，可能需要抵（或拉）门以防止锁舌被卡导致电机无法拖动"
                    ))
                else:
                    await matcher.send(MessageSegment.plain(
                        "已提交开门申请"
                    ))

            else:
                code = dev_clt.unlock()
                code = dyn16ToDec(code, 4)

                if time.time() - NOTE_UNLOCK_BY_PWD_TS > NOTE_COOLDOWN:
                    NOTE_UNLOCK_BY_PWD_TS = time.time()
                    await matcher.send(MessageSegment.plain(
                        "门锁设备当前不在线，若设备通电，可通过敲击出以下密码序列开门：\n{}".format(
                            ", ".join(code)
                        )
                    ))
                    await matcher.send(MessageSegment.plain(
                        "密码序列有效时间两分钟，当敲击序列正确识别后，电机会发出微弱提示声，此时代表正在开门"
                    ))
                    await matcher.send(MessageSegment.plain(
                        "门锁电机拉力略微弱，若锁舌被卡住，可能需要抵（或拉）门以防止锁舌被卡导致电机无法拖动"
                    ))
                else:
                    await matcher.send(MessageSegment.plain(
                        "门锁设备当前不在线，若设备通电，可通过敲击出以下密码序列开门：\n{}".format(
                            ", ".join(code)
                        )
                    ))
                CALLING_TS = 0

        # 默认响应
        else:
            if not CALLING_RESPOND_FLAG:
                msg = ["在", "怎么啦", "需要我帮啥", "干嘛", "在的", "在", "干嘛", "在的"]
                await matcher.send(MessageSegment.plain(
                    msg[int(random.random() * len(msg))]
                ))
                CALLING_RESPOND_FLAG = True
