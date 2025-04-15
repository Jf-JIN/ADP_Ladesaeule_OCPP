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


def listen_broadcast(port=12345):
    # 创建UDP Socket，绑定到所有接口和指定端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))  # 0.0.0.0 表示监听所有网络接口

    print(f"Listening for broadcasts on port {port}...")
    while True:
        data, addr = sock.recvfrom(1024)  # 接收数据（缓冲区大小1024字节）
        message = data.decode()
        if message.startswith("DEVICE_IP:"):
            ip = message.split(":")[1]
            print(f"Received IP from {addr[0]}: {ip}")


if __name__ == "__main__":
    listen_broadcast()
