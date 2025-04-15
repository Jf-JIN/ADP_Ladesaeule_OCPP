import os
import sys
import pprint
import socket
from DToolslib import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket
import time


# def get_ip():
#     # 获取本机IP地址（适用于有网络连接的情况）
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         s.connect(("8.8.8.8", 80))  # 连接一个外部服务器，无需实际通信
#         ip = s.getsockname()[0]
#     except Exception:
#         ip = "127.0.0.1"  # 失败时返回本地回环地址
#     finally:
#         s.close()
#     return ip


# def broadcast_ip(port=12345, interval=5):
#     # 创建UDP Socket，并启用广播模式
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#     while True:
#         ip = get_ip()
#         message = f"DEVICE_IP:{ip}".encode()
#         # 向局域网广播地址发送消息
#         sock.sendto(message, ('255.255.255.255', port))
#         print(f"Broadcasted IP: {ip}")
#         time.sleep(interval)  # 每隔 interval 秒广播一次


# if __name__ == "__main__":
#     broadcast_ip()


import requests
import subprocess

import requests
import subprocess
import platform


def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"


def get_ssid():
    system = platform.system()
    try:
        if system == "Linux":
            ssid = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        elif system == "Windows":
            command = "netsh wlan show interfaces | findstr SSID"
            output = subprocess.check_output(command, shell=True).decode("gbk").strip()
            ssid = output.split(":")[1].strip()
        else:
            ssid = "Unsupported OS"
        return ssid
    except Exception as e:
        return f"Error: {str(e)}"


public_ip = get_public_ip()
ssid = get_ssid()

webhook_url = "https://webhook.site/abcd1234..."
while True:
    requests.post(webhook_url, json={
        'ip': public_ip,
        'ssid': ssid
    })

requests.post(webhook_url, json={
    'ip': public_ip,
    'ssid': ssid
})
