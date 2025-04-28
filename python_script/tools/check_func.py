
import os
from const.Const_Parameter import APP_WORKSPACE_PATH
import json


def isPidRunning(pid):
    try:
        return os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


_cfdct = {}


def _write_default_config(config_path) -> dict:
    dct = {
        'ocpp_opt_host': 'ws://130.83.148.29',
        'ocpp_opt_port': 80,
        'charge_units': [(1, 'shellypro3em-2cbcbbb2e0b8.local'),],
        'max_voltage': 220,
        'max_shelly_retry': 5,
        'assumed_phase': 3,
        'self_check_timeout': -31,
        'letch_motor_runtime': 1,
        'calibration_period': 60,
        'polling_evse_interval': 1,
        'polling_shelly_interval': 1,
        'polling_shelly_timeout': 10,
        'datacollector_data_interval': 1,
        'datacollector_fig_interval': 1,
        'evse_write_retry': 10,
        'charging_stable_countdown': 10
    }
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(dct, indent=4, ensure_ascii=False))
        return dct
    except Exception as e:
        return {}


def import_data() -> dict:
    global _cfdct
    if _cfdct:
        return _cfdct
    config_path = os.path.join(APP_WORKSPACE_PATH, 'config_sys.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            _cfdct = config_data
            return _cfdct
        except Exception as e:
            _cfdct = _write_default_config(config_path)
            return _cfdct
    else:
        _cfdct = _write_default_config(config_path)
        return _cfdct
