
from const.Analog_Define import AnalogDefine


class _Response(AnalogDefine):
    SUCCESS = 0
    TIMEOUT = 1
    ERROR = 2


class _Response_Result(AnalogDefine):
    SUCCESS = 0
    TIMEOUT = 1


class CP_Params(AnalogDefine):
    RESPONSE = _Response()
    RESPONSE_RESULT = _Response_Result()
    NETWORK_BUFFER_TIME = 1
    RESPONSE_DELAY_TIME = 1
