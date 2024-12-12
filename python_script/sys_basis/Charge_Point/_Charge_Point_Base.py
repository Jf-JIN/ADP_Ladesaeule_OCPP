
import asyncio
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from sys_basis.XSignal import XSignal
from ocpp.v201.enums import *
import inspect
import time


class ChargePointBase(object):
    """
    充电桩服务器基类
    该类主要提供其与主线程的通讯机制

    信号: 
    - signal_ocpp_request: OCPP请求消息信号
    - signal_ocpp_response: OCPP响应消息信号
    - signal_info: 普通信号, 用于信息显示, 调试等

    属性: 
    - response_timeout_in_baseclass

    方法: 
    - send_response_message: 发送响应消息
    - show_current_message_to_send : 显示当前待发送的消息队列
    - show_time_table_for_send_message : 显示当前待发送消息的时间表
    - set_response_timeout: 设置响应超时时间
    - _wait_for_result `<保护>`: 等待响应消息
    - _send_signal_info_and_ocpp_request `<保护>`: 发送/打印信息信号和OCPP请求消息信号
    - _send_signal_info `<保护>`: 发送/打印信息信号
    - _set_network_buffer_time_in_baseclass `<保护>`: 设置网络缓冲时间, 命名in_baseclass主要区分于子类的方法
    - _init_parameters_in_baseclass `<保护>`: 初始化参数, 因继承问题不得已而为之
    """
    signal_ocpp_request = XSignal()  # OCPP请求消息信号
    signal_ocpp_response = XSignal()  # OCPP响应消息信号
    signal_info = XSignal()  # 普通信号, 用于信息显示, 调试等

    @property
    def response_timeout_in_baseclass(self):
        return self._response_timeout

    def send_response_message(self, message_action: str | Action, message, send_time) -> bool:
        """
        发送响应消息

        发送时间指 从当前实例通过信号发送给主线程的时间戳. 
        接收时间指 主线程调用该函数传递消息的时间

        以下情况将不会发送消息:
        1. 当消息的发送时间小于记录的发送时间, 则表示当前消息已错过发送时间, 将被自动忽略. 
        2. 当消息的接收时间大于记录的接收时间, 则表示当前消息已错过发送时间, 将被自动忽略. 

        参数:
        - message_action: 消息类型, 请使用enums.Action枚举类
            - 例如: `enums.Action.authorize`
        - message: 响应消息, 该消息为OCPP数据类类型的消息, 请使用生成器进行消息生成
            - 例如: `authorize_response.generate(authorize_response.get_id_token_info('Accepted'))`
        - send_time: 接收的信号中的时间戳, 用于判断消息是否过期, 键名 `send_time` . 
            - 例如: request_message['send_time']

        返回:
        - True: 发送成功
        - False: 发送失败, 消息已过时
        """
        current_time = time.time()

        # 情况1
        if message_action in self.__time_table_for_send_message and self.__time_table_for_send_message[message_action]['send_time'] > send_time:
            self._send_signal_info(f'<Error - send_time> the send time of the message {message_action} is less than the recorded send time, the message will be ignored')
            return False
        # 情况2
        if message_action in self.__time_table_for_send_message and self.__time_table_for_send_message[message_action]['receive_time'] < current_time:
            self._send_signal_info(f'<Error - receive_time> the receive time of the message {message_action} is greater than the current time, the message will be ignored')
            return False
        # 可以发送消息
        if message_action not in self.__time_table_for_send_message:
            self.__time_table_for_send_message[message_action] = {
                'send_time': send_time,
                'receive_time': current_time
            }
        self.__current_message_to_send[message_action].append(message)
        return True

    def show_current_message_to_send(self) -> None:
        """
        显示当前待发送消息列表
        """
        self._send_signal_info(self.__current_message_to_send)

    def show_time_table_for_send_message(self) -> None:
        """
        返回发送信息的时间表

        主要用于查看是否当前消息已过时
        """
        self._send_signal_info(self.__time_table_for_send_message)

    def set_response_timeout(self, response_timeout_s: int | float) -> None:
        """ 
        更改响应超时时间

        参数：
        - response_timeout(int|float): 响应超时时间, 单位为 `秒`

        返回：
        - True: 更改成功
        - False: 更改失败，响应时间维持原来的值
        """
        if not isinstance(response_timeout_s, (int, float)):
            self._send_signal_info('<Error - Type - response_timeout> response_timeout must be int or float')
            return False
        if response_timeout_s <= 0:
            self._send_signal_info('<Error - Type - response_timeout> response_timeout must be greater than 0')
            return False
        self._response_timeout = response_timeout_s
        return True

    async def _wait_for_result(self, message_action: str | Action, default_message) -> dict:
        """
        等待响应消息
        该函数的机制是, 当监听到响应请求时, 会先发送信号给主线程, 当前实例会停留在该函数进行监听消息, 如果主线程调用了当前类中的 `send_response_message`, 则 `self.__current_message_to_send[message_action]` 会增加一个消息, 该函数会读取消息, 检查其是否为对应请求消息类型的消息, 若是则返回消息, 此时当前实例会继续执行, 否则将继续等待.

        当等待时长超过 self._response_timeout 时, 会返回 default_message, 并拒绝接受当次的系统响应消息.

        参数:
        - message_action: 消息类型, 请使用enums.Action枚举类

        返回:
        - message: 响应消息, 该消息为OCPP数据类类型的消息
        """
        response_timeout = self._response_timeout - self.__network_buffer_time  # 网络缓冲时间, 考虑到网络延迟, 提前结束等待
        wait_until = time.time() + response_timeout
        while not message_action in self.__current_message_to_send or len(self.__current_message_to_send[message_action]) < 1:
            await asyncio.sleep(0.1)
            if time.time() > wait_until:
                self.__time_table_for_send_message[message_action]['recv_time'] = time.time()
                error_text = f'********************\n < Error - Timeout_for_Response > System has no response for {message_action} request in {response_timeout} seconds (required response time: {self._response_timeout} seconds), the default message will be returned\n\t{default_message}\n********************'
                self._send_signal_info(error_text)
                return default_message
        message = self.__current_message_to_send[message_action].pop(0)
        if self.__current_message_to_send[message_action] == []:
            del self.__current_message_to_send[message_action]
        return message

    def _send_signal_info_and_ocpp_request(self, message_action: str | None, info_action: str | None = None) -> None:
        """
        用于发送/打印 信息信号 和 OCPP消息信号

        参数:
        - message_action: 消息类型, 建议使用 Action 的枚举值, 如 Action.authorize
        - info_action: 信息动作, 默认为None, 输出 <Request> received

        该函数将通过 signal_info 和 signal_ocpp_request 发送信号, 并在控制台打印信息.

        ocpp_message 信号将携带一个字典, 包含

            - `action`: 消息类型
            - `data`: OCPP消息的字典形式
            - `send_time`: 发送时间
        """
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        if not info_action:
            info_action = '<Request> received'

        func_info = self.__get_func_name_and_params(frame=caller_frame)
        bound_arguments: inspect.BoundArguments = func_info['bound_arguments']

        struct_params_info = f"""\n->>> {info_action} - {message_action}\n"""
        temp_dict = {
            'action': message_action,
            'data': {},
            'send_time': time.time()
        }
        for name, value in bound_arguments.arguments.items():
            struct_params_info += f"\t - {name}: {value}\n"
            temp_dict['data'][name] = value
        self.__set_time_table_for_send_message(message_action, temp_dict['send_time'])
        self._send_signal_info(struct_params_info)
        self.signal_ocpp_request.emit(temp_dict)

    def _send_signal_info(self, *args) -> None:
        """
        发送/打印信息信号

        涵盖发送前的检查

        参数: 
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            self.signal_info.emit(temp)
            print(temp)
        except Exception as e:
            error_text = f'********************\n<Error - send_signal_info> {e}\n********************'
            self.signal_info.emit(error_text)
            print(error_text)

    def _set_network_buffer_time_in_baseclass(self, network_buffer_time) -> None:
        self.__network_buffer_time = network_buffer_time

    def _init_parameters_in_baseclass(self) -> None:
        self.__current_message_to_send = {}
        self.__time_table_for_send_message = {}
        self.__network_buffer_time = 2

    def __init__(self, response_timeout=30):
        self._response_timeout = response_timeout
        self._init_parameters_in_baseclass()

    def __get_func_name_and_params(self, frame: inspect.FrameInfo) -> dict | None:
        """
        获取调用函数的函数名和参数

        参数:
        - frame: 调用函数的帧信息

        返回:
        - dict: 调用函数的函数名和参数, 键值信息如下:
            - `func_name`: 函数名
            - `bound_arguments`: 参数信息
        """
        if not frame or isinstance(frame, inspect.FrameInfo):
            return None
        if frame:
            caller_name = frame.f_code.co_name
            caller_func = None
            local_variables = frame.f_locals

            if 'self' in frame.f_locals:
                instance = local_variables.pop('self')
                caller_func = getattr(instance, caller_name, None)
            else:
                caller_func = frame.f_globals.get(caller_name, None) or local_variables.get(caller_name, None)

            if caller_func:
                sig = inspect.signature(caller_func)
                bound_arguments = sig.bind(**local_variables)
                bound_arguments.apply_defaults()
                return {'func_name': caller_name, 'bound_arguments': bound_arguments}
        return None

    def __set_time_table_for_send_message(self, message_action, send_time) -> None:
        """ 
        设置信息时间表信息
        如果未曾有过该消息类型, 则创建新的字典, 否则更新该消息类型的发送时间

        参数: 
        - `message_action`: 消息类型
        - `send_time`: 发送时间
        """
        if message_action not in self.__time_table_for_send_message:
            self.__time_table_for_send_message[message_action] = {
                'send_time': send_time,
                'recv_time': 0}
        else:
            self.__time_table_for_send_message[message_action]['send_time'] = send_time
