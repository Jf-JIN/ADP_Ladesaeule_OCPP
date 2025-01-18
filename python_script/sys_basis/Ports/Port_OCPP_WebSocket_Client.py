
import asyncio
import traceback
from const.Charge_Point_Parameters import CP_Params
from sys_basis.Charge_Point._Charge_Point_V1_6 import ChargePointV16
from sys_basis.Charge_Point._Charge_Point_V2_0_1 import ChargePointV201
from sys_basis.XSignal import XSignal
from sys_basis.Ports.Core_WebSocket.WebSocket_Client import WebSocketClient
from const.Const_Parameter import *

_info = Log.OCPP.info


class PortOCPPWebsocketClient(object):
    """
    充电桩ocpp WebSocket客户端 端口

    参数:
        - uri(str): 充电桩ocpp WebSocket服务器地址
        - charge_point_name(str): 充电桩名称
        - charge_point_version(str): 充电桩版本, 支持:
            - "v16", "v1.6", "v1_6", "ocpp16", "ocpp1.6", "ocpp1_6"
            - "v2.0.1", "v2_0_1", "ocpp201", "ocpp2.0.1", "ocpp2_0_1"
        - recv_timeout_s(int|float): 接收消息超时时间, 单位为秒, 须大于0, 默认值为 30.
        - retry_interval_s(int|float): 重试间隔时间, 单位为秒, 须大于0, 默认值为 1.
        - max_retries(int): 最大重试次数, 默认值为-1, 表示无限重试
        - ping_interval_s(int|float): 心跳间隔时间, 单位为秒, 须大于0, 默认值为 20.
        - ping_timeout_s(int|float): 心跳超时时间, 单位为秒, 须大于0, 默认值为 20.
        - info_title(str): 信息标题, 默认为 "OCPP_Client_Port"
        - websocket_info_title(str): WebSocket信息标题, 默认为 "OCPP_WebSocket_Client"

    信号:
        - signal_thread_ocpp_client_info(str): 信息信号
        - signal_thread_ocpp_client_recv(str): 接收内容信号, 此内容为所有内容, 为Websocket端口原始接收信息
        - signal_thread_ocpp_client_normal_message(str): 普通消息信号, 此内容为除OCPP外的内容
        - signal_thread_ocpp_client_recv_request(dict): OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
        - signal_thread_ocpp_client_recv_response(dict): OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `result`(int): 响应结果, 表示响应是否成功收到.
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        - signal_thread_ocpp_client_recv_response_result(dict): OOCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下:
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `result`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`

    属性:
        - isRunning: 是否正在运行
        - websocket: WebSocket客户端对象
        - ocpp_cp: OCPP客户端对象
        - list_request_message: OCPP请求消息列表

    方法:
        - run: 启动方法, 请通过传入给 asyncio.gather() 进行调用
        - send_normal_message(message): 发送普通消息
        - send_request_message(message): 发送请求消息
        - send_response_message(message_action, message, send_time, message_id): 发送响应消息
    """

    def __init__(
        self,
        uri: str,
        charge_point_name: str,
        charge_point_version: str = 'v2.0.1',
        recv_timeout_s: int | float = 20,
        retry_interval_s: int | float = 1,
        ocpp_response_timeout_s: int | float = 20,
        listen_timeout_s: int | float = 10,
        max_retries: int = -1,
        ping_interval_s: int | float = 30,
        ping_timeout_s: int | float = 40,
        info_title: str = 'OCPP_Client_Port',
        websocket_info_title: str = 'OCPP_WebSocket_Client'
    ) -> None:
        super().__init__()
        self.__signal_thread_ocpp_client_info: XSignal = XSignal(str)
        self.__signal_thread_ocpp_client_recv: XSignal = XSignal(str)
        self.__signal_thread_ocpp_client_normal_message: XSignal = XSignal(str)
        self.__signal_thread_ocpp_client_recv_request: XSignal = XSignal(dict)
        self.__signal_thread_ocpp_client_recv_response: XSignal = XSignal(dict)
        self.__signal_thread_ocpp_client_recv_response_result: XSignal = XSignal(dict)
        self.__websocket = WebSocketClient(
            uri=uri,
            recv_timeout_s=recv_timeout_s,
            retry_interval_s=retry_interval_s,
            max_retries=max_retries,
            info_title=websocket_info_title,
            ping_interval_s=ping_interval_s,
            ping_timeout_s=ping_timeout_s
        )
        self.__websocket.signal_websocket_client_info.connect(self.signal_thread_ocpp_client_info.emit)
        self.__websocket.signal_websocket_client_recv.connect(self.signal_thread_ocpp_client_recv.emit)
        self.__list_request_message: list = []  # 存储待发送请求消息, 当列表非空则持续发送, 当列表为空则相应事件(__event_request_message)等待
        self.__list_normal_message: list = []  # 存储待发送普通消息, 当列表非空则持续发送, 当列表为空则相应事件(__event_normal_message)等待
        self.__event_request_message: asyncio.Event = asyncio.Event()  # 请求消息事件
        self.__event_normal_message: asyncio.Event = asyncio.Event()  # 普通消息事件
        self.__isRunning: bool = True  # 是否正在运行, 用于控制协程/循环运行的开关
        self.__listen_timeout_s: int | float = listen_timeout_s
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None
        # 版本兼容
        if str(charge_point_version).lower() in ['v16', 'v1.6', 'v1_6', 'ocpp16', 'ocpp1.6', 'ocpp1_6', '16']:
            from sys_basis.Charge_Point import ChargePointV16
            self.__charge_point = ChargePointV16(charge_point_name, self.__websocket, ocpp_response_timeout_s)
        elif str(charge_point_version).lower() in ['v201', 'v2.0.1', 'v2_0_1', 'ocpp201', 'ocpp2.0.1', 'ocpp2_0_1', '201']:
            from sys_basis.Charge_Point import ChargePointV201
            self.__charge_point = ChargePointV201(charge_point_name, self.__websocket, ocpp_response_timeout_s)
        else:
            raise ValueError(
                f'Invalid charge point version: {charge_point_version}. Valid versions are: \n\t- "v16", "v1.6", "v1_6", "ocpp16", "ocpp1.6", "ocpp1_6", \n\t- "v2.0.1", "v2_0_1", "ocpp201", "ocpp2.0.1", "ocpp2_0_1".')
        self.__charge_point.signal_charge_point_ocpp_request.connect(self.signal_thread_ocpp_client_recv_request.emit)
        self.__charge_point.signal_charge_point_ocpp_response.connect(self.signal_thread_ocpp_client_recv_response.emit)
        self.__charge_point.signal_charge_point_ocpp_response_result.connect(self.signal_thread_ocpp_client_recv_response_result.emit)
        self.__charge_point.signal_charge_point_info.connect(self.signal_thread_ocpp_client_info.emit)

    @property
    def signal_thread_ocpp_client_info(self) -> XSignal:
        """ 信息信号, 用于获取调试信息或显示信息 """
        return self.__signal_thread_ocpp_client_info

    @property
    def signal_thread_ocpp_client_recv(self) -> XSignal:
        """ 接收内容信号, 此内容为所有内容, 为Websocket端口原始接收信息 """
        return self.__signal_thread_ocpp_client_recv

    @property
    def signal_thread_ocpp_client_normal_message(self) -> XSignal:
        """ 普通消息信号, 此内容为除OCPP外的内容 """
        return self.__signal_thread_ocpp_client_normal_message

    @property
    def signal_thread_ocpp_client_recv_request(self) -> XSignal:
        """
        OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
        """
        return self.__signal_thread_ocpp_client_recv_request

    @property
    def signal_thread_ocpp_client_recv_response(self) -> XSignal:
        """
        OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `result`(int): 响应结果, 表示响应是否成功收到.
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        """
        return self.__signal_thread_ocpp_client_recv_response

    @property
    def signal_thread_ocpp_client_recv_response_result(self) -> XSignal:
        """
        OOCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下:
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `result`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项:`SUCCESS`, `TIMEOUT`, `ERROR`
        """
        return self.__signal_thread_ocpp_client_recv_response_result

    @property
    def isRunning(self) -> bool:
        """ 是否正在运行. """
        return self.__isRunning

    @property
    def websocket(self) -> WebSocketClient:
        """ WebSocket客户端对象. """
        return self.__websocket

    @property
    def ocpp_cp(self) -> ChargePointV16 | ChargePointV201:
        """ OCPP客户端对象. """
        return self.__charge_point

    @property
    def list_request_message(self) -> list:
        """ OCPP请求消息列表. """
        return self.__list_request_message

    async def run(self) -> None:
        """
        异步协程主体
        """
        try:
            async with self.__websocket:
                self.__task_listening = asyncio.create_task(self.__listen_for_messages())
                self.__task_send_request_messages = asyncio.create_task(self.__send_request_message())
                self.__task_send_normal_messages = asyncio.create_task(self.__send_normal_message())
                await asyncio.gather(
                    self.__task_listening,
                    self.__task_send_request_messages,
                    self.__task_send_normal_messages,
                )
                await asyncio.Future()
        except Exception as e:
            self.__send_signal_info(f"<Error - OCPP_Client_Port>\n{traceback.format_exc()}")
        finally:
            self.__isRunning = False

    def send_request_message(self, message) -> None:
        """
        发送请求消息

        当请求发送后, 将等待响应数据. 有如下三种情况:

        1. 成功接收响应数据, 数据将通过信号 `signal_charge_point_ocpp_response` 发送回来, 数据格式如下:
            - `action`: 消息类型
            - `data`: OCPP消息的字典形式
            - `send_time`: 请求发送时间
        2. 超时未接收到响应数据, 将通过信号 `signal_charge_point_info` 发送报错信息, `signal_charge_point_ocpp_response` 不发送信息
        3. 其他错误, 将通过信号 `signal_charge_point_info` 发送报错信息, `signal_charge_point_ocpp_response` 不发送信息

        参数:
            - message: 请求消息对象, OCPP数据类, 如: `call.Authorize`
        """
        self.__list_request_message.append(message)
        self.__event_request_message.set()
        _info('已解锁发送请求消息锁')

    def send_response_message(self,  message_action: str, message, send_time: float, message_id: str) -> int:
        """
        发送响应消息, 结果将通过信号 signal_thread_ocpp_client_recv_response 以字典形式发送, 结构如下:
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `result`(int): 响应结果, 表示响应是否成功收到.
                - 枚举类 `CP_Params.RESPONSE`
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
            - message_id(str): 消息ID, 用于判断消息是否过期, 键名 `message_id` .
                - 例如: request_message['message_id']

        - 返回:
            - flag(int): 
                - `RESPONSE_RESULT.SUCCESS` `0 - 成功`
                - `RESPONSE_RESULT.TIMEOUT ` `1 - 超时`
                - `RESPONSE_RESULT.ERROR` `2 - 错误`
        """
        try:
            # 此处结果将通过信号 signal_thread_ocpp_client_recv_response 传递, 无需手动处理
            flag: int = self.__charge_point.send_response_message(message_action, message, send_time, message_id)
            return flag
        except:
            self.__send_signal_info(f'<Error - send_response_message>\n{(traceback.format_exc())}')
            return CP_Params.RESPONSE_RESULT.ERROR

    def send_normal_message(self, message: str) -> None:
        """
        发送普通消息

        - 参数:
            - message(str): 普通消息, 该消息不得以 "`[`" 开头, 以免和OCPP消息混淆
        """
        if isinstance(message, str) and not message.startswith('['):
            self.__list_normal_message.append(message)
            self.__event_normal_message.set()
        else:
            self.__send_signal_info('<ValueError> normal message must not start with "["')

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        - 参数:
            - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        self.__send_signal(signal=self.signal_thread_ocpp_client_info, error_hint='send_signal_info', log=Log.OCPP.info, doShowTitle=True, doPrintInfo=False, args=[*args])

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        - 参数:
            - signal(XSignal): 信号对象
            - error_hint(str): 错误提示
            - log(Callable): 日志器动作
            - doShowTitle(bool): 是否显示标题
            - doPrintInfo(bool): 是否打印信息
            - args: 元组或列表或可解包对象, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式.
        """
        try:
            temp = ''.join([str(*args)]) + '\n'
            if self.__info_title and doShowTitle:
                temp = f'< {self.__info_title} >\n' + temp
            signal.emit(temp)
            if doPrintInfo:
                print(temp)
            if log:
                log(temp)
        except Exception as e:
            error_text = f'********************\n<Error - {error_hint}> {e}\n********************'
            if self.__info_title and doShowTitle:
                error_text = f'< {self.__info_title} >\n' + error_text
            signal.emit(error_text)
            if doPrintInfo:
                print(error_text)
            if log:
                log(error_text)

    async def __listen_for_messages(self):
        """
        监听消息, 循环执行, 主要是给充电桩传递消息.

        收到的消息实际上是通过信号Websocket的 `signal_websocket_client_recv` 和 `signal_websocket_client_info` 传进来
        """
        message = ''
        while self.__isRunning:
            _info('正在监听消息..............')
            try:
                try:
                    message = await asyncio.wait_for(self.__websocket.recv(), timeout=self.__listen_timeout_s)
                    if message is None:
                        await self.__websocket.connect()
                        await asyncio.sleep(CP_Params.OCPP_LISTEN_INTERVAL)  # 防止断连后频繁监听
                except asyncio.TimeoutError:
                    message = ''
                except Exception as e:
                    message = ''
                    _info(f'监听消息时发生异常: {repr(e)} 重连中............')
                    self.__websocket.connect()
                    await asyncio.sleep(CP_Params.OCPP_LISTEN_INTERVAL)
                _info(f'获得监听消息\n {repr(self.__websocket)}\n{type(message)}\n{repr(message)}')
                if (isinstance(message, str) and message.startswith('[')):  # 信息过滤
                    await self.__charge_point.route_message(message)
                elif message:
                    self.__signal_thread_ocpp_client_normal_message.emit(message)
            except:
                _info(f'<--报错--> 获得监听消息\n {traceback.format_exc()}\n\n{repr(message)}')
                pass

    async def __send_request_message(self) -> None:
        """
        发送请求消息, 循环执行

        当 send_request_message 被调用时, 会将消息放入队列中, 然后通过此方法发送

        当信息列表 __list_request_message 为空时, 将等待事件 __event_request_message 触发
        """
        while self.__isRunning:
            await self.__event_request_message.wait()
            _info('正在发送请求消息..............')
            if not self.__isRunning:  # 提前终止
                break
            try:
                # 此处结果将由 __charge_point.signal_charge_point_ocpp_response 传递, 无需手动处理
                if len(self.__list_request_message) > 0:
                    _info('消息已存储在队列中, 请求发送********************')
                    await self.__charge_point.send_request_message(self.__list_request_message.pop(0))
                    _info('已执行请求')
            except:
                self.__send_signal_info(f'<Error - send_request_message>\n{traceback.format_exc()}')
            _info(f'请求结束, 当前消息队列中内容\t{self.__list_request_message}')
            if not self.__list_request_message:
                self.__event_request_message.clear()

    async def __send_normal_message(self) -> None:
        """
        发送请求消息, 循环执行

        当 send_normal_message 被调用时, 会将消息放入队列中, 然后通过此方法发送

        当信息列表 __list_normal_message 为空时, 将等待事件 __event_request_message 触发
        """
        while self.__isRunning:
            _info(f'监听正常消息队列, 等待消息发送++++++++\n{self.__list_normal_message}')
            await self.__event_normal_message.wait()
            if not self.__isRunning:  # 提前终止
                break
            try:
                await self.__websocket.send(self.__list_normal_message.pop(0))
            except:
                self.__send_signal_info(f'<Error - send_normal_message>\n{traceback.format_exc()}')
            _info(f'已执行正常消息, 列表为: \n{self.__list_normal_message}')
            if not self.__list_normal_message:
                self.__event_normal_message.clear()
