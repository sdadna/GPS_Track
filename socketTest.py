#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块

s = socket.socket()         # 创建 socket 对象
host = "1938552zb4.imwork.net" # 获取本地主机名
port = 21529                # 设置端口好

s.connect((host, port))
print s.send("asdfddddd")
s.close()  