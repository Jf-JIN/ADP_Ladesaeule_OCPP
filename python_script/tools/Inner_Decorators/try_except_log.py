
from typing import Any, Callable
import traceback
import wrapt


def try_except_log(logger_error=None, *func) -> Callable[..., Any | None]:
    """
    用于捕获函数的异常并返回异常对象. 

    参数:
    - logger_error (callable, 可选): 用于记录异常的日志函数. 默认为None. 
    - textbrowser (QWidget, 可选): 用于显示异常信息的文本框. 默认为None. 

    返回值:
    Callable[..., Any | None]: 包装后的函数, 捕获函数的异常并返回异常对象.
    """

    @wrapt.decorator
    def try_decorator(wrapped: Callable, instance, args, kwargs) -> Callable[..., Any | None]:
        try:
            return wrapped(*args, **kwargs)
        except Exception as e:
            e = traceback.format_exc()
            if logger_error:
                logger_error(e, extra={'moduleName': wrapped.__module__, 'functionName': wrapped.__qualname__})
            for item in func:
                try:
                    if isinstance(item, str):
                        parts = item.split('.')
                        fcn = instance
                        for part in parts:
                            fcn = getattr(fcn, part, None)
                        if callable(fcn):
                            fcn(e)
                        else:
                            print(f'请传入函数/方法，或者方法名称(属性名), 当前为 {type(fcn)}')
                    elif callable(item):
                        item(e)
                    else:
                        print(f'请传入函数/方法，或者方法名称(属性名), 当前为 {type(fcn)}')
                except:
                    print(traceback.format_exc())
            return None
    return try_decorator


if __name__ == '__main__':
    class PrintManager:
        def __init__(self):
            self.outputf = 'l'

        def output(self, text):
            print('PrintManager\t', text)

    class StaticPrintManager:
        @staticmethod
        def output(text):
            print('StaticPrintManager\t', text)

    class TryExceptLog:
        def __init__(self):
            self.mm = PrintManager()

        @try_except_log(None, StaticPrintManager.output, 'output', 'mm.output')
        def TestMain(self):
            1/0

        def output(self, text):
            print('TryExceptLog\t', text)

    a = TryExceptLog()
    a.TestMain()
