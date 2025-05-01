
from const.Analog_Define import AnalogDefine
from tools.data_gene import DataGene


class OptParams(AnalogDefine):
    EPRICES = DataGene.gene_eprices(0.33, 0.3, 6, 22)
    # HIS_USAGE = DataGene.gene_his_usage_seed(3456)
    HIS_USAGE = DataGene.gene_his_usage()
    MAX_GRID_POWER = 6000
    CHARGING_INTERVAL = 15  # minute
    NUM_RETRY_MAX = 3
