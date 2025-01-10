from ocpp.v16.enums import *
from ocpp.v16 import call
from ._Base import *


class GenMeterValuesRequest(Base_OCPP_Struct_V1_6):

    @staticmethod
    def generate(
        connector_id: int,
        meter_value: list,
        transaction_id: int | None = None
    ) -> call.MeterValues:
        """
        Generate MeterValuesRequest

        - Args: 
            - connector_id(int): 
            - meter_value(list): 
                - recommended to use `get_meter_value()` to set element or to build a custom list.
            - transaction_id(int|None): 

        - Returns:
            - call.MeterValues
        """
        return call.MeterValues(
            connector_id=connector_id,
            meter_value=meter_value,
            transaction_id=transaction_id
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.MeterValues:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.MeterValues
        """
        return call.MeterValues(
            connector_id=dict_data['connectorId'],
            meter_value=dict_data['meterValue'],
            transaction_id=dict_data.get('transactionId', None)
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
                - Enum: `Wh`, `kWh`, `varh`, `kvarh`, `W`, `kW`, `VA`, `kVA`, `var`, `kvar`, `A`, `V`, `K`, `Celcius`, `Celsius`, `Fahrenheit`, `Percent`, `Hertz`
                - Or use EnumClass (Recommended): `UnitOfMeasure`. e.g. `UnitOfMeasure.wh`

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
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
    def get_meter_value(
        timestamp: str,
        sampled_value: list
    ) -> dict:
        """
        Get meter value

        - Args: 
            - timestamp(str): 
                - format: date-time
            - sampled_value(list): 
                - recommended to use `get_sampled_value()` to set element or to build a custom list.

        - Returns:
            - temp_dict(dict)
        """
        temp_dict: dict = {
            'timestamp': timestamp,
            'sampledValue': sampled_value
        }
        return temp_dict
