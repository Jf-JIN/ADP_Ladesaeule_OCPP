
import asyncio
import time
import traceback
from ocpp.routing import on
from const.Charge_Point_Parameters import CP_Params
from sys_basis.Generator_Ocpp_Std.V1_6 import *
from ._Charge_Point_Base import ChargePointBase
from ocpp.v16 import ChargePoint as cpv16


class ChargePointV16(cpv16, ChargePointBase):
    """ 
    OCPP v1.6 信息端口类
    用于监听 ocpp 消息, 以及发送 ocpp 消息

    - 信号: 
        - signal_charge_point_ocpp_request(dict): OCPP请求消息信号(向系统传递外部请求), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
        - signal_charge_point_ocpp_response(dict): OCPP响应消息信号(向系统传递外部响应), 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
            - `response_status`(int): 响应状态, 表示响应是否成功收到. 
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`
        - signal_charge_point_ocpp_response_result(dict): OCPP响应消息结果信号. 向系统反馈消息是否在响应时间内发送出去了, 包含具体发送信息的内容, 与函数返回值不同的一点在于其记录了详细的消息信息, 可以用于后续对发送失败的消息进行处理, 内容为字典, 结构如下
            - `action`(str): 消息类型
            - `data`(dict): OCPP消息的字典形式
            - `send_time`(float): 接收的信号中的时间戳
            - `status`(int): 发送结果
                - 枚举类 `CP_Params.RESPONSE_RESULT`
                - 枚举项: `SUCCESS`, `TIMEOUT`
        - signal_charge_point_info(str): 普通信号, 用于信息显示, 调试等

    - 属性: 
        - response_timeout_in_baseclass(int|float)

    - 方法: 
        - send_request_message: 发送请求消息
        - send_response_message: 发送响应消息
        - show_current_message_to_send : 显示当前待发送的消息队列
        - show_time_table_for_send_message : 显示当前待发送消息的时间表
        - set_response_timeout: 设置响应超时时间

    """

    def __init__(self, id, connection, response_timeout: int | float = 30):
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()
        self._set_network_buffer_time_in_baseclass(CP_Params.NETWORK_BUFFER_TIME)
        # self._set_doSendDefaultResponse(True)

    async def send_request_message(self, message):
        """ 
        发送请求消息 (不清楚调用的call会不会因版本不同而有差别, 所以写在子类这里)

        数据将通过信号 `signal_charge_point_ocpp_response` 发送回来, 数据格式如下: 
            - `action`(str): 消息类型
            - `data`(dict): 解包后的数据
            - `send_time`(float): 请求发送时间
            - `response_status`(int): 响应状态, 
                - 枚举类 `CP_Params.RESPONSE`
                - 枚举项: `SUCCESS`, `TIMEOUT`, `ERROR`

        当请求发送后, 将等待响应数据. 有如下三种情况: 
        1. 成功接收响应数据
        2. 超时未接收到响应数据
        3. 其他错误

        参数: 
        - message: 请求消息对象, OCPP数据类, 如: `call.Authorize`

        返回: 
        - 无
        """
        request_time = time.time()
        try:
            response = await self.call(message)
            # signal_charge_point_ocpp_response 将在此函数发送
            self._unpack_data_and_send_signal_ocpp_response(response, request_time)
        except asyncio.TimeoutError:
            self._send_signal_info(f'< Error - Request - Response_Timeout > No response was received within {self.response_timeout_in_baseclass} seconds.')
            self.__signal_charge_point_ocpp_response.emit(
                {
                    'action': message.__class__.__name__,
                    'data': {},
                    'send_time': request_time,
                    'response_status': CP_Params.RESPONSE.TIMEOUT,
                }
            )
        except Exception:
            self._send_signal_info(f'<Error - Request> {traceback.format_exc()}')
            self.__signal_charge_point_ocpp_response.emit(
                {
                    'action': message.__class__.__name__,
                    'data': {},
                    'send_time': request_time,
                    'response_status': CP_Params.RESPONSE.ERROR,
                }
            )

    @on(Action.authorize)
    async def _on_authorize_request(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
        self._send_signal_info_and_ocpp_request(Action.authorize)

        default_message = '请修改此处默认信息, 参照_Charge_Point_Server_V2_0_1.py'

        return await self._wait_for_result(Action.authorize, default_message=default_message)
