
from const.Analog_Define import AnalogDefine
import os


os.chdir(os.path.dirname(os.path.dirname(__file__)))
APP_WORKSPACE_PATH = os.getcwd()


class OptParams(AnalogDefine):
    CHARGING_NEEDS_REQUEST_INTERVAL = 3600  # seconds
