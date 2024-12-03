
from const.Analog_Define import AnalogDefine
import os


os.chdir(os.path.dirname(os.path.dirname(__file__)))
APP_WORKSPACE_PATH = os.getcwd()


class Parameter(AnalogDefine):
    EXAMPLE = 'Example'
