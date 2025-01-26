
import asyncio
import types
import traceback
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from ocpp.charge_point import snake_to_camel_case
from sys_basis.XSignal import XSignal
from ocpp.v201.enums import *
from const.Charge_Point_Parameters import *
from const.Const_Parameter import *
from tools.data_gene import *
import inspect
import time
import uuid

_info = Log.CP.info
_debug = Log.CP.debug


class ChargePointBase(object):
    """
    充电桩服务器基类
    该类主要提供其与主线程的通讯机制

    - 信号:
        - signal_charge_point_ocpp_request(dict): OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
            - `message_id`: 消息ID, 用于匹配请求与响应
        - signal_charge_point_ocpp_response(dict): OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型, 实际是数据类的名称, 例如: `call.Authorize` 中的 `'Authorize'`, 在1.6版本中可能存在数据类名称与消息类型不一致的情况
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `result`(int): 响应结果, 表示响应是否成功收到.
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        - signal_charge_point_ocpp_response_result(dict): OCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `result`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`
        - signal_charge_point_info(str): 普通信号, 用于信息显示, 调试等

    - 属性:
        - response_timeout_in_baseclass(int|float)

    - 方法:
        - send_response_message: 发送响应消息
        - show_current_message_to_send : 显示当前待发送的消息队列
        - show_time_table_for_send_message : 显示当前待发送消息的时间表
        - set_response_timeout: 设置响应超时时间
        - (异步)_wait_for_result `<保护>`: 等待响应消息
        - _send_signal_info_and_ocpp_request `<保护>`: 发送/打印信息信号和OCPP请求消息信号
        - _send_signal_info `<保护>`: 发送/打印信息信号
        - _set_network_buffer_time_in_baseclass `<保护>`: 设置网络缓冲时间, 命名in_baseclass主要区分于子类的方法
        - _set_doSendDefaultResponse `保护`: 设置是否发送默认响应
        - _init_parameters_in_baseclass `<保护>`: 初始化参数, 因继承问题不得已而为之
    """
    @property
    def signal_charge_point_ocpp_request(self) -> XSignal:  # OCPP请求消息信号
        """
        OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
            - `message_id`: 消息ID, 用于匹配请求与响应
        """
        return self.__signal_charge_point_ocpp_request

    @property
    def signal_charge_point_ocpp_response(self) -> XSignal:  # OCPP响应消息信号
        """
        OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型, 实际是数据类的名称, 例如: `call.Authorize` 中的 `'Authorize'`, 在1.6版本中可能存在数据类名称与消息类型不一致的情况
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `message_id`: 消息ID, 用于匹配请求与响应
            - `result`(int): 响应结果, 表示响应是否成功收到.
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        """
        return self.__signal_charge_point_ocpp_response

    @property
    def signal_charge_point_ocpp_response_result(self) -> XSignal:
        """
        OCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `result`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`
        """
        return self.__signal_charge_point_ocpp_response_result

    @property
    def signal_charge_point_info(self):  # 普通信号, 用于信息显示, 调试等
        """ 普通信号, 用于信息显示, 调试等 """
        return self.__signal_charge_point_info

    @property
    def response_timeout_in_baseclass(self) -> int | float:
        """ 响应超时时间, 单位为秒 """
        return self._response_timeout

    def send_response_message(self, message_action: str | Action, message, send_time: float, message_id: str) -> int:
        """
        发送响应消息, 结果将通过信号 signal_charge_point_ocpp_response_result 以字典形式发送, 结构如下:
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `result`(int): 发送结果
                - 枚举类: `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`

        发送时间指 从当前实例通过信号发送给主线程的时间戳.
        接收时间指 主线程调用该函数传递消息的时间

        以下情况将不会发送消息:
        1. 当消息的发送时间小于记录的发送时间, 则表示当前消息已错过发送时间, 将被自动忽略.
        2. 当消息的接收时间大于记录的接收时间, 则表示当前消息已错过发送时间, 将被自动忽略.

        - 参数:
            - message_action(str): 消息类型, 请使用enums.Action枚举类
                - 例如: `enums.Action.authorize`
            - message(dataclass): 响应消息, 该消息为OCPP数据类类型的消息, 请使用生成器进行消息生成
                - 例如: `authorize_response.generate(authorize_response.get_id_token_info('Accepted'))`
            - send_time(float): 接收的信号中的时间戳, 用于判断消息是否过期, 键名 `send_time` .
                - 例如: request_message['send_time']

        - 返回值:
            CP_Params.RESPONSE_RESULT`的枚举值. 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        """
        current_time = time.time()

        # 情况1
        _debug(self.__time_table_for_send_message, message_action in self.__time_table_for_send_message, message_id, message_id not in self.__time_table_for_send_message[message_action])
        if (message_action in self.__time_table_for_send_message and
                message_id in self.__time_table_for_send_message[message_action] and
                self.__time_table_for_send_message[message_action][message_id]['send_time'] > send_time):
            self._send_signal_info(f'<Error - send_time> the send time of the message {message_action} is less than the recorded send time, the message will be ignored\n\t{message}')
            self.signal_charge_point_ocpp_response_result.emit({
                'action': message_action,
                'data': message,
                'send_time': send_time,
                'message_id': message_id,
                'result': CP_Params.RESPONSE_RESULT.TIMEOUT})
            return CP_Params.RESPONSE_RESULT.TIMEOUT
        # 情况2
        # if (message_action in self.__time_table_for_send_message and
        #         message_id in self.__time_table_for_send_message[message_action] and
        #         self.__time_table_for_send_message[message_action][message_id]['receive_time'] > 0 and
        #         self.__time_table_for_send_message[message_action][message_id]['receive_time'] < current_time):
        if (message_action in self.__time_table_for_send_message and
                message_id not in self.__time_table_for_send_message[message_action]):
            self._send_signal_info(f'<Error - receive_time> the receive time of the message {message_action} is greater than the current time, the message will be ignored\n\t{message}')
            self.signal_charge_point_ocpp_response_result.emit(
                {
                    'action': message_action,
                    'data': message,
                    'send_time': send_time,
                    'message_id': message_id,
                    'result': CP_Params.RESPONSE_RESULT.TIMEOUT
                }
            )
            return CP_Params.RESPONSE_RESULT.TIMEOUT
        # 可以发送消息
        if message_action not in self.__time_table_for_send_message:
            # self.__time_table_for_send_message[message_action][message_id] = {
            #     'send_time': send_time,
            #     'receive_time': current_time
            # }
            self.__time_table_for_send_message[message_action] = {}
        else:
            self.__time_table_for_send_message[message_action].pop(message_id, None)
        if message_action not in self.__current_message_to_send:
            self.__current_message_to_send[message_action] = []
        self.__current_message_to_send[message_action].append(message)
        self.signal_charge_point_ocpp_response_result.emit({
            'action': message_action,
            'data': message,
            'send_time': send_time,
            'message_id': message_id,
            'result': CP_Params.RESPONSE_RESULT.SUCCESS})
        return CP_Params.RESPONSE_RESULT.SUCCESS

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

    def set_response_timeout(self, response_timeout_s: int | float) -> bool:
        """
        更改响应超时时间

        - 参数:
            - response_timeout(int|float): 响应超时时间, 单位为 `秒`

        - 返回值:
            - True: 更改成功
            - False: 更改失败, 响应时间维持原来的值
        """
        if not isinstance(response_timeout_s, (int, float)):
            self._send_signal_info('<Error - Type - response_timeout> response_timeout must be int or float')
            return False
        if response_timeout_s <= 0:
            self._send_signal_info('<Error - Type - response_timeout> response_timeout must be greater than 0')
            return False
        self._response_timeout = response_timeout_s
        return True

    async def _wait_for_result(self, message_action: str | Action, default_message):  # TODO while 循环没有对是否已经发送了做出判断
        """
        等待响应消息
        该函数的机制是, 当监听到响应请求时, 会先发送信号给主线程, 当前实例会停留在该函数进行监听消息, 如果主线程调用了当前类中的 `send_response_message`, 则 `self.__current_message_to_send[message_action]` 会增加一个消息, 该函数会读取消息, 检查其是否为对应请求消息类型的消息, 若是则返回消息, 此时当前实例会继续执行, 否则将继续等待.

        当等待时长超过 self._response_timeout 时, 会返回 default_message, 并拒绝接受当次的系统响应消息.

        - 参数:
            - message_action(str): 消息类型, 请使用enums.Action枚举类

        - 返回值:
            - message(dataclass): 响应消息, 该消息为OCPP数据类类型的消息
        """
        _info(f'调用 _wait_for_result, {message_action}')
        response_timeout = self._response_timeout - self.__network_buffer_time  # 网络缓冲时间, 考虑到网络延迟, 提前结束等待
        wait_until = time.time() + response_timeout
        message_id = uuid.uuid4().hex
        self._send_signal_info_and_ocpp_request(message_action, message_id)
        while message_action not in self.__current_message_to_send or (message_action in self.__current_message_to_send and len(self.__current_message_to_send[message_action]) < 1):
            await asyncio.sleep(0.1)
            if time.time() > wait_until:
                # self.__time_table_for_send_message[message_action][message_id]['receive_time'] = time.time()
                self.__time_table_for_send_message[message_action].pop(message_id, None)
                error_text = f'********************\n < Error - Timeout_for_Response > System has no response for {message_action} request in {response_timeout} seconds (required response time: {self._response_timeout} seconds), the default message will be returned\n\t{default_message}\n********************'
                self._send_signal_info(error_text)
                if not self.__doSendDefaultResponse:
                    await asyncio.sleep(self.__network_buffer_time + CP_Params.RESPONSE_DELAY_TIME)  # 延迟到超时后发送, 此举为了结束该函数, 但实际上消息已无效
                return default_message
        _debug(f'Response消息队列完整 前  {self.__current_message_to_send}')
        _debug(f'Response消息队列 前 {type(self.__current_message_to_send[message_action])}  {self.__current_message_to_send[message_action]}')
        message = self.__current_message_to_send[message_action].pop(0)
        _debug(f'Response消息队列 后 {type(self.__current_message_to_send[message_action])}  {self.__current_message_to_send[message_action]}')
        if self.__current_message_to_send[message_action] == []:
            del self.__current_message_to_send[message_action]
        _debug(f'Response消息队列 删除后 {message_action in self.__current_message_to_send}  {self.__current_message_to_send}')
        return message

    def _send_signal_info_and_ocpp_request(self, message_action: str | Action, message_id: str,  info_action: str | None = None) -> None:
        """
        用于发送/打印 信息信号 和 OCPP消息信号

        - 参数:
            - message_action: 消息类型, 建议使用 Action 的枚举值, 如 Action.authorize
            - info_action: 信息动作, 默认为None, 输出 <Request> received

        该函数将通过 signal_charge_point_info 和 signal_charge_point_ocpp_request 发送信号, 并在控制台打印信息.

        ocpp_message 信号将携带一个字典, 包含
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 发送时间
        """
        frame: types.FrameType = inspect.currentframe()
        caller_frame = frame.f_back
        caller_frame = caller_frame.f_back
        if not info_action:
            info_action = '<Request> received'
        func_info = self.__get_func_name_and_params(frame=caller_frame)
        bound_arguments: inspect.BoundArguments = func_info['bound_arguments']
        struct_params_info = f"""\n->>> {info_action} - {message_action}\n"""
        temp_dict = {
            'action': message_action,
            'data': {},
            'send_time': time.time(),
            'message_id': message_id
        }
        for name, value in bound_arguments.arguments.items():
            struct_params_info += f"\t - {name}: {value}\n"
            temp_dict['data'][DataGene.snake_to_camel_string(name)] = snake_to_camel_case(value)
        self.__set_time_table_for_send_message(message_action, temp_dict['send_time'], temp_dict['message_id'])
        # self.__set_message_id_table_for_send_message(message_action, temp_dict['message_id'])
        self._send_signal_info(struct_params_info)
        self.signal_charge_point_ocpp_request.emit(temp_dict)

    def _send_signal_info(self, *args) -> None:
        """
        发送/打印信息信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            self.signal_charge_point_info.emit(temp)
            Log.CP.info(temp)
        except Exception as e:
            error_text = f'********************\n<Error - send_signal_info> {traceback.format_exc()}\n********************'
            self.signal_charge_point_info.emit(error_text)
            Log.CP.info(error_text)

    def _set_network_buffer_time_in_baseclass(self, network_buffer_time) -> None:
        self.__network_buffer_time = network_buffer_time

    def _set_doSendDefaultResponse(self, flag: bool) -> None:
        self.__doSendDefaultResponse = flag

    def _init_parameters_in_baseclass(self) -> None:
        self.__signal_charge_point_ocpp_request: XSignal = XSignal(dict)  # OCPP请求消息信号
        self.__signal_charge_point_ocpp_response: XSignal = XSignal(dict)  # OCPP响应消息信号
        self.__signal_charge_point_ocpp_response_result: XSignal = XSignal(dict)  # OCPP响应结果信号
        self.__signal_charge_point_info: XSignal = XSignal(str)  # 普通信号, 用于信息显示, 调试等
        self.__current_message_to_send: dict = {}
        self.__time_table_for_send_message: dict = {}
        self.__network_buffer_time: int | float = 0
        self.__doSendDefaultResponse: bool = False

    def __init__(self, response_timeout=30) -> None:
        self._response_timeout: int = response_timeout
        self._init_parameters_in_baseclass()

    def __get_func_name_and_params(self, frame: types.FrameType) -> dict | None:
        """
        获取调用函数的函数名和参数

        - 参数:
            - frame: 调用函数的帧信息

        返回:
            - dict: 调用函数的函数名和参数, 键值信息如下:
                - `func_name`: 函数名
                - `bound_arguments`: 参数信息
        """
        if not frame or not isinstance(frame, types.FrameType):
            return None
        if frame:
            caller_name = frame.f_code.co_name
            caller_func = None
            local_variables = frame.f_locals
            formal_params = {}
            for key, item in local_variables.items():
                if key not in ['default_message', 'self']:
                    formal_params[key] = item

            if 'self' in frame.f_locals:
                instance = local_variables.pop('self')
                caller_func = getattr(instance, caller_name, None)
            else:
                caller_func = frame.f_globals.get(caller_name, None) or local_variables.get(caller_name, None)

            if caller_func:
                sig = inspect.signature(caller_func)
                bound_arguments = sig.bind(**formal_params)
                bound_arguments.apply_defaults()
                return {'func_name': caller_name, 'bound_arguments': bound_arguments}
        return None

    def __set_time_table_for_send_message(self, message_action: str | Action, send_time: float, message_id: str) -> None:
        """
        设置信息时间表信息
        如果未曾有过该消息类型, 则创建新的字典, 否则更新该消息类型的发送时间

        - 参数:
            - `message_action`(str): 消息类型
            - `send_time`(float): 发送时间
        """
        if message_action not in self.__time_table_for_send_message:
            self.__time_table_for_send_message[message_action] = {}
            self.__time_table_for_send_message[message_action][message_id] = {
                'send_time': send_time,
                'receive_time': 0}
        else:
            if message_id not in self.__time_table_for_send_message[message_action]:
                self.__time_table_for_send_message[message_action][message_id] = {
                    'send_time': send_time,
                    'receive_time': 0}
            else:
                self.__time_table_for_send_message[message_action][message_id]['send_time'] = send_time

    def _unpack_data_and_send_signal_ocpp_response(self, data, send_time: float, ori_data=None) -> None:
        """
        解包数据并发送信号

        数据将通过 `self._send_signal_charge_point_ocpp_response` 发送, 数据格式为:
            - `action`(str): 消息类型, 实际是数据类的名称, 例如: `call.Authorize` 中的 `'Authorize'`, 在1.6版本中可能存在数据类名称与消息类型不一致的情况
            - `ori_data`: 原始数据, 发送的Request数据
            - `data`(dict): 解包后的数据
            - `send_time`(float): 请求发送时间
            - `result`(int): 响应结果,
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`

        - 参数:
            - `data`(dataclass): ocpp数据类, 类型如:  `call_result.Authorize`
            - `send_time`(float): 发送时间

        - 返回值:
            - 无
        """
        if not data:
            return
        temp_dict = {
            'action': data.__class__.__name__,
            'ori_data': ori_data,
            'data': {},
            'send_time': send_time,
            'result': CP_Params.RESPONSE.SUCCESS,
        }
        info_text = f'->>> <Response> received - {temp_dict["action"]}\n'
        for item in data.__class__.__dict__['__match_args__']:
            temp_dict['data'][item] = getattr(data, item)
            info_text += f'\t - {item}: {temp_dict["data"][item]}\n'
        self.signal_charge_point_ocpp_response.emit(temp_dict)
        self._send_signal_info(info_text)
