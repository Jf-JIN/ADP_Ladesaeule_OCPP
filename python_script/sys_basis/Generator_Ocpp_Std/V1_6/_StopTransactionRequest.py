from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenStopTransactionRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        meter_stop: int,
        timestamp: str,
        transaction_id: int,
        id_tag: str | None = None,
        reason: str | Reason | None = None,
        transaction_data: list | None = None
    ) -> call.StopTransaction:
        """
        Generate StopTransactionRequest

        - Args: 
            - meter_stop(int): 
            - timestamp(str): 
                - format: date-time
            - transaction_id(int): 
            - id_tag(str|None): 
                - length limit: [1, 20]
            - reason(str|Reason|None): 
                - Enum: `EmergencyStop`, `EVDisconnected`, `HardReset`, `Local`, `Other`, `PowerLoss`, `Reboot`, `Remote`, `SoftReset`, `UnlockCommand`, `DeAuthorized`
                - Or use EnumClass (Recommended): `Reason`. e.g. `Reason.emergency_stop`
            - transaction_data(list|None): 
                - recommended to use `get_transaction_data()` to set element or to build a custom list.

        - Returns:
            - call.StopTransaction
        """
        return call.StopTransaction(
            meter_stop = meter_stop,
            timestamp = timestamp,
            transaction_id = transaction_id,
            id_tag = id_tag,
            reason = reason,
            transaction_data = transaction_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.StopTransaction:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.StopTransaction
        """
        return call.StopTransaction(
            meter_stop = dict_data['meterStop'],
            timestamp = dict_data['timestamp'],
            transaction_id = dict_data['transactionId'],
            id_tag = dict_data.get('idTag', None),
            reason = dict_data.get('reason', None),
            transaction_data = dict_data.get('transactionData', None)
        )


    @staticmethod
    def get_sampled_value(
        value: str,
        context: str | ReadingContext | None = None,
        format: str | ValueFormat | None = None,
        measurand: str | Measurand | None = None,
        phase: str | Phase | None = None,
        location: str | Location | None = None,
        unit: str | UnitOfMeasure | None = None
    ) -> dict:
        """
        Get sampled value

        - Args: 
            - value(str): 
            - context(str|ReadingContext|None): 
                - Enum: `Interruption.Begin`, `Interruption.End`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`, `Other`
                - Or use EnumClass (Recommended): `ReadingContext`. e.g. `ReadingContext.interruption.begin`
            - format(str|ValueFormat|None): 
                - Enum: `Raw`, `SignedData`
                - Or use EnumClass (Recommended): `ValueFormat`. e.g. `ValueFormat.raw`
            - measurand(str|Measurand|None): 
                - Enum: `Energy.Active.Export.Register`, `Energy.Active.Import.Register`, `Energy.Reactive.Export.Register`, `Energy.Reactive.Import.Register`, `Energy.Active.Export.Interval`, `Energy.Active.Import.Interval`, `Energy.Reactive.Export.Interval`, `Energy.Reactive.Import.Interval`, `Power.Active.Export`, `Power.Active.Import`, `Power.Offered`, `Power.Reactive.Export`, `Power.Reactive.Import`, `Power.Factor`, `Current.Import`, `Current.Export`, `Current.Offered`, `Voltage`, `Frequency`, `Temperature`, `SoC`, `RPM`
                - Or use EnumClass (Recommended): `Measurand`. e.g. `Measurand.energy.active.export.register`
            - phase(str|Phase|None): 
                - Enum: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1`
                - Or use EnumClass (Recommended): `Phase`. e.g. `Phase.l1`
            - location(str|Location|None): 
                - Enum: `Cable`, `EV`, `Inlet`, `Outlet`, `Body`
                - Or use EnumClass (Recommended): `Location`. e.g. `Location.cable`
            - unit(str|UnitOfMeasure|None): 
                - Enum: `Wh`, `kWh`, `varh`, `kvarh`, `W`, `kW`, `VA`, `kVA`, `var`, `kvar`, `A`, `V`, `K`, `Celcius`, `Celsius`, `Fahrenheit`, `Percent`
                - Or use EnumClass (Recommended): `UnitOfMeasure`. e.g. `UnitOfMeasure.wh`

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'value': value
        }
        if context is not None:
            temp_dict['context'] = context
        if format is not None:
            temp_dict['format'] = format
        if measurand is not None:
            temp_dict['measurand'] = measurand
        if phase is not None:
            temp_dict['phase'] = phase
        if location is not None:
            temp_dict['location'] = location
        if unit is not None:
            temp_dict['unit'] = unit
        return temp_dict


    @staticmethod
    def get_transaction_data(
        timestamp: str,
        sampled_value: list
    ) -> dict:
        """
        Get transaction data

        - Args: 
            - timestamp(str): 
                - format: date-time
            - sampled_value(list): 
                - recommended to use `get_sampled_value()` to set element or to build a custom list.

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'timestamp': timestamp,
            'sampledValue': sampled_value
        }
        return temp_dict

