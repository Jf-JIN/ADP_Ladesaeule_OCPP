
import os
import fcntl
import atexit
import sys
from const.Const_Parameter import *

_log = Log.CRITICAL


class _null:
    def __repr__(self):
        return 'null'


_Null = _null()


class ProcessLock:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__isInitialized = False
        return cls.__instance__

    def __init__(self, lock_file_path: str) -> None:
        if self.__isInitialized:
            return
        self.__isInitialized = True
        self.__lock_file_path = lock_file_path
        self.__file = None

    @staticmethod
    def release():
        if ProcessLock.__instance__ is None:
            return
        ProcessLock.__instance__.__release()

    @staticmethod
    def acquire(load_file_path: str = _Null):
        if ProcessLock.__instance__ is None:
            if not isinstance(load_file_path, str):
                raise TypeError('load_file_path must be a string')
            ProcessLock.__instance__ = ProcessLock(load_file_path)
        ProcessLock.__instance__.__acquire()

    def __acquire(self):
        self.__file = open(self.__lock_file_path, 'w')
        try:
            # 尝试获取独占锁（非阻塞）
            fcntl.flock(self.__file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.__file.write(str(os.getpid()))
            self.__file.flush()
        except BlockingIOError:
            _log.info("Another instance is already running.")
            sys.exit(1)
        except Exception as e:
            _log.error(f"An error occurred while acquiring the lock")
            sys.exit(1)

        # 注册退出时自动清理
        atexit.register(self.release)

    def __release(self):
        if self.__file and os.path.exists(self.__lock_file_path):
            try:
                fcntl.flock(self.__file, fcntl.LOCK_UN)
                self.__file.close()
                os.remove(self.__lock_file_path)
            except Exception as e:
                _log.exception('Error cleaning lock')
