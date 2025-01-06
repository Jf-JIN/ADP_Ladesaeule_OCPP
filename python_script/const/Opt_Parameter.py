
from const.Analog_Define import AnalogDefine
import os


class OptParams(AnalogDefine):
    CHARGING_NEEDS_REQUEST_INTERVAL = 3600  # seconds
    OCPP_WEBSOCKET_TIMEOUT = 30  # seconds
    OCPP_WEBSOCKET_PORT = 12345
