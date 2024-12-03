
import typing
import traceback
import wrapt


@wrapt.decorator
def boundary_check(func: typing.Callable[..., typing.Any],
                   instance: typing.Any,
                   args: tuple,
                   kwargs: dict) -> typing.Any:
    """
    用于检查函数的参数类型是否为注解的类型. 若非, 则打印错误信息, 并直接退出函数,  返回值为None.

    - <!> 请注意, 该修饰器仅能检查一层变量类型, 如果是嵌套的变量类型, 该修饰器无法检查, 请单独在被修饰函数中进行检查.
    - typing 中的类型仅支持 typing.Any, typing.Union, typing.Callable, typing.List, typing.Dict, typing.Tuple 类型.


    参数:
    - func: 被修饰器修饰的函数

    返回值:
    - 包装后的函数
    - 如果参数类型非注解类型, 则返回None
    """
    annotations = func.__annotations__
    param_names = func.__code__.co_varnames[:func.__code__.co_argcount]
    all_args = dict(zip(param_names, args), **kwargs)
    error_messages = []
    # print("所有参数:", all_args)
    # print("函数的变量注解:", annotations)
    for param_name, param_value in all_args.items():
        if param_name not in annotations:
            continue
        defined_type = annotations[param_name]
        input_type = type(param_value)
        try:
            if hasattr(defined_type, '__origin__'):
                typing_type = defined_type.__origin__
                # 检查 typing.Any 类型
                if typing_type is typing.Any:
                    continue
                # 检查 typing.Union 类型
                elif typing_type is typing.Union:
                    if not isinstance(param_value, defined_type.__args__):
                        error_messages.append(f"""[{func.__module__}] - [{func.__qualname__}] - [类型错误]: 参数 '{param_name}' 的类型必须是 <class '{typing_type}'>, 当前为: {input_type}\n""")
                # 检查 typing.Callable 类型
                elif typing_type is typing.Callable:
                    if not callable(param_value):
                        error_messages.append(f"""[{func.__module__}] - [{func.__qualname__}] - [类型错误]: 参数 '{param_name}' 的类型必须是 <class '{typing_type}'>, 当前为: {input_type}\n""")
                # 检查 typing.List / typing.Dict / typing.Tuple 类型
                elif typing_type in (list, dict, tuple):
                    if not isinstance(param_value, typing_type):
                        error_messages.append(f"[{func.__module__}] - [{func.__qualname__}] - [类型错误]: 参数 '{param_name}' 的类型必须是 {typing_type}, 当前为: {input_type}\n")
            # 检查 None 类型
            # 形参是 None,  实参也是 None 的情况, 避免下面对None进行操作, 跳过循环
            elif param_value is None and (defined_type is type(None) or defined_type is None):
                continue
            # 形参是 None , 但是 实参是 非None 的情况
            elif param_value is not None and (defined_type is type(None) or defined_type is None):
                error_messages.append(f"""[{func.__module__}] - [{func.__qualname__}] - [类型错误]: 参数 '{param_name}' 的类型必须是 <class '{defined_type}'> \t当前为: {input_type}\n""")
            # 形参是 非None , 但是 实参是 None 的情况
            elif param_value is None and (defined_type is not type(None) or defined_type is not None):
                error_messages.append(f"""[{func.__module__}] - [{func.__qualname__}] - [类型错误]: 参数 '{param_name}' 的类型必须是 <class '{defined_type}'> \t当前为: {input_type}\n""")
            else:
                # 检查其他类型
                if '[' in str(defined_type):  # 对例如 List[int], dict[str,int], tuple[int] 这些类型进行处理
                    defined_type = eval(str(defined_type).split('[')[0])
                if not isinstance(param_value, defined_type):
                    error_messages.append(f"""[{func.__module__}] - [{func.__qualname__}] - [类型错误]: 参数 '{param_name}' 的类型必须是 <class '{defined_type}'> \t当前为: {input_type}\n""")
        except:
            print(traceback.format_exc())
            print(f"[{func.__module__}] - [{func.__qualname__}] - [装饰器错误]: 参数 '{param_name}' 注解指定 <class '{defined_type}'> \t实际传入为: {input_type}\n")
            return None
    if error_messages:
        print(''.join(error_messages))
        return None
    return func(*args, **kwargs)
