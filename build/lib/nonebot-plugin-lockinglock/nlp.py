#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: Nonebot-Plugin-LockingLock
# Filename: nlp
# Created on: 2022/10/17


class NlpUnit:

    def __init__(self):
        pass

    def __match_kwds(self, msg: str, kws: set) -> bool:
        ret = False

        for i in kws:
            if i in msg and len(msg) < 4 * len(i):
                ret = True
                break

        return ret

    def is_calling(self, msg) -> bool:
        kws = {"Cody", "cody", "科迪"}

        ret = self.__match_kwds(msg, kws)

        return ret

    def is_unlock(self, msg) -> bool:
        kws = {"开门", "开锁", "开一下锁", "开一下门", "门开一下", "锁开一下"}

        ret = self.__match_kwds(msg, kws)

        if not ret:
            ret = self.which_lock(msg) is not None

        return ret

    def which_lock(self, msg) -> (str, None):
        ret = None
        kws = (("开一下", "的门"),
               ("打开", "的门"),
               ("开一下", "门"),
               ("打开", "门"),
               ("解锁", "的门"),
               ("解锁", "门"))

        for fore, last in kws:
            fi = msg.find(fore)
            li = msg.find(last)
            if li > fi != -1:
                ret = msg[fi + len(fore): li]
                break

        return ret
