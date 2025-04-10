
from system.UI.EVSE_Test_UI_ui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EVSETestUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__init_parameters()
        self.__init_ui()
        self.__init_signal_connections()
        self.show()

    def __init_parameters(self):
        ...

    def __init_ui(self):
        self.setWindowTitle("EVSE Test")
        self.setFixedSize(800, 600)

    def __init_signal_connections(self):
        ...

    def updata_tableWidget(self, data):
        ...
