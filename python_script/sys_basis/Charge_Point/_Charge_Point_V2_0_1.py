
import asyncio
import traceback
from ocpp.routing import on
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from ._Charge_Point_Base import ChargePointBase
from ocpp.v201 import ChargePoint as cpv201


class ChargePointV201(cpv201, ChargePointBase):
    def __init__(self, id, connection, response_timeout: int | float = 30):
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()

    async def send_request_message(self, message_action: str | Action, message):
        try:
            response = await self.call(message)
            response_text = {
                message_action: response
            }
            self.signal_ocpp_response.emit(message_action, response_text)
            print('\n->Response received 芜湖!>:', repr(response))
        except asyncio.TimeoutError:
            self._send_signal_info(f'< Error - Request - Response_Timeout > No response was received within {self.response_timeout_in_baseclass} seconds.')
        except Exception:
            self._send_signal_info(f'<Error - Request> {traceback.format_exc()}')

    @on(Action.authorize)
    async def on_authorize_request(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
        self._send_signal_info_and_ocpp_request(Action.authorize)

        default_message = authorize_response.generate(
            id_token_info=authorize_response.get_id_token_info('Unknown')
        )  # 词条需要修改, 根据实际需求考虑, 选择默认消息, 这个只是示例

        return await self._wait_for_result(Action.authorize, default_message)

    @on(Action.boot_notification)
    async def on_authorize_request000(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
        self._send_signal_info_and_ocpp_request(Action.authorize)

        default_message = authorize_response.generate(
            id_token_info=authorize_response.get_id_token_info('Unknown')
        )  # 词条需要修改, 根据实际需求考虑, 选择默认消息, 这个只是示例

        return await self._wait_for_result(Action.authorize, default_message)
