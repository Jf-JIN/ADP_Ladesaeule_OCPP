
from __future__ import annotations

from PyQt5.QtCore import Qt, QObject, QEvent, pyqtSignal
from PyQt5.QtWidgets import QLabel

if 0:
    from Modbus_Shelly_Simulator import Simulator


class LabelRightDoubleFilter(QObject):
    signal_textbrowser_LDFilter = pyqtSignal(str)

    def __init__(self, parent: Simulator, label: QLabel, func):
        super().__init__(label)
        # self.__parent: PyToExeUI = parent # 用于检查, 记得运行时注释掉!
        self.__parent = parent
        self.__label = label
        self.__func = func

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick and obj is not None:
            if event.button() == Qt.RightButton:
                self.__func()
        return super().eventFilter(obj, event)
