from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSpinBox
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QIcon
from Modbus_Shelly_Simulator_ui import Ui_MainWindow
import sys
import os
import json

from Event_Filter import LabelRightDoubleFilter
from Shelly_Simulator import ShellySimulator_Thread
from Reader import *


"""
to write
1007    EVSERegAddress.EVSE_STATUS_FAILS: 0,
1002    EVSERegAddress.VEHICLE_STATE:  int((time.time() // 10) % 5 + 1),
2002    EVSERegAddress.CURRENT_MIN: random.randint(0, 13),
1003    EVSERegAddress.CURRENT_MAX: random.choice([6, 13, 20, 32, 63, 80]),

to read
1004    EVSERegAddress.TURN_OFF_SELFTEST_OPERATION: 0,  # 可选值： 0 (0b000, TurnOn), 1 (0b001, TurnOff), 2 (0b010, selftest), 3 (0b011, ), 4 (0b100, clear RCD), 5 (0b101, )
        }
1000    EVSERegAddress.CONFIGURED_AMPS
2005    EVSERegAddress.CHARGE_OPERATION
        0  1 << 0: Enable button for current change(1)      EnblBtnChrg 允钮改流
        2  1 << 1: Stop charging when button pressed(0)     StopChrgPrs 按钮停充
        4  1 << 2: Pilot ready state LED(0)                 PilotRdLED  引绪示灯
        8  1 << 3: enable charging on vehicle status D(1)   EnblChrgD   D态允充
        16 1 << 4: enable RCD feedback on MCLR pin(0)       EnblRCDMCLR 允RCD反馈
        32 1 << 5: auto clear RCD error(0)                  AutoClrRCD  自RCD清零
"""

APP_PATH = os.getcwd()
JSON_FILE_PATH = os.path.join(APP_PATH, 'Modbus_Shelly_Simulator.json')
ICON_SVG = """<svg t="1738041248852" class="icon" viewBox="0 0 1024 1024" version="1.1" p-id="4191" width="200" height="200" id="svg1" sodipodi:docname="Modbus_Shelly_Simulator.svg" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)" inkscape:export-filename="Modbus_Shelly_Simulator.png" inkscape:export-xdpi="96" inkscape:export-ydpi="96" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><defs id="defs1"><linearGradient id="linearGradient5" inkscape:collect="always"><stop style="stop-color:#fe6244;stop-opacity:1;" offset="0" id="stop5" /><stop style="stop-color:#feb532;stop-opacity:1;" offset="0.22555411" id="stop8" /><stop style="stop-color:#fe0000;stop-opacity:1;" offset="0.36114731" id="stop9" /><stop style="stop-color:#f0b900;stop-opacity:1;" offset="0.56975228" id="stop10" /><stop style="stop-color:#fe6244;stop-opacity:1;" offset="0.7131682" id="stop7" /><stop style="stop-color:#fe6244;stop-opacity:0;" offset="1" id="stop6" /></linearGradient><linearGradient inkscape:collect="always" xlink:href="#linearGradient5" id="linearGradient6" x1="87.681421" y1="449.15844" x2="941.6146" y2="449.15844" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0.90866618,0,0,1.011345,47.004769,168.9843)" /></defs><sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:zoom="2.8743891" inkscape:cx="76.016153" inkscape:cy="89.584254" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="svg1" /><rect style="fill:#000000;fill-opacity:0;stroke:#4d4d4d;stroke-width:104.412;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke" id="rect1" width="902.71057" height="657.16858" x="63.05587" y="247.45821" /><path d="M 867.80935,38.151943 76.324432,281.07415 c -35.650975,10.93683 -55.70012,48.70261 -44.763288,84.3536 a 67.557519,67.557519 0 0 0 28.207709,37.11266 L 293.60984,551.83084 c 24.96294,15.93358 57.38988,13.79804 80.05142,-5.287 L 665.51413,300.73971 c 7.02862,-6.11634 17.69592,-5.3803 23.81226,1.65867 5.51506,6.34441 5.52542,15.77807 0.0207,22.13284 L 443.07648,616.11456 c -19.10576,22.58898 -21.2413,54.99519 -5.28699,79.9063 L 587.26651,929.5301 c 20.17355,31.46286 62.02379,40.61666 93.48663,20.44317 a 67.659113,67.659113 0 0 0 28.11442,-36.95725 l 243.66861,-790.469 c 10.95757,-35.671712 -9.0915,-73.478971 -44.7633,-84.426172 a 67.513978,67.513978 0 0 0 -39.73545,0.02074 h -0.22807 z" fill="#00c657" p-id="4192" id="path1" style="stroke-width:1.03667" /><path style="fill:#000000;fill-opacity:0;stroke:url(#linearGradient6);stroke-width:98.1639;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:0;stroke-dasharray:none;paint-order:fill markers stroke" d="M 159.79643,697.67685 H 293.1864 l 70.11525,-263.23534 85.50643,377.59167 44.46331,-120.8293 34.20257,49.62631 73.53548,-189.87466 47.88359,107.88333 64.98488,10.78833 53.01396,21.57669 h 102.60772 v 0" id="path2" /></svg>"""


class Simulator(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(1000, 800)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.__init_parameter()
        self.__init_ui()
        self.__init_signal_connections()
        self.write()
        self.reader.start()
        self.shelly.start()

    def __init_parameter(self):
        self.isFileNeededToReset = False
        self.json_ori_data = {}
        self.copy_board = QApplication.clipboard()
        self.__isCurrentValueChanged = False
        self.__isMaxVoltageChanged = False
        self.check_json_file()
        self.__init_threads()

    def __init_threads(self):
        self.reader = ReaderThread(JSON_FILE_PATH)
        self.shelly = ShellySimulator_Thread()
        self.shelly.set_current_max_value(self.current_max_1003)
        self.shelly.set_current_min_value(self.current_min_2002)

    def __init_ui(self):
        self.setStyleSheet(""" \
QWidget {
    font: 20px 'Arial';
}
QWidget#centralwidget {
    background-color: #81BFDA;
}
QSpinBox {
    background-color: #A7D477;
}
QSpinBox#sb_set_current, #sb_set_max_voltage{
    background-color: transparent;
    border: none;
}
QLabel {
    padding: 0px 5px;
    background-color: transparent;
    border-radius:10px;
}
""")
        self.setWindowIcon(QIcon(self.pixmap_from_svg(ICON_SVG)))
        self.setWindowTitle('Modbus / Shelly Simulator')
        self.lb_ip_local.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.lb_ip_remote.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        lb_default_listener = LabelRightDoubleFilter(self, self.lb_default, self.write_default_update_display)
        lb_set_vaild_listener = LabelRightDoubleFilter(self, self.lb_set_invaild, self.shelly.set_inVaild)
        lb_clear_listener = LabelRightDoubleFilter(self, self.lb_clear, self.shelly.clear)
        lb_set_turnonoff_listener = LabelRightDoubleFilter(self, self.lb_turnonoff, self.set_turn_onoff_1004)
        lb_set_selftest_listener = LabelRightDoubleFilter(self, self.lb_selftest, self.set_selftest_1004)
        lb_clear_RCD_listener = LabelRightDoubleFilter(self, self.lb_clearRCD, self.set_clear_RCD_1004)
        lb_2005_0_listener = LabelRightDoubleFilter(self, self.lb_2005_0, self.set_2005_0)
        lb_2005_1_listener = LabelRightDoubleFilter(self, self.lb_2005_1, self.set_2005_1)
        lb_2005_2_listener = LabelRightDoubleFilter(self, self.lb_2005_2, self.set_2005_2)
        lb_2005_3_listener = LabelRightDoubleFilter(self, self.lb_2005_3, self.set_2005_3)
        lb_2005_4_listener = LabelRightDoubleFilter(self, self.lb_2005_4, self.set_2005_4)
        lb_2005_5_listener = LabelRightDoubleFilter(self, self.lb_2005_5, self.set_2005_5)
        self.lb_default.installEventFilter(lb_default_listener)
        self.lb_set_invaild.installEventFilter(lb_set_vaild_listener)
        self.lb_clear.installEventFilter(lb_clear_listener)
        self.lb_turnonoff.installEventFilter(lb_set_turnonoff_listener)
        self.lb_selftest.installEventFilter(lb_set_selftest_listener)
        self.lb_clearRCD.installEventFilter(lb_clear_RCD_listener)
        self.lb_2005_0.installEventFilter(lb_2005_0_listener)
        self.lb_2005_1.installEventFilter(lb_2005_1_listener)
        self.lb_2005_2.installEventFilter(lb_2005_2_listener)
        self.lb_2005_3.installEventFilter(lb_2005_3_listener)
        self.lb_2005_4.installEventFilter(lb_2005_4_listener)
        self.lb_2005_5.installEventFilter(lb_2005_5_listener)
        self.sb_set_current.setButtonSymbols(QSpinBox.NoButtons)
        self.sb_set_current.wheelEvent = lambda event: None
        self.sb_set_current.setMinimum(self.current_min_2002)
        self.sb_set_current.setMaximum(self.current_max_1003)
        self.sb_currnt_min.setMinimum(0)
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_max_voltage.setMinimum(0)
        self.sb_set_max_voltage.setMaximum(2147483647)
        self.sb_set_max_voltage.setButtonSymbols(QSpinBox.NoButtons)
        self.sb_set_max_voltage.wheelEvent = lambda event: None
        self.update_display()

    def __init_signal_connections(self) -> None:
        self.cb_relay_onoff.stateChanged.connect(self.relay_onoff)
        self.cb_diode.stateChanged.connect(self.diode)
        self.cb_vent.stateChanged.connect(self.vent)
        self.cb_waiting_pilot.stateChanged.connect(self.waiting_pilot)
        self.cb_rcd_check.stateChanged.connect(self.rcd_check)
        self.rb_ready.clicked.connect(self.evse_ready)
        self.rb_ev_present.clicked.connect(self.ev_present)
        self.rb_charging.clicked.connect(self.charging)
        self.rb_charging_vent.clicked.connect(self.charging_vent)
        self.rb_failure.clicked.connect(self.failure)
        self.sb_currnt_min.valueChanged.connect(self.current_min)
        self.sb_set_current.editingFinished.connect(self.set_current)
        self.sb_set_max_voltage.editingFinished.connect(self.set_max_voltage)
        self.rb_current_max_6.clicked.connect(self.current_max_6)
        self.rb_current_max_13.clicked.connect(self.current_max_13)
        self.rb_current_max_20.clicked.connect(self.current_max_20)
        self.rb_current_max_32.clicked.connect(self.current_max_32)
        self.rb_current_max_63.clicked.connect(self.current_max_63)
        self.rb_current_max_80.clicked.connect(self.current_max_80)
        self.pb_copy_local.clicked.connect(self.copy_ip_address)
        self.pb_copy_remote.clicked.connect(self.copy_ip_address)
        self.reader.signal_reader.connect(self.handle_reader_signal)
        self.reader.signal_reader.connect(self.shelly.handle_thread_data)
        self.shelly.signal_ip_address.connect(self.handle_shelly_ip_signal)
        self.shelly.signal_ph0.connect(self.handle_ph0_signal)
        self.shelly.signal_ph1.connect(self.handle_ph1_signal)
        self.shelly.signal_ph2.connect(self.handle_ph2_signal)
        self.shelly.signal_start.connect(self.handle_shelly_start_signal)

    def pixmap_from_svg(self, icon_code: str) -> QIcon:
        '''
        svg转pixmap

        参数:
            Icon_code: SVG 的源码(str)
        '''
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return pixmap

    def write(self):
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            temp_dict: dict = {
                '1007': self.evse_state_1007,
                '1002': self.vehicle_state_1002,
                '2002': self.current_min_2002,
                '1003': self.current_max_1003,
                '1004': self.onoff_selftest_1004,
                '1000': self.configured_amps_1000,
                '2005': self.charge_operation_2005,
                'latch_lock_pin': self.latch_lock_pin,
                'latch_unlock_pin': self.latch_unlock_pin,
                'max_voltage': self.max_voltage,
            }
            json.dump(temp_dict, f, indent=4, ensure_ascii=False)

    def write_default_file(self):
        self.evse_state_1007 = 0
        self.vehicle_state_1002 = 1
        self.current_max_1003 = 6
        self.current_min_2002 = 5
        self.onoff_selftest_1004 = 0
        self.configured_amps_1000 = 0
        self.charge_operation_2005 = 0b001001
        self.latch_lock_pin = ''
        self.latch_unlock_pin = ''
        self.max_voltage = 230
        self.__isCurrentValueChanged = True
        self.__isMaxVoltageChanged = True
        self.write()

    def check_json_file(self):
        if os.path.exists(JSON_FILE_PATH):
            json_dict = {}
            try:
                with open(JSON_FILE_PATH, 'r') as f:
                    json_dict: dict = json.load(f)
                self.evse_state_1007 = json_dict.get('1007', 0)
                self.vehicle_state_1002 = json_dict.get('1002', 1)
                self.current_min_2002 = max(0, min(13, json_dict.get('2002', 0)))
                self.current_max_1003 = json_dict.get('1003', 0)
                self.onoff_selftest_1004 = json_dict.get('1004', None)
                self.configured_amps_1000 = json_dict.get('1000', None)
                self.charge_operation_2005 = json_dict.get('2005', None)
                self.latch_lock_pin = json_dict.get('latch_lock_pin', None)
                self.latch_unlock_pin = json_dict.get('latch_unlock_pin', None)
                self.max_voltage = json_dict.get('max_voltage', 230)
                self.current_max_1003 = max(0, min(80, self.current_max_1003))
                self.current_min_2002 = max(0, min(13, self.current_min_2002))
                self.configured_amps_1000 = min(max(self.current_min_2002, self.configured_amps_1000), self.current_max_1003)
                self.__isCurrentValueChanged = True
                self.__isMaxVoltageChanged = True
            except:
                self.isFileNeededToReset = True
        else:
            self.isFileNeededToReset = True
        if self.isFileNeededToReset:
            self.write_default_file()

    def update_display(self):
        self.cb_relay_onoff.setChecked(self.evse_state_1007 & (1 << 0))
        self.cb_diode.setChecked(self.evse_state_1007 & (1 << 1))
        self.cb_vent.setChecked(self.evse_state_1007 & (1 << 2))
        self.cb_waiting_pilot.setChecked(self.evse_state_1007 & (1 << 3))
        self.cb_rcd_check.setChecked(self.evse_state_1007 & (1 << 4))
        self.rb_ready.setChecked(self.vehicle_state_1002 == 1)
        self.rb_ev_present.setChecked(self.vehicle_state_1002 == 2)
        self.rb_charging.setChecked(self.vehicle_state_1002 == 3)
        self.rb_charging_vent.setChecked(self.vehicle_state_1002 == 4)
        self.rb_failure.setChecked(self.vehicle_state_1002 == 5)
        self.sb_currnt_min.setValue(self.current_min_2002)
        self.rb_current_max_6.setChecked(self.current_max_1003 == 6)
        self.rb_current_max_13.setChecked(self.current_max_1003 == 13)
        self.rb_current_max_20.setChecked(self.current_max_1003 == 20)
        self.rb_current_max_32.setChecked(self.current_max_1003 == 32)
        self.rb_current_max_63.setChecked(self.current_max_1003 == 63)
        self.rb_current_max_80.setChecked(self.current_max_1003 == 80)
        self.update_display_read()

    def update_display_read(self):
        def set_read_text(label: QLabel, value, flag_isValue=False):
            if value is None:
                text = 'UnDef'
            elif isinstance(value, str):
                text = 'Error'
            else:
                if flag_isValue:
                    text = bin(value)
                else:
                    text = str(value)
            label.setText(text)

        set_read_text(self.lb_configured_amps_value, self.configured_amps_1000, True)
        set_read_text(self.lb_onoff_selftest_value, self.onoff_selftest_1004, True)
        set_read_text(self.lb_charge_operation_value, self.charge_operation_2005, True)

        self.lb_latch_lock_pin_value.setText(self.latch_lock_pin if self.latch_lock_pin is not None else 'UnDef')
        self.lb_latch_unlock_pin_value.setText(self.latch_unlock_pin if self.latch_lock_pin is not None else 'UnDef')
        if self.__isCurrentValueChanged:
            self.sb_set_current.setValue(max(self.current_min_2002, min(self.configured_amps_1000, self.current_max_1003)))
            self.__isCurrentValueChanged = False
        if self.__isMaxVoltageChanged:
            self.sb_set_max_voltage.setValue(self.max_voltage)
            self.__isMaxVoltageChanged = False

        self.lb_turnonoff.setStyleSheet('background-color: #F93827') if not self.onoff_selftest_1004 & (1 << 0) else self.lb_turnonoff.setStyleSheet('background-color: #73EC8B')
        self.lb_selftest.setStyleSheet('background-color: #F93827') if self.onoff_selftest_1004 & 1 << 1 else self.lb_selftest.setStyleSheet('background-color: #73EC8B')
        self.lb_clearRCD.setStyleSheet('background-color: #F93827') if self.onoff_selftest_1004 & 1 << 2 else self.lb_clearRCD.setStyleSheet('background-color: #73EC8B')
        self.lb_2005_0.setStyleSheet('background-color: #F93827') if self.charge_operation_2005 & 1 << 0 else self.lb_2005_0.setStyleSheet('background-color: #73EC8B')
        self.lb_2005_1.setStyleSheet('background-color: #F93827') if self.charge_operation_2005 & 1 << 1 else self.lb_2005_1.setStyleSheet('background-color: #73EC8B')
        self.lb_2005_2.setStyleSheet('background-color: #F93827') if self.charge_operation_2005 & 1 << 2 else self.lb_2005_2.setStyleSheet('background-color: #73EC8B')
        self.lb_2005_3.setStyleSheet('background-color: #F93827') if self.charge_operation_2005 & 1 << 3 else self.lb_2005_3.setStyleSheet('background-color: #73EC8B')
        self.lb_2005_4.setStyleSheet('background-color: #F93827') if self.charge_operation_2005 & 1 << 4 else self.lb_2005_4.setStyleSheet('background-color: #73EC8B')
        self.lb_2005_5.setStyleSheet('background-color: #F93827') if self.charge_operation_2005 & 1 << 5 else self.lb_2005_5.setStyleSheet('background-color: #73EC8B')

        # # 显示状态
        set_read_text(self.lb_configured_amps, self.configured_amps_1000)
        # self.lb_onoff_selftest_value
        # self.lb_charge_operation_value
        if self.latch_lock_pin == 0 and self.latch_unlock_pin == 1:
            self.lb_latch_lock_pin.setText('Off')
            self.lb_latch_unlock_pin.setText('Off')
        elif self.latch_lock_pin == 1 and self.latch_unlock_pin == 0:
            self.lb_latch_lock_pin.setText('On')
            self.lb_latch_unlock_pin.setText('On')
        elif (self.latch_lock_pin == 1 and self.latch_unlock_pin == 1) or (self.latch_lock_pin == 0 and self.latch_unlock_pin == 0):
            self.lb_latch_lock_pin.setText('Stop')
            self.lb_latch_unlock_pin.setText('Stop')
        else:
            self.lb_latch_lock_pin.clear()
            self.lb_latch_unlock_pin.clear()

    def handle_shelly_ip_signal(self, ip_list: list):
        self.lb_ip_local.setText(ip_list[0])
        self.lb_ip_remote.setText(ip_list[1])

    def handle_reader_signal(self, data: dict):
        if data['1000'] != self.configured_amps_1000:
            self.__isCurrentValueChanged = True
        if data['max_voltage'] != self.max_voltage:
            self.__isMaxVoltageChanged = True
        self.configured_amps_1000 = data['1000']
        self.onoff_selftest_1004 = data['1004']
        self.charge_operation_2005 = data['2005']
        self.update_display_read()

    def handle_ph0_signal(self, data_dict: dict):
        self.lb_current_ph0.setText('{:.2f}'.format(data_dict['current']))
        self.lb_pf_ph0.setText('{:.2f}'.format(data_dict['pf'])) if isinstance(data_dict['pf'], float) else self.lb_pf_ph0.clear()
        self.lb_power_ph0.setText('{:.4f}'.format(data_dict['power']/1000))
        self.lb_voltage_ph0.setText('{:.2f}'.format(data_dict['voltage']))
        self.lb_total_ph0.setText('{:.2f}'.format(data_dict['total']))
        self.lb_isValid_ph0.setText(str(data_dict['is_valid']))

    def handle_ph1_signal(self, data_dict: dict):
        self.lb_current_ph1.setText('{:.2f}'.format(data_dict['current']))
        self.lb_pf_ph1.setText('{:.2f}'.format(data_dict['pf'])) if isinstance(data_dict['pf'], float) else self.lb_pf_ph1.clear()
        self.lb_power_ph1.setText('{:.4f}'.format(data_dict['power']/1000))
        self.lb_voltage_ph1.setText('{:.2f}'.format(data_dict['voltage']))
        self.lb_total_ph1.setText('{:.2f}'.format(data_dict['total']))
        self.lb_isValid_ph1.setText(str(data_dict['is_valid']))

    def handle_ph2_signal(self, data_dict: dict):
        self.lb_current_ph2.setText('{:.2f}'.format(data_dict['current']))
        self.lb_pf_ph2.setText('{:.2f}'.format(data_dict['pf'])) if isinstance(data_dict['pf'], float) else self.lb_pf_ph2.clear()
        self.lb_power_ph2.setText('{:.4f}'.format(data_dict['power']/1000))
        self.lb_voltage_ph2.setText('{:.2f}'.format(data_dict['voltage']))
        self.lb_total_ph2.setText('{:.2f}'.format(data_dict['total']))
        self.lb_isValid_ph2.setText(str(data_dict['is_valid']))

    def handle_shelly_start_signal(self, flag):
        if flag:
            if self.vehicle_state_1002 == 2:
                self.vehicle_state_1002 = 3
            elif self.vehicle_state_1002 == 4:
                return
            self.write_update_display()
        else:
            if 2 < self.vehicle_state_1002 < 5:
                self.vehicle_state_1002 = 2
                self.write_update_display()

    def copy_ip_address(self) -> None:
        sender = self.sender()
        if sender == self.pb_copy_local:
            self.copy_board.setText(self.lb_ip_local.text())
        elif sender == self.pb_copy_remote:
            self.copy_board.setText(self.lb_ip_remote.text())

    def write_update_display(self) -> None:
        self.write()
        self.update_display()

    def write_default_update_display(self) -> None:
        self.write_default_file()
        self.update_display()

    def set_current(self) -> None:
        current = self.sb_set_current.value()
        current = max(self.current_min_2002, min(current, self.current_max_1003))
        self.configured_amps_1000 = current
        self.write()

    def set_max_voltage(self) -> None:
        voltage = self.sb_set_max_voltage.value()
        self.max_voltage = voltage
        self.write()

    def relay_onoff(self) -> None:
        if self.cb_relay_onoff.isChecked():
            self.evse_state_1007 |= 1
        else:
            self.evse_state_1007 &= ~1
        self.write()

    def diode(self) -> None:
        if self.cb_diode.isChecked():
            self.evse_state_1007 |= 1 << 1
        else:
            self.evse_state_1007 &= ~(1 << 1)
        self.write()

    def vent(self) -> None:
        if self.cb_vent.isChecked():
            self.evse_state_1007 |= 1 << 2
        else:
            self.evse_state_1007 &= ~(1 << 2)
        self.write()

    def waiting_pilot(self) -> None:
        if self.cb_waiting_pilot.isChecked():
            self.evse_state_1007 |= 1 << 3
        else:
            self.evse_state_1007 &= ~(1 << 3)
        self.write()

    def rcd_check(self) -> None:
        if self.cb_rcd_check.isChecked():
            self.evse_state_1007 |= 1 << 4
        else:
            self.evse_state_1007 &= ~(1 << 4)
        self.write()

    def evse_ready(self) -> None:
        self.vehicle_state_1002 = 1
        self.write()

    def ev_present(self) -> None:
        self.vehicle_state_1002 = 2
        self.write()

    def charging(self) -> None:
        self.vehicle_state_1002 = 3
        self.write()

    def charging_vent(self) -> None:
        self.vehicle_state_1002 = 4
        self.write()

    def failure(self) -> None:
        self.vehicle_state_1002 = 5
        self.write()

    def current_min(self) -> None:
        self.current_min_2002 = self.sb_currnt_min.value()
        self.sb_set_current.setMinimum(self.current_min_2002)
        lim = max(self.configured_amps_1000, self.current_min_2002)
        if self.configured_amps_1000 != lim:
            self.configured_amps_1000 = lim
            self.__isCurrentValueChanged = True
        self.write()

    def current_max_6(self) -> None:
        self.current_max_1003 = 6
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_current.setMaximum(self.current_max_1003)
        lim = min(self.configured_amps_1000, self.current_max_1003)
        if self.configured_amps_1000 != lim:
            self.configured_amps_1000 = lim
            self.__isCurrentValueChanged = True
        self.write()

    def current_max_13(self) -> None:
        self.current_max_1003 = 13
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_current.setMaximum(self.current_max_1003)
        lim = min(self.configured_amps_1000, self.current_max_1003)
        if self.configured_amps_1000 != lim:
            self.configured_amps_1000 = lim
            self.__isCurrentValueChanged = True
        self.write()

    def current_max_20(self) -> None:
        self.current_max_1003 = 20
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_current.setMaximum(self.current_max_1003)
        lim = min(self.configured_amps_1000, self.current_max_1003)
        if self.configured_amps_1000 != lim:
            self.configured_amps_1000 = lim
            self.__isCurrentValueChanged = True
        self.write()

    def current_max_32(self) -> None:
        self.current_max_1003 = 32
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_current.setMaximum(self.current_max_1003)
        lim = min(self.configured_amps_1000, self.current_max_1003)
        if self.configured_amps_1000 != lim:
            self.configured_amps_1000 = lim
            self.__isCurrentValueChanged = True
        self.write()

    def current_max_63(self) -> None:
        self.current_max_1003 = 63
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_current.setMaximum(self.current_max_1003)
        lim = min(self.configured_amps_1000, self.current_max_1003)
        if self.configured_amps_1000 != lim:
            self.configured_amps_1000 = lim
            self.__isCurrentValueChanged = True
        self.write()

    def current_max_80(self) -> None:
        self.current_max_1003 = 80
        self.sb_currnt_min.setMaximum(self.current_max_1003)
        self.sb_set_current.setMaximum(self.current_max_1003)
        self.write()

    def set_turn_onoff_1004(self):
        if self.onoff_selftest_1004 & 1 << 0:
            self.onoff_selftest_1004 &= ~(1 << 0)
        else:
            self.onoff_selftest_1004 |= 1 << 0
        self.write_update_display()

    def set_selftest_1004(self):
        if self.onoff_selftest_1004 & 1 << 1:
            self.onoff_selftest_1004 &= ~(1 << 1)
        else:
            self.onoff_selftest_1004 |= 1 << 1
        self.write_update_display()

    def set_clear_RCD_1004(self):
        if self.onoff_selftest_1004 & 1 << 2:
            self.onoff_selftest_1004 &= ~(1 << 2)
        else:
            self.onoff_selftest_1004 |= 1 << 2
        self.write_update_display()

    def set_2005_0(self):
        if self.charge_operation_2005 & 1 << 0:
            self.charge_operation_2005 &= ~(1 << 0)
        else:
            self.charge_operation_2005 |= (1 << 0)
        self.write_update_display()

    def set_2005_1(self):
        if self.charge_operation_2005 & 1 << 1:
            self.charge_operation_2005 &= ~(1 << 1)
        else:
            self.charge_operation_2005 |= (1 << 1)
        self.write_update_display()

    def set_2005_2(self):
        if self.charge_operation_2005 & 1 << 2:
            self.charge_operation_2005 &= ~(1 << 2)
        else:
            self.charge_operation_2005 |= (1 << 2)
        self.write_update_display()

    def set_2005_3(self):
        if self.charge_operation_2005 & 1 << 3:
            self.charge_operation_2005 &= ~(1 << 3)
        else:
            self.charge_operation_2005 |= (1 << 3)
        self.write_update_display()

    def set_2005_4(self):
        if self.charge_operation_2005 & 1 << 4:
            self.charge_operation_2005 &= ~(1 << 4)
        else:
            self.charge_operation_2005 |= (1 << 4)
        self.write_update_display()

    def set_2005_5(self):
        if self.charge_operation_2005 & 1 << 5:
            self.charge_operation_2005 &= ~(1 << 5)
        else:
            self.charge_operation_2005 |= (1 << 5)
        self.write_update_display()

    def closeEvent(self, a0):
        self.shelly.stop()
        return super().closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = Simulator()
    mainWin.show()
    sys.exit(app.exec_())
