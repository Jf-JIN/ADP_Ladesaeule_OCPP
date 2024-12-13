
import asyncio
import time
import traceback
from ocpp.routing import on
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from ._Charge_Point_Base import ChargePointBase
from ocpp.v201 import ChargePoint as cpv201


class ChargePointV201(cpv201, ChargePointBase):
    """ 
    OCPP v2.0.1 信息端口类
    用于监听 ocpp 消息, 以及发送 ocpp 消息

    信号: 
    - signal_charge_point_ocpp_request: OCPP请求消息信号, 内容为字典, 结构如下
        - `action`: 消息类型
        - `data`: OCPP消息的字典形式
        - `send_time`: 请求收到时间 / 向系统发送时间, 这里的 send 含义是从 OCPP端口 向系统发送的动作
    - signal_charge_point_ocpp_response: OCPP响应消息信号
        - `action`: 消息类型
        - `data`: OCPP消息的字典形式
        - `send_time`: 请求发送时间,  这里send 含义是从 OCPP端口 向外部发送的动作
    - signal_charge_point_info: 普通信号, 用于信息显示, 调试等

    属性: 
    - response_timeout_in_baseclass(int|float)

    方法: 
    - send_request_message: 发送请求消息
    - send_response_message: 发送响应消息
    - show_current_message_to_send : 显示当前待发送的消息队列
    - show_time_table_for_send_message : 显示当前待发送消息的时间表
    - set_response_timeout: 设置响应超时时间

    """

    def __init__(self, id, connection, response_timeout: int | float = 30):
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()

    async def send_request_message(self, message):
        """ 
        发送请求消息

        当请求发送后, 将等待响应数据. 有如下三种情况: 

        1. 成功接收响应数据, 数据将通过信号 `signal_ocpp_response` 发送出去, 数据格式如下: 
            - `action`: 消息类型
            - `data`: OCPP消息的字典形式
            - `send_time`: 请求发送时间
        2. 超时未接收到响应数据, 将通过信号 `signal_info` 发送报错信息, `signal_ocpp_response` 不发送信息
        3. 其他错误, 将通过信号 `signal_info` 发送报错信息, `signal_ocpp_response` 不发送信息

        参数: 
        - message: 请求消息对象, OCPP数据类, 如: `call.Authorize`

        返回: 
        - 无
        """
        try:
            request_time = time.time()
            response = await self.call(message)
            self._unpack_data_and_send_signal_ocpp_response(response, request_time)
        except asyncio.TimeoutError:
            self._send_signal_info(f'< Error - Request - Response_Timeout > No response was received within {self.response_timeout_in_baseclass} seconds.')
        except Exception:
            self._send_signal_info(f'<Error - Request> {traceback.format_exc()}')

    @on(Action.authorize)
    async def _on_authorize_request(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
        self._send_signal_info_and_ocpp_request(Action.authorize)

        default_message = authorize_response.generate(
            id_token_info=authorize_response.get_id_token_info('Unknown')
        )  # 词条需要修改, 根据实际需求考虑, 选择默认消息, 这个只是示例
        return await self._wait_for_result(Action.authorize, default_message)
