<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-lockinglock

_✨ [LockingLock 查看插件](https://github.com/i2cy/Nonebot-Plugin-LockingLock) ✨_

</div>

<p align="center">
  <a href="https://github.com/i2cy/Nonebot-Plugin-LockingLock/master/LICENSE">
    <img src="https://img.shields.io/github/license/i2cy/Nonebot-Plugin-LockingLock.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-lockinglock">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-lockinglock.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">
</p>

## 配置项

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。

### 默认配置模板
    i2ll_host="127.0.0.1"
    i2ll_port=8421
    i2ll_psk="i2tcppsk"
    i2ll_clt_buffer=20
    i2ll_timeout=15
    i2ll_devices:“
    [
        {
            alias: ["test_device"],
            root_topic: "esp32test/test_device",
            permitted_group: [123456788]
        }
    ]
    ”