# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from gui.apiOS import ApiOS


(Ui, QDataviewMaster) = uic.loadUiType('gui/masterDataview.ui')


class DataviewMaster(QDataviewMaster):
    def __init__(self, parent, schema, index, type_data=1):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.ui = Ui()
        self.ui.setupUi(self)
        self.api = ApiOS()
        self.schema = schema
        self.type_data = type_data

        self.set_data(index)

    def __del__(self):
        self.ui = None

    # List Files ---------------------------------

    def set_data(self, index):
        try:
            self.ui.title.setText(self.schema["data"][index]["path"])
            self.ui.table.clear()
            self.ui.table.setColumnCount(2)
            self.ui.table.setRowCount(0)
            self.ui.table.setHorizontalHeaderLabels(["X", "Y"])

            data = []

            if self.type_data == 1:
                data = self.schema["data"][index]["input_data"]
            else:
                data = self.schema["data"][index]["output_data"]

            self.ui.table.setRowCount(len(data))

            i = 0
            for item in data:
                if self.type_data == 1:
                    self.ui.table.setItem(i, 0, QTableWidgetItem(str(item[0])))
                    self.ui.table.setItem(i, 1, QTableWidgetItem(str(item[1])))
                else:
                    self.ui.table.setItem(i, 0, QTableWidgetItem(str(item["point"][0])))
                    self.ui.table.setItem(i, 1, QTableWidgetItem(str(item["point"][1])))
                i += 1
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось отобразить данные")
