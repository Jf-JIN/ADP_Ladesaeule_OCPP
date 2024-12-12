
from ocpp.routing import on
from sys_basis.Generator_Ocpp_Std.V2_0_1 import *
from ._Charge_Point_Server_Base import ChargePointServerBase
from ocpp.v201 import ChargePoint as cpv201


class ChargePointServerV201(cpv201, ChargePointServerBase):
    def __init__(self, id, connection, response_timeout=30):
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()
        self._set_response_timeout_in_baseclass(response_timeout)

    @on(Action.authorize)
    async def on_authorize_request(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
        self._send_signal_info_and_ocpp_message(Action.authorize)

        default_message = authorize_response.generate(
            id_token_info=authorize_response.get_id_token_info('Unknown')
        )  # 词条需要修改, 根据实际需求考虑, 选择默认消息, 这个只是示例

        return await self._wait_for_result(Action.authorize, default_message)
