
from ocpp.routing import on
from sys_basis.Generator_Ocpp_Std.V1_6 import *
from ._Charge_Point_Base import ChargePointBase
from ocpp.v16 import ChargePoint as cpv16


class ChargePointV16(cpv16, ChargePointBase):
    def __init__(self, id, connection, response_timeout=30):
        super().__init__(id, connection, response_timeout)
        self._init_parameters_in_baseclass()

    @on(Action.authorize)
    async def on_authorize_request(self, id_token: dict, custom_data: dict | None = None, certificate: str | None = None, hash_data: list | None = None):
        self._send_signal_info_and_ocpp_request(Action.authorize)

        default_message = '请修改此处默认信息, 参照_Charge_Point_Server_V2_0_1.py'

        return await self._wait_for_result(Action.authorize, default_message=default_message)
