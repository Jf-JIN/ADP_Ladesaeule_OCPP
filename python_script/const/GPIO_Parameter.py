""" 
GPIO 枚举类


"""
from const.Analog_Define import AnalogDefine


class GPIOParams(AnalogDefine):
    MESSAGE_SEND_INTERVAL = 60  # seconds
    CHARGE_UNITS = [
        (0, '192.168.1.100'),
        # (1, 'url1'),
    ]
    MAX_VOLTAGE = 220
    SELF_CHECK_TIMEOUT = 31 # 自检超时时间
    GPIO_PIN_17 = 17
    GPIO_PIN_27 = 27


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


class ResultFlag(AnalogDefine):
    SUCCESS = 0
    FAIL = 1


class VehicleState(AnalogDefine):
    READY = 1
    EV_IS_PRESENT = 2
    CHARGING = 3
    CHARGING_WITH_VENTILATION = 4
    FAILURE = 5
