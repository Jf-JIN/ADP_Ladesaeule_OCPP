
import ocpp
import asyncio
import traceback
from threading import Thread
from script.sys_basis.XSignal import XSignal
from sys_basis.WebSocket_Server import WebSocketServer


class OCPPWebsocketServerPort(Thread):
    """ 
    充电桩ocpp WebSocket客户端线程

    参数:
    - host(str): 充电桩ocpp WebSocket服务器地址
    - port(int): 充电桩ocpp WebSocket服务器端口
    - charge_point_name(str): 充电桩名称
    - charge_point_version(str): 充电桩版本, 支持:
        - "v16", "v1.6", "v1_6", "ocpp16", "ocpp1.6", "ocpp1_6"
        - "v2.0.1", "v2_0_1", "ocpp201", "ocpp2.0.1", "ocpp2_0_1"
    - info_title(str): 信息标题, 默认为 "OCPP Server"

    信号: 
    - signal_thread_ocpp_server_info: 线程信息信号
    - signal_thread_ocpp_server_recv_request: 接收请求信号
    - signal_thread_ocpp_server_recv_response: 接收响应信号
    - signal_thread_ocpp_server_recv_response_result: 接收响应结果信号
    - signal_thread_ocpp_server_finished: 线程完成信号

    属性: 
    - isRunning: 是否正在运行

    方法: 
    - send_request_message(message): 发送请求消息
    - send_response_message(message_action, message, send_time): 发送响应消息
    - stop(): 停止线程
    """

    def __init__(self, host: str, port: int, charge_point_name: str, charge_point_version: str = 'v2.0.1', info_title: str = 'OCPP Server'):
        super().__init__()
        self.__signal_thread_ocpp_server_info = XSignal()
        self.__signal_thread_ocpp_server_recv_request = XSignal()
        self.__signal_thread_ocpp_server_recv_response = XSignal()
        self.__signal_thread_ocpp_server_recv_response_result = XSignal()
        self.__signal_thread_ocpp_server_finished = XSignal()
        self.__websocket = WebSocketServer(host, port)
        self.__list_request_message = []  # 存储待发送请求消息, 当列表非空则持续发送, 当列表为空则相应事件(__event_request_message)等待
        self.__list_response_message = []  # 存储待发送响应消息, 当列表非空则持续发送, 当列表为空则相应事件(__event_response_message)等待
        self.__event_request_message = asyncio.Event()  # 请求消息事件
        self.__event_response_message = asyncio.Event()  # 响应消息事件
        self.__isRunning = True  # 是否正在运行, 用于控制线程运行的开关
        try:
            if info_title is not None:
                self.__info_title = str(info_title)
        except:
            self.__send_signal_info(f'<Error - __init__> info_title must be convertible to a string. It has been set to None. The provided type is {type(info_title)}')
            self.__info_title = None
        # 版本兼容
        if str(charge_point_version).lower() in ['v16', 'v1.6', 'v1_6', 'ocpp16', 'ocpp1.6', 'ocpp1_6', '16']:
            from sys_basis.Charge_Point import ChargePointV16
            self.__charge_point = ChargePointV16(charge_point_name, self.__websocket)
        elif str(charge_point_version).lower() in ['v201', 'v2.0.1', 'v2_0_1', 'ocpp201', 'ocpp2.0.1', 'ocpp2_0_1', '201']:
            from sys_basis.Charge_Point import ChargePointV201
            self.__charge_point = ChargePointV201(charge_point_name, self.__websocket)
        else:
            raise ValueError(
                f'Invalid charge point version: {charge_point_version}. Valid versions are: \n\t- "v16", "v1.6", "v1_6", "ocpp16", "ocpp1.6", "ocpp1_6", \n\t- "v2.0.1", "v2_0_1", "ocpp201", "ocpp2.0.1", "ocpp2_0_1".')
        self.__charge_point.signal_charge_point_ocpp_request.connect(self.signal_thread_ocpp_server_recv_request.emit)
        self.__charge_point.signal_charge_point_ocpp_response.connect(self.signal_thread_ocpp_server_recv_response.emit)
        self.__charge_point.signal_charge_point_ocpp_response_result.connect(self.signal_thread_ocpp_server_recv_response_result.emit)
        self.__charge_point.signal_charge_point_info.connect(self.signal_thread_ocpp_server_info.emit)

    @property
    def signal_thread_ocpp_server_info(self) -> XSignal:
        return self.__signal_thread_ocpp_server_info

    @property
    def signal_thread_ocpp_server_recv_request(self) -> XSignal:
        return self.__signal_thread_ocpp_server_recv_request

    @property
    def signal_thread_ocpp_server_recv_response(self) -> XSignal:
        return self.__signal_thread_ocpp_server_recv_response

    @property
    def signal_thread_ocpp_server_recv_response_result(self) -> XSignal:
        return self.__signal_thread_ocpp_server_recv_response_result

    @property
    def signal_thread_ocpp_server_finished(self) -> XSignal:
        return self.__signal_thread_ocpp_server_finished

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def send_request_message(self, message: str) -> None:
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

    def send_response_message(self,  message_action: str, message, send_time: float) -> None:
        """ 
        发送响应消息, 结果将通过信号 __signal_thread_ocpp_server_recv_response_result 以字典形式发送, 结构如下: 
        - `action`: 消息类型
        - `data`: OCPP消息的字典形式
        - `send_time`: 接收的信号中的时间戳
        - `result`: 发送结果, True/False

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
        """
        self.__list_response_message.append((message_action, message, send_time))
        self.__event_response_message.set()

    def __send_signal_info(self, *args) -> None:
        """
        发送/打印 信息信号

        涵盖发送前的检查

        参数:
        - args: 可变数量的参数, 每个参数都应该是能够被转换为字符串的对象. 建议传递字符串、数字或任何有明确 `__str__` 或 `__repr__` 方法的对象, 以确保能够正确地将参数转换为字符串形式. 
        """
        self.__send_signal(signal=self.signal_thread_ocpp_server_info, error_hint='send_signal_info', log=None, doShowTitle=True, doPrintInfo=True, args=args)

    def __send_signal(self, signal: XSignal, error_hint: str, log=None, doShowTitle: bool = False, doPrintInfo: bool = False, args=[]) -> None:
        """
        发送/打印 信号

        涵盖发送前的检查

        参数:
        - signal(XSignal): 信号对象
        - error_hint(str): 错误提示
        - log: 日志器动作
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
                log(temp)

    async def __send_request_message(self) -> None:
        """ 
        发送请求消息, 循环执行

        当 send_request_message 被调用时, 会将消息放入队列中, 然后通过此方法发送

        当信息列表 __list_request_message 为空时, 将等待事件 __event_request_message 触发
        """
        while self.__isRunning:
            await self.__event_request_message.wait()
            if not self.__isRunning:  # 提起终止
                break
            try:
                # 此处结果将由 __charge_point.signal_charge_point_ocpp_response 传递, 无需手动处理
                await self.__charge_point.send_request_message(self.__list_request_message.pop(0))
            except:
                self.__send_signal_info(f'<Error - send_request_message>\n{traceback.format_exc}')
            if self.__list_request_message:
                self.__event_request_message.clear()

    async def __send_response_message(self) -> None:
        """ 
        发送响应消息, 循环执行

        当 send_response_message 被调用时, 会将消息放入队列中, 然后通过此方法发送

        当信息列表 __list_response_message 为空时, 将等待事件 __event_response_message 触发
        """
        while self.__isRunning:
            await self.__event_response_message.wait()
            if not self.__isRunning:  # 提起终止
                break
            try:
                # 此处结果将通过信号 signal_thread_ocpp_server_recv_response_result 传递, 无需手动处理
                result = await self.__charge_point.send_response_message(*self.__list_response_message.pop(0))
            except:
                self.__send_signal_info(f'<Error - send_response_message>\n{traceback.format_exc}')
            if self.__list_response_message:
                self.__event_response_message.clear()

    async def __start_charge_point_loop(self) -> None:
        """ 
        异步协程主体
        """
        async with self.__websocket:
            self.__task_listening = asyncio.create_task(self.__charge_point.start())
            setattr(self.__task_listening, 'task_name', 'task_listening')
            self.__task_send_request_messages = asyncio.create_task(self.__send_request_message())
            setattr(self.__task_listening, 'task_name', 'task_send_request_messages')
            self.__task_send_response_messages = asyncio.create_task(self.__send_response_message())
            setattr(self.__task_listening, 'task_name', 'task_send_response_messages')
            await asyncio.gather(self.__task_listening, self.__task_send_request_messages, self.__task_send_response_messages)
            await asyncio.Future()

    def stop(self) -> None:
        """
        终止线程

        `__isRunning` 将设置为 `False` , 并取消所有任务
        所有阻塞的信号量将被释放
        """
        self.__isRunning = False
        self.__event_request_message.set()
        self.__event_response_message.set()
        for task in [self.__task_listening, self.__task_send_request_messages, self.__task_send_response_messages]:
            if task:
                task.cancel()
                self.__send_signal_info(f'<Task Cancel> {task.task_name} is canceled')
        self.signal_thread_ocpp_server_finished.emit()

    def run(self) -> None:
        # asyncio.run(self.__start_charge_point_loop())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # self.__tasks.append(self.loop.create_task(self.__start_charge_point_loop()))
        self.loop.create_task(self.__start_charge_point_loop())
        self.loop.run_forever()
