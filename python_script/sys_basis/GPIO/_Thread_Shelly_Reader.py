from logging import exception

import requests
import traceback

class GetShellyData:


# 替换为实际的 Shelly 3EM 设备 IP 地址
shelly_ip = "192.168.1.100"
emeter_index = 0  # 通道索引：0、1 或 2
emeter_url = f"http://{shelly_ip}/emeter/{emeter_index}"

try:
#请求失败后的处理
    response = requests.get(emeter_url, timeout=5)
    response.raise_for_status()
    data = response.json()
    print(f"通道 {emeter_index} 的电能数据：", data)
except requests.exceptions.RequestException as e:
    print(f"请求失败: {traceback.format_exc()}")
#except Exception 断连，重连等等

# 假设已经获取了 emeter 数据
voltage = data.get("voltage")
current = data.get("current")
power = data.get("power")
print(f"电压: {voltage} V, 电流: {current} A, 功率: {power} W")
