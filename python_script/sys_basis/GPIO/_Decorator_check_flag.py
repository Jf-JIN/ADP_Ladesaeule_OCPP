# from functools import wraps
from const.GPIO_Parameter import *
#
# def check_flag(method):
#     """
#     检查flag装饰器，如果结果为FAIL，调用错误处理方法。
#     """
#
#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             # 调用配置方法，获取flag和结果
#             flag, value, message = method(self)
#
#             # 如果 flag 是 FAIL，执行错误处理
#             if flag == ResultFlag.FAIL:
#                 self.checking_connection()
#
#
#                # return None  # 或其他需要的返回值
#
#             # 将 value 和 message 传递给被装饰函数
#             return func(self, value, message, *args, **kwargs)
#
#         return wrapper
#
#     return decorator


import wrapt


def check_flag(used_method):
    """
    装饰器：检查 flag，如果返回 FAIL，执行错误处理逻辑。
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # 在运行时动态调用 used_method
        flag, value, message = used_method(instance)

        if flag == ResultFlag.FAIL:
            # 如果 flag 失败，执行错误处理
            instance.checking_connection()
            #return None

        # 将 value 和 message 传递给被装饰的函数
        return wrapped(*args, **kwargs, value=value, message=message)

    return wrapper

