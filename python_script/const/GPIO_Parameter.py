
from const.Analog_Define import AnalogDefine


class GPIOParams(AnalogDefine):
    MESSAGE_SEND_INTERVAL = 60  # seconds
    PORT = '/dev/ttyS0'
    BAUDRATE = 9600
    POLL_INTERVAL = 5 #EVSE状态检查
    POLL_INTERVAL_CHECK = 1 #车辆状态检查
    POLL_INTERVAL_SHELLY = 1
    PARITY = 'N' # 无校验位
    STOPBITS = 1 # 停止位
    BYTESIZE = 8  # 数据位
    TIMEOUT = 1  # 超时时间
    SHELLY_IP = "192.168.1.100"#Shelly IP地址
    SHELLY_EMETER_INDEX = 0 #Shelly电表索引


class ResultFlag(AnalogDefine):
    SUCCESS = 0
    FAIL = 1

class REG1004(AnalogDefine):
    TURN_OFF_CHARGING_NOW = 0b00000001 #BIT0
    RUN_SELFTEST_AND_RCD_TEST_PROCEDURE = 0b00000010 #BIT1
    CLEAR_RCD_ERROR = 0b00000100 #BIT2

class EVSEFails(AnalogDefine):
    """
    EVSE status and fails:
        bit0: relay on/off (暂定0 = on, 1 = off)
        bit1: diode check fail
        bit2: vent required fail
        bit3: waiting for pilot release (error recovery delay)
        bit4: RCD check error
        bit5:
        bit6-bit15: reserved
    """
    RELAY_OFF = 0b00000001 #BIT0
    DIODE_CHECK_FAIL = 0b00000010 #BIT1
    VENT_REQUIRED_FAIL = 0b00000100 #BIT2
    WAITING_FOR_PILOT_RELEASE = 0b00001000 #BIT3
    RCD_CHECK_ERROR = 0b00010000 #BIT4
    NUM_BIT = 5

class REG2005(AnalogDefine):
    RCD_FEEDBACK_ENABLE = 0b00010000 #BIT4

class VehicleState(AnalogDefine):

    READY = 1
    EV_IS_PRESENT = 2
    CHARGING = 3
    CHARGING_WITH_VENTILATION = 4
    FAILURE = 5