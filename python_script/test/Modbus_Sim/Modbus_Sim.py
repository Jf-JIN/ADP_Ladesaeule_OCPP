from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
from Modbus_Sim_ui import Ui_MainWindow
import sys
import os
import json

""" 
1007    EVSERegAddress.EVSE_STATUS_FAILS: 0,
1002    EVSERegAddress.VEHICLE_STATE:  int((time.time() // 10) % 5 + 1),
2002    EVSERegAddress.CURRENT_MIN: random.randint(0, 13),
1003    EVSERegAddress.CURRENT_MAX: random.choice([6, 13, 20, 32, 63, 80]),
1004    EVSERegAddress.TURN_OFF_SELFTEST_OPERATION: 0,  # 可选值： 0 (0b000, TurnOn), 1 (0b001, TurnOff), 2 (0b010, selftest), 3 (0b011, ), 4 (0b100, clear RCD), 5 (0b101, )
        }
"""

app_path = os.getcwd()
fp = os.path.join(app_path, "Modbus_Sim.json")


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.__init_parameter()
        self.__init_ui()
        self.__init_signal_connections()
        self.write()

    def __init_parameter(self):
        def rewrite_data():
            self.evse_state1007 = 0
            self.vehicle_state1002 = 1
            self.current_max = 6
            self.current_min_value = 5
            with open(fp, "w", encoding="utf-8") as f:
                temp_dict: dict = {
                    "1007": 0,
                    "1002": 1,
                    "2002": 5,
                    "1003": 6,
                }
                json.dump(temp_dict, f, indent=4, ensure_ascii=False)
        if os.path.exists(fp):
            json_dict = {}
            try:
                with open(fp, "r") as f:
                    json_dict = json.load(f)
                self.evse_state1007 = json_dict['1007']
                self.vehicle_state1002 = json_dict['1002']
                self.current_min_value = max(0, min(13, json_dict['2002']))
                self.current_max = json_dict['1003']
            except:
                rewrite_data()

        else:
            rewrite_data()

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
""")
        self.sb_currnt_min.setMaximum(13)
        self.sb_currnt_min.setMinimum(0)
        self.cb_relay_onoff.setChecked(self.evse_state1007 & (1 << 0))
        self.cb_diode.setChecked(self.evse_state1007 & (1 << 1))
        self.cb_vent.setChecked(self.evse_state1007 & (1 << 2))
        self.cb_waiting_pilot.setChecked(self.evse_state1007 & (1 << 3))
        self.cb_rcd_check.setChecked(self.evse_state1007 & (1 << 4))
        self.rb_ready.setChecked(self.vehicle_state1002 == 1)
        self.rb_ev_present.setChecked(self.vehicle_state1002 == 2)
        self.rb_charging.setChecked(self.vehicle_state1002 == 3)
        self.rb_charging_vent.setChecked(self.vehicle_state1002 == 4)
        self.rb_failure.setChecked(self.vehicle_state1002 == 5)
        self.sb_currnt_min.setValue(max(0, min(13, self.current_min_value)))
        self.rb_current_max_6.setChecked(self.current_max == 6)
        self.rb_current_max_13.setChecked(self.current_max == 13)
        self.rb_current_max_20.setChecked(self.current_max == 20)
        self.rb_current_max_32.setChecked(self.current_max == 32)
        self.rb_current_max_63.setChecked(self.current_max == 63)
        self.rb_current_max_80.setChecked(self.current_max == 80)

    def __init_signal_connections(self) -> None:
        self.cb_relay_onoff.stateChanged.connect(self.relay_onoff)
        self.cb_diode.stateChanged.connect(self.diode)
        self.cb_vent.stateChanged.connect(self.vent)
        self.cb_waiting_pilot.stateChanged.connect(self.waiting_pilot)
        self.cb_rcd_check.stateChanged.connect(self.rcd_check)
        self.rb_ready.clicked.connect(self.ready)
        self.rb_ev_present.clicked.connect(self.ev_present)
        self.rb_charging.clicked.connect(self.charging)
        self.rb_charging_vent.clicked.connect(self.charging_vent)
        self.rb_failure.clicked.connect(self.failure)
        self.sb_currnt_min.valueChanged.connect(self.current_min)
        self.rb_current_max_6.clicked.connect(self.current_max_6)
        self.rb_current_max_13.clicked.connect(self.current_max_13)
        self.rb_current_max_20.clicked.connect(self.current_max_20)
        self.rb_current_max_32.clicked.connect(self.current_max_32)
        self.rb_current_max_63.clicked.connect(self.current_max_63)
        self.rb_current_max_80.clicked.connect(self.current_max_80)

    def write(self):
        with open(fp, 'w', encoding='utf-8') as f:
            temp_dict: dict = {
                "1007": self.evse_state1007,
                "1002": self.vehicle_state1002,
                "2002": self.current_min_value,
                "1003": self.current_max,
            }
            json.dump(temp_dict, f, indent=4, ensure_ascii=False)

    def relay_onoff(self) -> None:
        if self.cb_relay_onoff.isChecked():
            self.evse_state1007 |= 1
        else:
            self.evse_state1007 &= ~1
        self.write()

    def diode(self) -> None:
        if self.cb_diode.isChecked():
            self.evse_state1007 |= 1 << 1
        else:
            self.evse_state1007 &= ~(1 << 1)
        self.write()

    def vent(self) -> None:
        if self.cb_vent.isChecked():
            self.evse_state1007 |= 1 << 2
        else:
            self.evse_state1007 &= ~(1 << 2)
        self.write()

    def waiting_pilot(self) -> None:
        if self.cb_waiting_pilot.isChecked():
            self.evse_state1007 |= 1 << 3
        else:
            self.evse_state1007 &= ~(1 << 3)
        self.write()

    def rcd_check(self) -> None:
        if self.cb_rcd_check.isChecked():
            self.evse_state1007 |= 1 << 4
        else:
            self.evse_state1007 &= ~(1 << 4)
        print(self.evse_state1007)
        self.write()

    def ready(self) -> None:
        self.vehicle_state1002 = 1
        self.write()

    def ev_present(self) -> None:
        self.vehicle_state1002 = 2
        self.write()

    def charging(self) -> None:
        self.vehicle_state1002 = 3
        self.write()

    def charging_vent(self) -> None:
        self.vehicle_state1002 = 4
        self.write()

    def failure(self) -> None:
        self.vehicle_state1002 = 5
        self.write()

    def current_min(self) -> None:
        self.current_min_value = self.sb_currnt_min.value()
        self.write()

    def current_max_6(self) -> None:
        self.current_max = 6
        self.write()

    def current_max_13(self) -> None:
        self.current_max = 13
        self.write()

    def current_max_20(self) -> None:
        self.current_max = 20
        self.write()

    def current_max_32(self) -> None:
        self.current_max = 32
        self.write()

    def current_max_63(self) -> None:
        self.current_max = 63
        self.write()

    def current_max_80(self) -> None:
        self.current_max = 80
        self.write()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
