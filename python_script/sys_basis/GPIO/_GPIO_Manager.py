
import time

from _EVSE_communication import EVSECommunication


class GPIO_Manager:

    def __init__(self):
        self.evse = EVSECommunication()
        self.__EVSE_Failure = False

    def set_current(self,current):
        self.evse.set_current(current)
# 主程序
if __name__ == "__main__":
    def print_time(current_time):
        print(f"收到时间信号: {current_time}")


    t_thread = TimeThread(interval=1)
    t_thread.signal_currentTime.connect(print_time)  # 连接槽
    t_thread.start()

    try:
        # 主线程继续运行，等待用户手动终止
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("正在停止线程...")
        t_thread.stop()
        t_thread.join()
        print("线程已停止。")
