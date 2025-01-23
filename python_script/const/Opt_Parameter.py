
from const.Analog_Define import AnalogDefine
from tools.data_gene import DataGene


class OptParams(AnalogDefine):
    CHARGING_NEEDS_REQUEST_INTERVAL = 3600  # seconds
    EPRICES = DataGene.gene_eprices(0.33, 0.3, 6, 22)
    # HIS_USAGE = DataGene.gene_his_usage_seed(3456)
    HIS_USAGE = DataGene.gene_his_usage()
