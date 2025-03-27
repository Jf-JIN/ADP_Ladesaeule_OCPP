"""
GPIO 枚举类


"""
from const.Analog_Define import AnalogDefine


class GPIOParams(AnalogDefine):
    VENDOR_ID = 'Darmstadt'
    MESSAGE_SEND_INTERVAL = 60  # seconds
    CHARGE_UNITS = [
        # (EVSE_Id, Shelly_main_url)
        # (1, '172.18.25.49:6666'),
        (1, 'http://192.168.124.9:6666'),
        # (1, 'http://130.83.148.29:6666'),

        # (0, '192.168.1.100'),
        # (1, 'url1'),
    ]
    DO_USE_RCD: bool = False
    MAX_VOLTAGE = 230
    SELF_CHECK_TIMEOUT = -31
    """ EVSE 自检时间, 单位: 秒. 该值必须 >=30 秒, 否则自检将不会启动 """
    LETCH_MOTOR_RUNTIME = 2
    """ 栓电机运行时间, 单位: 秒. 该值必须大于0秒, 否则电机将不会启动 """
    CALIBRATION_PERIOD = 60
    """ 校准周期, 单位: 秒. 该值必须大于0秒, 否则校准将不会启动 """
    POLLING_EVSE_INTERVAL = 1
    """ 轮询 EVSE 间隔, 单位: 秒. 该值必须大于0秒 """
    POLLING_SHELLY_INTERVAL = 1
    """ 轮询 Shelly 间隔, 单位: 秒. 该值必须大于0秒 """
    POLLING_SHELLY_TIMEOUT = 10
    """ Shelly 超时时间, 单位: 秒. 该值必须大于0秒 """
    DATACOLLECTOR_DATA_INTERVAL = 1
    """ 文字数据发送间隔, 单位: 秒. 该值必须大于0秒 """
    DATACOLLECTOR_FIG_INTERVAL = 1
    """ 图像数据发送间隔, 单位: 秒. 该值必须大于0秒 """
    REQUEST_INTERVAL = 1
    """ 请求间隔, 单位: 秒. 该值必须大于0秒 """


class ResultFlag(AnalogDefine):
    SUCCESS = 0
    FAIL = 1


class VehicleState(AnalogDefine):
    READY = 1  # 准备就绪, 可以开始充电
    EV_IS_PRESENT = 2  # 车辆已插入
    CHARGING = 3  # 充电中
    CHARGING_WITH_VENTILATION = 4  # 充电中, 需要通风
    FAILURE = 5  # 故障
    CRITICAL = 666  # 严重故障


class EVSEErrorInfo(AnalogDefine):
    RELAY_OFF = 'Relay Off'
    RELAY_ON = 'Relay On'
    DIODE_CHECK_FAIL = 'diode Check Fail'
    VENT_REQUIRED_FAIL = 'Vent Required Fail'
    WAITING_FOR_PILOT_RELEASE = 'Waiting For Pilot Release'
    RCD_CHECK_ERROR = 'RCD Check Error'
    RCD_CHECK_FAILED = 'RCD Check Failed'
    READ_ERROR = 'Read Error'
    WRITE_ERROR = 'Write Error'


class RaspPins(AnalogDefine):
    POWER_3V3_0 = 1
    POWER_5V_0 = 2
    GPIO_2 = 3
    POWER_5V_1 = 4
    GPIO_3 = 5
    GROUND_0 = 6
    GPIO_4 = 7
    GPI0_14 = 8
    GROUND_1 = 9
    GPI0_15 = 10
    GPI0_17 = 11
    GPI0_18 = 12
    GPI0_27 = 13
    GROUND_2 = 14
    GPI0_22 = 15
    GPI0_23 = 16
    POWER_3V3_1 = 17
    GPI0_24 = 18
    GPI0_10 = 19
    GROUND_3 = 20
    GPI0_9 = 21
    GPI0_25 = 22
    GPI0_11 = 23
    GPI0_8 = 24
    GROUND_4 = 25
    GPI0_7 = 26
    GPI0_0 = 27
    GPI0_1 = 28
    GPI0_5 = 29
    GROUND_5 = 30
    GPI0_6 = 31
    GPI0_12 = 32
    GPI0_13 = 33
    GROUND_6 = 34
    GPI0_19 = 35
    GPI0_16 = 36
    GPI0_26 = 37
    GPI0_20 = 38
    GROUND_7 = 39
    GPI0_21 = 40

    BCM_PIN_0 = 0
    BCM_PIN_1 = 1
    BCM_PIN_2 = 2
    BCM_PIN_3 = 3
    BCM_PIN_4 = 4
    BCM_PIN_5 = 5
    BCM_PIN_6 = 6
    BCM_PIN_7 = 7
    BCM_PIN_8 = 8
    BCM_PIN_9 = 9
    BCM_PIN_10 = 10
    BCM_PIN_11 = 11
    BCM_PIN_12 = 12
    BCM_PIN_13 = 13
    BCM_PIN_14 = 14
    BCM_PIN_15 = 15
    BCM_PIN_16 = 16
    BCM_PIN_17 = 17
    BCM_PIN_18 = 18
    BCM_PIN_19 = 19
    BCM_PIN_20 = 20
    BCM_PIN_21 = 21
    BCM_PIN_22 = 22
    BCM_PIN_23 = 23
    BCM_PIN_24 = 24
    BCM_PIN_25 = 25
    BCM_PIN_26 = 26
    BCM_PIN_27 = 27


class ModbusParams(AnalogDefine):
    PORT = '/dev/ttyS0'  # 串口号
    BAUDRATE = 9600  # 波特率
    PARITY = 'N'  # 无校验位
    STOPBITS = 1  # 停止位
    BYTESIZE = 8  # 数据位
    TIMEOUT = 3  # 超时时间
    RETRIES = 10  # 重试次数


class EVSERegAddress(AnalogDefine):
    CONFIGURED_AMPS = 1000
    AMPS_OUTPUT = 1001
    VEHICLE_STATE = 1002
    CURRENT_MAX = 1003
    TURN_OFF_SELFTEST_OPERATION = 1004  # turn off charging | self test operation
    FIRMWARE_REVISION = 1005
    EVSE_STATE = 1006
    EVSE_STATUS_FAILS = 1007
    TIMEOUT_ERROR = 1008
    TIMEOUT_SELFTEST = 1009
    # ...
    DEFAULT_AMPS = 2000
    SLAVE_ADDRESS = 2001
    CURRENT_MIN = 2002
    ANALOG_INPUT_CONFIG = 2003
    AMPS_SETTINGS = 2004
    CHARGE_OPERATION = 2005
    CURRENT_SHARING_MODE = 2006
    PP_DETECTION = 2007
    # ...
    BOOTLOADER_FIRMWARE_REVISION = 2009
    AMPS1 = 2010
    AMPS2 = 2011
    AMPS3 = 2012
    AMPS4 = 2013
    AMPS5 = 2014
    AMPS6 = 2015
    AMPS7 = 2016
    AMPS8 = 2017


class BitsFlag(AnalogDefine):

    class _REG1004(AnalogDefine):
        TURN_OFF_CHARGING_NOW: int = 1 << 0
        SELFTEST_RCDTEST: int = 1 << 1
        CLEAR_RCD_ERROR: int = 1 << 2

    class _REG1007(AnalogDefine):
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
        RELAY_OFF: int = 1 << 0
        DIODE_CHECK_FAIL: int = 1 << 1
        VENT_REQUIRED_FAIL: int = 1 << 2
        WAITING_FOR_PILOT_RELEASE: int = 1 << 3
        RCD_CHECK_ERROR: int = 1 << 4

    class _REG2005(AnalogDefine):
        ENABLE_BUTTON: int = 1 << 0
        ENABLE_STOP_BUTTON: int = 1 << 1
        PILOT_READE_LED: int = 1 << 2
        ENABLE_ON_VEHICLE_STATUS: int = 1 << 3
        ENABLE_RCD_FEEDBACK: int = 1 << 4
        AUTO_CLEAR_RCD_ERROR: int = 1 << 5
        AN_PULLUP: int = 1 << 6
        PWM_DEBUG: int = 1 << 7
        ERROR_LED: int = 1 << 8
        PILOT_AUTO_RECOVER_DELAY: int = 1 << 9
        ENABLE_STARTUP_DELAY: int = 1 << 12
        DISABLE_ESVE_AFTER_CHARGE: int = 1 << 13
        DISABLE_EVSE: int = 1 << 14
        ENABLE_BOOTLOADER_MODE: int = 1 << 15

    REG1004 = _REG1004()
    """ 
    turn off charging | self test operation | clear RCD error
    - `TURN_OFF_CHARGING_NOW`: turn off charging now
    - `SELFTEST_RCDTEST`: run selftest and RCD test procedure (approx. 30 seconds)
    - `CLEAR_RCD_ERROR`: clear RCD error
    """
    REG1007 = _REG1007()
    """ 
    EVSE status and fails:
    - `RELAY_OFF`: tuple: relay on/off
    - `DIODE_CHECK_FAIL`: tuple: diode check fail
    - `VENT_REQUIRED_FAIL`: tuple: vent required fail
    - `WAITING_FOR_PILOT_RELEASE`: tuple: waiting for pilot release (error recovery delay)
    - `RCD_CHECK_ERROR`: tuple: RCD check error
    """
    REG2005 = _REG2005()
    """ 
    charge operation
    - `ENABLE_BUTTON`: Enable button for current change (no sense when 2003 = 0)
        - default: 1
    - `ENABLE_STOP_BUTTON`: Stop charging when button pressed
        - charging will automatically start after you manually unplug and plug the cable to the vehicle
        - default: 0
    - `PILOT_READE_LED`: Pilot ready state LED
        - default: 0
    - `ENABLE_ON_VEHICLE_STATUS`: enable charging on vehicle status D (ventilation required)
        - default: 1
    - `ENABLE_RCD_FEEDBACK`: enable RCD feedback on MCLR pin (pin 4)
        - default: 0
    - `AUTO_CLEAR_RCD_ERROR`: auto clear RCD error
        - default: 0
    - `AN_PULLUP`: AN pullup (rev16 and later)
        - default: 0
    - `PWM_DEBUG`: PWM debug bit (rev17 and later)
        - default: 0
    - `ERROR_LED`: error LED routing to AN out (rev17 and later)
        - default: 0
    - `PILOT_AUTO_RECOVER_DELAY`: pilot auto recover delay (rev17 and later)
        - default: 1
    - `ENABLE_STARTUP_DELAY`: enable startup delay
    - `DISABLE_ESVE_AFTER_CHARGE`: disable EVSE after charge (write 8192)
    - `DISABLE_EVSE`: disable EVSE (write 16384)
    - `ENABLE_BOOTLOADER_MODE`: enable bootloader mode (write 32768)
    """
