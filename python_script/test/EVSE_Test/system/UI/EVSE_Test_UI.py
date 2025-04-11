

import functools
from PyQt5.QtWidgets import QTableWidgetItem
from system.Socket_Core import SocketCore
from system.UI.EVSE_Test_UI_ui import *
import socket
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import typing
import pprint
import datetime

from system.Modbus_Handler import *
from system.Socket_Core import *
from system.Latch_Motor import *
from const.Const_Logger import *
from const.Const_Icon import *


_log = Log.UI

UNDEF_STR = 'Undefine'
_TABLE_WIDGET_COLUMN_MIN_WIDTH = 40

_DEFAULT_WIDGET_COLUMN_WIDTH = 140


class _PDUTableStruct:
    signal_data_changed: EventSignal = EventSignal()
    __instance__ = None

    def __new__(cls, *args, **kwargs) -> typing.Self:
        if cls.__instance__ is None:
            cls.__instance__: typing.Self = super().__new__(cls)
            cls.__instance__.__isinitialized__ = False
        return cls.__instance__

    def __init__(self):
        if self.__isinitialized__:
            return
        self.__isinitialized__ = True
        self.__PDU_dict = {}

    @staticmethod
    def setValue(value: dict) -> None:
        _PDUTableStruct.__instance__.set_value(value)
        return

    @staticmethod
    def addValue(register_address: int, value: ModbusDataStruct) -> None:
        _PDUTableStruct.__instance__.add_value(register_address, value)
        return

    @staticmethod
    def addRegisterAddress(register_address: int) -> None:
        _PDUTableStruct.__instance__.add_register_address(register_address)
        return

    @staticmethod
    def removeValue(register_address: int) -> None:
        _PDUTableStruct.__instance__.remove_value(register_address)
        return

    @staticmethod
    def clearData() -> None:
        _PDUTableStruct.__instance__.clear_data()
        return

    @staticmethod
    def getData() -> dict:
        return _PDUTableStruct.__instance__.get_data()

    @staticmethod
    def getStruct(register_address: int) -> ModbusDataStruct | None:
        return _PDUTableStruct.__instance__.get_struct(register_address)

    @staticmethod
    def getRegisterAddressList() -> list:
        return _PDUTableStruct.__instance__.get_register_address_list()

    def set_value(self, value: dict) -> typing.Self:
        if not isinstance(value, dict):
            _log.warning("PDU_dict must be a dictionary")
            return self
        if value == self.__PDU_dict:
            return self
        self.__PDU_dict = value
        self.signal_data_changed.emit()
        return self

    def add_register_address(self, register_address: int) -> typing.Self:
        if not isinstance(register_address, int):
            _log.warning(f"register_address in <_PDUTableStruct> must be an integer")
            return self
        register_address = int(register_address)
        if register_address in self.__PDU_dict:
            _log.warning(f"register_address {register_address} already exists in <_PDUTableStruct>")
            return self
        self.__PDU_dict[register_address] = None
        _log.info(f"register_address {register_address} added to <_PDUTableStruct>")
        self.signal_data_changed.emit()
        return self

    def add_value(self, register_address: int, value: ModbusDataStruct) -> typing.Self:
        if not isinstance(register_address, int) or not isinstance(value, ModbusDataStruct):
            _log.warning(f"register_address and value in <_PDUTableStruct::add_value> should be int and ModbusDataStruct, but got {type(register_address)} and {type(value)}")
            return self
        register_address = int(register_address)
        if register_address in self.__PDU_dict and self.__PDU_dict[register_address] == value:
            return self
        self.__PDU_dict[register_address] = value
        self.signal_data_changed.emit()
        return self

    def remove_value(self, register_address: int) -> typing.Self:
        if not isinstance(register_address, int):
            _log.warning(f"register_address in <_PDUTableStruct::remove_value> should be int, but got {type(register_address)}")
            return self
        register_address = int(register_address)
        if register_address in self.__PDU_dict:
            self.__PDU_dict.pop(register_address)
            self.signal_data_changed.emit()
        else:
            _log.warning(f"register_address in <_PDUTableStruct::remove_value> should be int, but got {type(register_address)}")
        return self

    def clear_data(self) -> typing.Self:
        self.__PDU_dict.clear()
        self.signal_data_changed.emit()
        return self

    def get_data(self) -> dict:
        return self.__PDU_dict

    def get_register_address_list(self) -> list:
        return list(self.__PDU_dict.keys())

    def get_struct(self, register_address: int) -> ModbusDataStruct | None:
        if not isinstance(register_address, int):
            _log.warning(f"register_address in <_PDUTableStruct::get_struct> should be int, but got {type(register_address)}")
            return None
        register_address = int(register_address)
        if register_address in self.__PDU_dict:
            return self.__PDU_dict[register_address]
        else:
            _log.warning(f"register_address in <_PDUTableStruct::get_struct> should be int, but got {type(register_address)}")
            return None

    @property
    def length(self) -> int:
        return len(self.__PDU_dict)


class EVSETestUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__init_parameters()
        self.__init_ui()
        self.__init_signal_connections()
        self.show()

    def __init_parameters(self):
        self.__PDU_struct = _PDUTableStruct()
        self.__socket_obj: SocketCore | None = None
        self.__available_modbus_id = set()
        self.__reflect_recv_dict = {
            'modbus_data_read': self.__handle_read_response,
        }
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__send_read_request_loop)
        self.__timer.start(1000)

    def __init_ui(self) -> None:
        self.setWindowTitle("EVSE Test")

        labels = [
            "Reg_Addr",
            "function_code",
            "isError",
            "exception_code",
            "dev_id",
            "transaction_id",
            "bits",
            "address",
            "registers",
            "status", ]
        self.tableWidget_all_register.setColumnCount(len(labels))
        self.tableWidget_all_register.setHorizontalHeaderLabels(labels)
        # self.tableWidget_all_register.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_all_register.horizontalHeader().setMinimumSectionSize(_TABLE_WIDGET_COLUMN_MIN_WIDTH)
        self.tableWidget_all_register.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.tableWidget_all_register.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_all_register.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidget_all_register.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableWidget_all_register.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableWidget_all_register.verticalHeader().setVisible(False)
        for idx, _ in enumerate(labels):
            self.tableWidget_all_register.setColumnWidth(idx, _DEFAULT_WIDGET_COLUMN_WIDTH)

        self.le_socket_id.setPlaceholderText(SocketEnum.HOST_PLACEHLODER)

        self.sp_modbus_id.setMaximum(255)
        self.sp_modbus_id.setMinimum(0)
        self.sp_modbus_id.setValue(1)
        self.sp_modbus_id.wheelEvent = lambda event: None

        self.le_add_register.setClearButtonEnabled(True)
        self.le_register_address.setClearButtonEnabled(True)
        self.le_socket_id.setClearButtonEnabled(True)
        self.le_write_value.setClearButtonEnabled(True)

        self.pb_add.setIcon(QIcon(self.__convert_svg_to_pixmap(PLUS)))
        self.pb_remove.setIcon(QIcon(self.__convert_svg_to_pixmap(MINUS)))
        self.pb_add.setIconSize(QSize(20, 20))
        self.pb_remove.setIconSize(QSize(20, 20))

        self.setStyleSheet(""" font: 16px "Arial"; """)

    def __init_signal_connections(self) -> None:
        self.pb_add.clicked.connect(self.__on_pb_add_clicked)
        self.pb_remove.clicked.connect(self.__on_pb_remove_clicked)
        self.pb_read.clicked.connect(self.__on_pb_read_clicked)
        self.pb_write.clicked.connect(self.__on_pb_write_clicked)
        self.pb_connect.clicked.connect(self.__on_pb_connect_clicked)
        self.__PDU_struct.signal_data_changed.connect(self.updata_tableWidget)
        self.pb_lock.clicked.connect(self.__run_motor_lock)
        self.pb_unlock.clicked.connect(self.__run_motor_unlock)
        self.pb_shutdown.clicked.connect(self.__on_pb_shut_down)
        self.le_socket_id.editingFinished.connect(self.__on_pb_connect_clicked)

    def updata_tableWidget(self):
        self.tableWidget_all_register.clearContents()
        unit_count: int = self.__PDU_struct.length
        self.tableWidget_all_register.setRowCount(unit_count)
        data_dict = self.__PDU_struct.get_data()
        for index_row, (register_address, struct) in enumerate(data_dict.items()):
            struct: ModbusDataStruct
            item_register_address = QTableWidgetItem(str(register_address))
            item_isError = QTableWidgetItem(str(struct.isError)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_exception_code = QTableWidgetItem(str(struct.exception_code)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_function_code = QTableWidgetItem(str(struct.function_code)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_dev_id = QTableWidgetItem(str(struct.dev_id)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_transaction_id = QTableWidgetItem(str(struct.transaction_id)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_bits = QTableWidgetItem(str(struct.bits)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_address = QTableWidgetItem(str(struct.address)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_registers = QTableWidgetItem(str(struct.registers)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            item_status = QTableWidgetItem(str(struct.status)) if struct is not None else QTableWidgetItem(UNDEF_STR)
            for index_column, item in enumerate([
                    item_register_address,
                    item_function_code,
                    item_isError,
                    item_exception_code,
                    item_dev_id,
                    item_transaction_id,
                    item_bits,
                    item_address,
                    item_registers,
                    item_status,]):
                item.setData(Qt.UserRole, str(register_address))
                item.setToolTip(str(register_address))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.tableWidget_all_register.setItem(index_row, index_column, item)

    def __convert_svg_to_pixmap(self, svg_str: str) -> QPixmap:
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(svg_str.encode()))
        return pixmap

    def set_socket(self, socket_obj: SocketCore) -> typing.Self:
        self.__socket_obj: SocketCore = socket_obj
    # # 将真正的 UI 更新操作推到主线程中执行
    # QTimer.singleShot(0, lambda: self.update_ui(msg))
        self.__socket_obj.signal_connection_status.connect(self.__transport_to_on_connection_changed)
        self.__socket_obj.signal_recv_json.connect(self.__transport_to_on_json_recv)
        return self

    def __send_read_request_loop(self):
        for idx, (register_address, item) in enumerate(self.__PDU_struct.get_data().items()):
            item: ModbusDataStruct
            # _log.info(register_address)
            self.send_read_request(register_address)

    def send_read_request(self, register_address: int, isSpecific: bool = False) -> typing.Self:
        # if isinstance(register_address, int):
        #     register_address = [register_address]
        modbus_id = self.sp_modbus_id.value()
        request_message: dict = {'modbus_data_read': {'modbus_id': modbus_id, 'read_request': register_address, 'isSpecific': isSpecific}}
        if not self.__socket_obj:
            # QMessageBox.information(self, 'No Socket Connection', 'Please connect to the server first')
            return self
        self.__socket_obj.send(request_message)
        _log.info(f'Sent request: {request_message}')
        return self

    def send_write_request(self, register_address: int, register_value: int) -> typing.Self:
        modbus_id = self.sp_modbus_id.value()
        request_message: dict = {'modbus_data_write': {'modbus_id': modbus_id, 'write_request': [register_address, register_value]}}
        self.__socket_obj.send(request_message)
        return self

    def __convert_to_int(self, value: str) -> int | None:
        if value.startswith('0x'):
            value = int(value, 16)
        elif value.startswith('0b'):
            value = int(value, 2)
        elif value.isdigit():
            value = int(value)
        else:
            return None
        return value

    def get_manual_register_address(self, register_address_str: str) -> int | None:
        register_address: int | None = self.__convert_to_int(register_address_str)
        if register_address is None:
            _log.warning(f'Invalid register address: {register_address}')
            QMessageBox.warning(self, 'Invalid register address',
                                f'Invalid register address: {register_address}.<br>It must be in hexadecimal, binary or decimal format<br>now is: {type(register_address_str)}')
        return register_address

    def __on_pb_read_clicked(self):
        register_address_str = self.le_register_address.text()
        register_address: int | None = self.get_manual_register_address(register_address_str)
        if register_address is None:
            return
        self.send_read_request(register_address, isSpecific=True)

    def __on_pb_write_clicked(self) -> None:
        register_address_str: str = self.le_register_address.text()
        register_address: int | None = self.get_manual_register_address(register_address_str)
        if register_address is None:
            return
        value: str = self.le_write_value.text()
        value = self.__convert_to_int(value)
        if value is None:
            _log.warning(f'Invalid value: {value}')
            QMessageBox.warning(self, 'Invalid value', f'Invalid value: {value}.<br>It must be in hexadecimal, binary or decimal format')
            return
        self.send_write_request(register_address, value)
        QMessageBox.information(self, 'Write', f'Write request for register {register_address} with value {value} sent')

    def __on_pb_connect_clicked(self):
        host = self.le_socket_id.text().strip()
        if not host:
            host: str = self.le_socket_id.placeholderText()
        if not host:
            QMessageBox.critical(self, 'No Host', 'No host specified, please enter a host')
            return
        if not self.__socket_obj:
            self.set_socket(SocketCore(host))
        if self.__socket_obj and not self.__socket_obj.isConnected:
            self.__socket_obj.disconnect()
            self.set_socket(SocketCore(host))

        if self.__socket_obj.isConnected:
            self.__socket_obj.disconnect()
        else:
            self.__socket_obj.connect()

    def __on_pb_add_clicked(self):
        register_address_str: str = self.le_add_register.text()
        register_address: int | None = self.get_manual_register_address(register_address_str)
        if register_address is None:
            return
        self.__PDU_struct.add_register_address(register_address)
        self.le_add_register.clear()

    def __on_pb_remove_clicked(self):
        item: QTableWidgetItem | None = self.tableWidget_all_register.currentItem()
        if item is None:
            # QMessageBox.warning(self, 'No item selected', 'Please select an item to remove')
            return
        register_address: int = int(item.data(Qt.UserRole))
        self.__PDU_struct.remove_value(register_address)

    def __transport_to_on_connection_changed(self, connected: bool) -> None:
        QTimer.singleShot(0, functools.partial(self.__on_connection_changed, connected))

    def __transport_to_on_json_recv(self, recv_data: dict) -> None:
        QTimer.singleShot(0, functools.partial(self.__on_json_recv, recv_data))

    def __on_connection_changed(self, connected: bool) -> None:
        if connected:
            self.pb_connect.setText('Disconnect')
        else:
            self.pb_connect.setText('Connect')

    def __on_json_recv(self, recv_data: dict) -> None:
        for key, value in recv_data.items():
            if key not in self.__reflect_recv_dict:
                continue
            self.__reflect_recv_dict.get(key, lambda x: None)(value)

    def __handle_read_response(self, response: dict):
        """ 
        {
            modbus_id: int,
            register_address: int,
            data: int,
            isSpecific: bool
        }
        """
        modbus_id: int = response.get('modbus_id', None)
        register_address: int = response.get('register_address', None)
        data: int = response.get('data', {})
        isSpecific = response.get('isSpecific', False)
        if modbus_id is None or not data or register_address is None:
            if modbus_id is not None:
                self.__available_modbus_id.discard(modbus_id)
                self.lb_modbus_id_available.setText('not available')
            return
        modbus_id = int(modbus_id)
        register_address = int(register_address)
        self.__available_modbus_id.add(modbus_id)
        self.lb_modbus_id_available.setText('available')
        if isSpecific:
            self.tb_all_data_info.setText(f'{datetime.datetime.now().strftime("%H:%M:%S")} {modbus_id} {register_address}\n'+pprint.pformat(data))
        else:
            self.__PDU_struct.add_value(register_address, ModbusDataStruct(data))

    def __run_motor_lock(self):
        if not self.__socket_obj:
            # QMessageBox.information(self, 'No Socket Connection', 'Please connect to the server first')
            return self
        self.__socket_obj.send({'motor_run': {'doLock': True, 'runtime': self.sp_motor_time.value(), }, })

    def __run_motor_unlock(self):
        if not self.__socket_obj:
            # QMessageBox.information(self, 'No Socket Connection', 'Please connect to the server first')
            return self
        self.__socket_obj.send({'motor_run': {'doLock': False, 'runtime': self.sp_motor_time.value(), }, })

    def __on_pb_shut_down(self):
        if not self.__socket_obj:
            # QMessageBox.information(self, 'No Socket Connection', 'Please connect to the server first')
            return self
        self.__socket_obj.send({'shutdown': {'shouldShutDown': True}, })

    def closeEvent(self, a0):
        if self.__socket_obj:
            self.__socket_obj.disconnect()
        return super().closeEvent(a0)
