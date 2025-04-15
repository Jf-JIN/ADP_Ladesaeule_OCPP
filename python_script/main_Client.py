#! /usr/bin/python3.11

from sys_basis.Process_Lock import *
from const.Const_Parameter import *

from server.Client import Client
import atexit
import os
import signal
import sys

_log = Logger('criticla', os.getcwd())


class main_obj(object):
    def __init__(self):
        self._exit_flag = False  # 防止重复清理
        self.client = Client()

        # 注册退出处理
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.signal_handler)

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
        print('cleanup')
        if self._exit_flag:
            return
        self._exit_flag = True
        config_path = os.path.join(os.path.dirname(__file__), 'cleanup_config.txt')
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


main_obj_instance = None


def main():
    if os.path.exists(LOCK_FILE_PATH):
        print('The program is already running.')
        return
    pl = ProcessLock(LOCK_FILE_PATH)
    pl.acquire()
    global main_obj_instance
    main_obj_instance = main_obj()


def exception_handler(exc_type, exc_value, exc_traceback) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    _log.critical(error_message)
    if os.path.exists(LOCK_FILE_PATH):
        os.remove(LOCK_FILE_PATH)
    sys.exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_handler
    main()
