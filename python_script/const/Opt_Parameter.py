
from const.Analog_Define import AnalogDefine
import os
from sys_basis.Optimize.data_gene import DataGene


os.chdir(os.path.dirname(os.path.dirname(__file__)))
APP_WORKSPACE_PATH = os.getcwd()


class OptParams(AnalogDefine):
    CHARGING_NEEDS_REQUEST_INTERVAL = 3600  # seconds
    OCPP_WEBSOCKET_TIMEOUT = 30  # seconds
    OCPP_WEBSOCKET_PORT = 12345
    EPRICES = DataGene.gene_eprices(0.33, 0.3, 6, 22)
    HIS_USAGE = DataGene.gene_his_usage_seed(3456)
