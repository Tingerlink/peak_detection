# -*- coding: utf-8 -*-

import sys
import plot_creater
import master_export

from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from gui.apiOS import ApiOS
from master_import import ImportDataMaster
from master_visualization import VisualizationMaster
from master_conversion import ConversionMaster
from master_dataview import DataviewMaster


(Ui_MainWindow, QMainWindow) = uic.loadUiType('gui/mainWindow.ui')


class MainWindow(QMainWindow):
    schema = {
        "data": [],
        "index": 0
    }

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.api = ApiOS()

    def __del__(self):
        self.ui = None

    # List files -----------------------------

    def set_list_files(self, element, type_files="input"):
        data_sources = []

        try:
            if type_files == "input":
                data_sources = [("[%s] %s" % (item["code"], item["path"])) for item in self.schema["data"]]
            elif type_files == "output":
                for item in self.schema["data"]:
                    if item["output_data"] and (len(item["output_data"]) > 0):
                        data_sources.append("OUT [%s] %s" % (item["code"], item["path"]))

            element.clear()
            element.addItems(data_sources)
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось добавить список файлов")

    def select_file(self, index):
        """
        Событие выбора файла для предпосмотра данных
        :param index: Номер выбранного файла
        :return:
        """
        try:
            if type(index) != int:
                index = self.ui.list_files.currentRow()

            if index < 0:
                return
            self.draw_graph(self.schema["data"][index])
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось отобразить данные")

    # Masters --------------------------------

    def open_import_master(self):
        """
        Запуск мастера импорта
        :return:
        """
        try:
            modal = ImportDataMaster(parent=self, schema=self.schema)
            modal.setWindowModality(Qt.ApplicationModal)
            modal.show()
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось открыть мастер импорта")

    def open_export_master(self):
        """
        Запуск мастера экспорта
        :return:
        """
        try:
            if self.ui.output_files.count() <= 0:
                self.api.send_system_message(u"Предупреждение", u"Отсутствуют данные для экспорта")
            else:
                path = self.api.show_open_dir_dialog(self)
                if not path or (path == ""):
                    return
                master_export.push(self.schema, path)

                self.api.send_system_message(u"Экспорт", u"Данные были успешно записанны в директорию: '%s'" % path)

        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось открыть мастер экспорта")

    def open_visualization_master(self):
        """
        Запуск мастера визуализации данных
        :return:
        """
        try:
            modal = VisualizationMaster(parent=self, schema=self.schema)
            modal.setWindowModality(Qt.ApplicationModal)
            modal.show()
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось открыть мастер отображения данных")

    def open_conversion_master(self):
        """
        Запуск мастера преобразования данных
        :return:
        """
        try:
            modal = ConversionMaster(parent=self, schema=self.schema)
            modal.setWindowModality(Qt.ApplicationModal)
            modal.show()
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось открыть мастер преобразования данных")

    def open_dataview_output_master(self):
        """
        Запуск мастера просмотра выходных данных
        :return:
        """
        try:
            index = self.ui.output_files.currentRow()
            if index >= 0:
                modal = DataviewMaster(parent=self, schema=self.schema, index=index, type_data=0)
                modal.setWindowModality(Qt.ApplicationModal)
                modal.show()
            else:
                self.api.send_system_message("Предупреждение", "Необходимо выбрать файл")
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось открыть мастер просмотра выходных данных")

    def open_dataview_input_master(self):
        """
        Запуск мастера просмотра входных данных
        :return:
        """
        try:
            index = self.ui.list_files.currentRow()
            if index >= 0:
                modal = DataviewMaster(parent=self, schema=self.schema, index=index, type_data=1)
                modal.setWindowModality(Qt.ApplicationModal)
                modal.show()
            else:
                self.api.send_system_message("Предупреждение", "Необходимо выбрать файл")

        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось открыть мастер просмотра входных данных")

    # Graphic --------------------------------

    def draw_graph(self, data):
        """
        Отрисовка графика предпросмотра
        :param data: Набор точек
        :return:
        """
        self.reset_chart()

        self.ui.graph_widget.addWidget(plot_creater.create_plot(data))

    def reset_chart(self):
        """
        Очистка графика
        :return:
        """
        count = self.ui.graph_widget.count()
        for i in range(0, count):
            self.ui.graph_widget.removeWidget(self.ui.graph_widget.widget(0))


if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName("qt")

    # create widget
    w = MainWindow()
    w.show()

    # execute application
    sys.exit(app.exec_())