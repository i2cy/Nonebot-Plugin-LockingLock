#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Project: NonebotPluginLockingLock
# Filename: setup
# Created on: 1/10/2022

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugin-lockinglock",  # Replace with your own username
    version="0.1.0",
    author="I2cy Cloud",
    author_email="i2cy@outlook.com",
    description="Locking Lock remote controller plugin based on Nonebot standard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i2cy/Nonebot-Plugin-LockingLock",
    project_urls={
        "Bug Tracker": "https://github.com/i2cy/Nonebot-Plugin-LockingLock/issues",
        "Source Code": "https://github.com/i2cy/Nonebot-Plugin-LockingLock",
        "Documentation": "https://github.com/i2cy/Nonebot-Plugin-LockingLock/master/README.md"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'i2cylib>=1.12.1',
        'i2llserver>=1.1.0',
        'nonebot2',
        'nonebot-adapter-mirai2'
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    entry_points={'console_scripts':
        [

        ]
    }
)
