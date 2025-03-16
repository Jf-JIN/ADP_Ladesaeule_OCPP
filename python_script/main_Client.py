#! /usr/bin/python3.11

from server.Client import Client
import atexit
import os
import signal
import sys


class main(object):
    def __init__(self):
        self._exit_flag = False  # 防止重复清理
        self.client = Client()

        # 注册退出处理
        atexit.register(self.cleanup)
        
        # 处理信号
        signals = (signal.SIGTERM, signal.SIGINT)
        for sig in signals:
            signal.signal(sig, self.signal_handler)
        
        # 跨平台处理
        if sys.platform == 'win32':
            import win32api
            win32api.SetConsoleCtrlHandler(lambda sig: self.signal_handler(sig, None), True)
        else:
            signal.signal(signal.SIGHUP, self.signal_handler)
        
        sys.excepthook = self.exception_hook

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self._exit_flag:
            return
        self._exit_flag = True

        print("Cleaning up resources...")
        # self.client.stop()

        config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write('Is successful to stop the program: True')

    def signal_handler(self, signum, frame):
        print(f"Received signal {signum}, cleaning up...")
        self.cleanup()
        sys.exit(0)

    def exception_hook(self, exc_type, exc_value, traceback):
        print("Unhandled exception occurred, cleaning up...")
        self.cleanup()
        sys.__excepthook__(exc_type, exc_value, traceback)


if __name__ == '__main__':
    main()
