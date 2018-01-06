# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from gui.apiOS import ApiOS

import plot_creater

(Ui, QVisualizationMaster) = uic.loadUiType('gui/masterVisualization.ui')


class VisualizationMaster(QVisualizationMaster):
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

    def select_file(self, index):
        try:
            if index < 0:
                return
            self.draw_graph(self.ui.input_graph, self.schema["data"][index])
            self.draw_graph(self.ui.output_graph, self.schema["data"][index], type_data="output")
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось построить графики")

    def draw_graph(self, control, data, type_data="input"):
        count = control.count()
        for i in range(0, count):
            control.removeWidget(control.widget(0))

            control.addWidget(plot_creater.create_plot(data, type_graph="one", type_data=type_data))

    def set_list_files(self):
        data_sources = [("[%s] %s" % (item["code"], item["path"])) for item in self.schema["data"]]

        self.ui.list_files.clear()
        self.ui.list_files.addItems(data_sources)
