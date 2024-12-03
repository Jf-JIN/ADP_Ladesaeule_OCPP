
from typing import Any, Callable
import time
import wrapt


@wrapt.decorator
def time_counter(func, instance, args, kwargs) -> Callable[..., tuple[Any, float]]:
    """
    用于计算函数的执行时间. 

    参数:
    - func: 的函数

    返回值:
    包装后的函数, 返回函数的执行结果和执行时间的元组
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    print(f'[{func.__module__}] - [{func.__qualname__}]-[runTime]:\t', end - start)
    return result
