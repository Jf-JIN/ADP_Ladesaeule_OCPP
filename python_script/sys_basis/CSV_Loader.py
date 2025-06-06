import csv
import io
from const.Const_Parameter import *
from enum import StrEnum, IntEnum

_log = Log.CSVLoader


class _CSVEnum():
    class Line(IntEnum):
        evseId = 0
        chargingProfileID = 1
        stackLevel = 2
        chargingProfilePurpose = 3
        chargingProfileKind = 4
        ChargingScheduleID = 5
        chargingRateUnit = 6
        startSchedule = 8
        chargingSchedule = 10

    class Value(IntEnum):
        evseId = 1
        chargingProfileID = 1
        stackLevel = 1
        chargingProfilePurpose = 1
        chargingProfileKind = 1
        ChargingScheduleID = 1
        chargingRateUnit = 1
        startSchedule = 1
        startPeriod = 0
        limit = 1

    class Key(StrEnum):
        evseId = 'evseId'
        chargingProfile = 'chargingProfile'
        chargingProfileID = 'id'
        chargingProfileID_CSV = 'chargingProfileID'
        stackLevel = 'stackLevel'
        chargingProfilePurpose = 'chargingProfilePurpose'
        chargingProfileKind = 'chargingProfileKind'
        chargingSchedule = 'chargingSchedule'
        ChargingScheduleID = 'id'
        ChargingScheduleID_CSV = 'ChargingScheduleID'
        chargingRateUnit = 'chargingRateUnit'
        startSchedule = 'startSchedule'
        chargingSchedulePeriod = 'chargingSchedulePeriod'
        startPeriod = 'startPeriod'
        limit = 'limit'


class CSVErrorMsg(StrEnum):
    missing_params = 'Missing Parameters\n缺少参数'
    invalid_unit = 'Unit Parameter Error, available value:["W", "A"]\n单位参数错误, 可选值:["W", "A"]'


class CSVLoader:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance__:
            cls.__instance__ = super().__new__(cls)
            cls.__instance__.__initialized__ = False
        return cls.__instance__

    def __init__(self, parent=None):
        if self.__initialized__:
            return
        self.__initialized__ = True
        super().__init__()
        self.__parent = parent
        self.__data = {}

    @staticmethod
    def loadCSV(csv_data: str) -> dict | str:
        instance = CSVLoader()
        return instance.__analyse(csv_data)

    def __analyse(self, csv_data: str) -> dict | str:
        temp = {
            _CSVEnum.Key.chargingProfile: {
                _CSVEnum.Key.chargingSchedule: [
                    {
                        _CSVEnum.Key.chargingSchedulePeriod: []
                    }
                ]
            }
        }
        try:
            csv_data = io.StringIO(csv_data)
            data = csv.reader(csv_data)
            key_counts = 0
            plan_counts = 0
            for idx, row in enumerate(data):
                if not row:
                    continue
                item0 = row[0].strip()
                item1 = row[1].strip()
                if item0 == _CSVEnum.Key.evseId:
                    temp[_CSVEnum.Key.evseId] = int(item1)
                    key_counts += 1
                elif item0 == _CSVEnum.Key.chargingProfileID_CSV:
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingProfileID] = int(item1)
                    key_counts += 1
                elif item0 == _CSVEnum.Key.stackLevel:
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.stackLevel] = int(item1)
                    key_counts += 1
                elif item0 == _CSVEnum.Key.chargingProfilePurpose:
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingProfilePurpose] = item1
                    key_counts += 1
                elif item0 == _CSVEnum.Key.chargingProfileKind:
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingProfileKind] = item1
                    key_counts += 1
                elif item0 == _CSVEnum.Key.ChargingScheduleID_CSV:
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingSchedule][0][_CSVEnum.Key.ChargingScheduleID] = int(item1)
                    key_counts += 1
                elif item0 == _CSVEnum.Key.chargingRateUnit:
                    if item1.upper() not in ["W", "A"]:
                        return CSVErrorMsg.invalid_unit
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingSchedule][0][_CSVEnum.Key.chargingRateUnit] = item1.upper()
                    key_counts += 1
                elif item0 == _CSVEnum.Key.startSchedule:
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingSchedule][0][_CSVEnum.Key.startSchedule] = item1
                    key_counts += 1
                elif item0.isdigit() and item1.isdigit():
                    temp[_CSVEnum.Key.chargingProfile][_CSVEnum.Key.chargingSchedule][0][_CSVEnum.Key.chargingSchedulePeriod].append(
                        {
                            _CSVEnum.Key.startPeriod: int(item0),
                            _CSVEnum.Key.limit: int(item1)
                        }
                    )
                    plan_counts += 1
            if plan_counts:
                key_counts += 1
            if key_counts == 9:
                self.__data: dict = temp
                return temp
            else:
                return CSVErrorMsg.missing_params
        except Exception as e:
            _log.exception()
            return str(e)

    @staticmethod
    def getData() -> dict:
        instance = CSVLoader()
        return instance.__data

    @staticmethod
    def clear() -> None:
        instance = CSVLoader()
        return instance.__data.clear()
