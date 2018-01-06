# -*- coding: utf-8 -*-
import threading

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QApplication

import peak_detection
import plot_creater
from gui.apiOS import ApiOS

import csv


(Ui, QConversionMaster) = uic.loadUiType('gui/masterConversion.ui')

class ConversionMaster(QConversionMaster):
    def __init__(self, parent, schema):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.ui = Ui()
        self.ui.setupUi(self)
        self.api = ApiOS()
        self.schema = schema
        self.set_list_files()

    def __del__(self):
        self.ui = None

    # List Files ---------------------------------

    def set_list_files(self):
        data_sources = []
        try:
            data_sources = [("[%s] %s" % (item["code"], item["path"])) for item in self.schema["data"]]

            self.ui.list_files.clear()
            self.ui.list_files.addItems(data_sources)
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось добавить список файлов")

    def run(self):
        count = len(self.schema["data"])
        beta = 0.0
        width = 0.0
        try:
            beta = float(str(self.ui.tb_beta.text()).replace(",", "."))
            width = float(str(self.ui.tb_with.text()).replace(",", "."))
        except Exception as err:
            self.api.send_system_message("Ошибка", "Неверный формат данных")
            return

        for index in range(0, count):
            threading.Thread(target=self.f, args=(index, count, beta, width)).run()

    def f(self, index, count, beta, width):
        try:
            k = (float(index) + 1.0) / float(count) * 100.0
            self.schema["data"][index]["output_data"] = \
                peak_detection.detect_peaks(self.schema["data"][index]["input_data"], beta, width)

            self.ui.progress.setValue(k)
            if k == 100:
                self.api.send_system_message("Выполнено", "Преобразование выполнено")

            self.set_list_files()
            QApplication.processEvents()
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось преобразовать данные")

    def apply(self):
        try:
            self.parent.schema = self.schema
            self.parent.set_list_files(self.parent.ui.list_files)
            self.parent.set_list_files(self.parent.ui.output_files, type_files="output")
            self.parent.reset_chart()
            self.api.send_system_message("Выполнено", "Данные сохранены")

        except:
            pass

    def select_file(self, index):
        try:
            if index < 0:
                return

            self.draw_graph(self.schema["data"][index])
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось отобразить данные")

    def draw_graph(self, data):
        """
        Отрисовка графика предпросмотра
        :param data: Набор точек
        :return:
        """
        self.reset_chart()

        self.ui.graph_widget.addWidget(plot_creater.create_plot(data, type_data="output"))

    def reset_chart(self):
        """
        Очистка графика
        :return:
        """
        count = self.ui.graph_widget.count()
        for i in range(0, count):
            self.ui.graph_widget.removeWidget(self.ui.graph_widget.widget(0))