
from const.Const_Logger import *
from server.Server_Function import *
import sys
import os
import traceback

isIntialized = False


def write_to_log(error_message: str):
    """ 在完成初始化前，程序出现错误时的输出 """
    log_file_path = os.path.join(APP_WP, 'Logs', 'critical.log')
    with open(log_file_path, 'w', encoding='utf-8') as f:
        f.write(error_message)


def exception_handler(exc_type, exc_value, exc_traceback) -> None:
    global isIntialized
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    if isIntialized:
        try:
            Log.CRITICAL.critical(error_message)
        except Exception as e:
            write_to_log()
    else:
        write_to_log()
    sys.exit(1)


def main():
    global isIntialized
    sys.excepthook = exception_handler
    isIntialized = True
    return ServerFunction()


if __name__ == "__main__":
    run_func = main()
