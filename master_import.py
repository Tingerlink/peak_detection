# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from gui.apiOS import ApiOS

import csv


(Ui, QImportMaster) = uic.loadUiType('gui/masterImport.ui')


class ImportDataMaster(QImportMaster):
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

    # List Files ----------------------------

    def set_list_files(self):
        """
        Установка списка файлов с контейнер списка файлов
        :return:
        """
        try:
            data_sources = [("[%s] %s" % (item["code"], item["path"])) for item in self.schema["data"]]
            self.ui.list_files.clear()
            self.ui.list_files.addItems(data_sources)
        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось отобразить список файлов")

    def add_list_items(self, items):
        """
        Добавление списка файлов в контейнер импортиркемых файлов
        :param items: Список файлов
        :return:
        """
        try:
            for item in items:
                try:
                    self.schema["data"].append({
                        "code": self.schema["index"],
                        "path": item,
                        "input_data": sorted(self.read_file(item), key=lambda x: x[0]),
                        "output_data": []
                    })
                    self.schema["index"] += 1
                except Exception as err:
                    self.api.send_system_message(u"Ошибка при импорте",
                                                 u"Файл '%s' содержит неверный формат данных, и не был импортирован" % item)

            self.set_list_files()
        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось добавить новые файлы")

    def select_current_file(self, index):
        """
        Событиее выбора файла из списка, для предпросмотра данных файла
        :param index: Номер файла в списке
        :return:
        """
        try:
            self.ui.table_preview.clear()
            self.ui.table_preview.setRowCount(0)
            self.ui.table_preview.setHorizontalHeaderLabels(["X", "Y"])

            if type(index) != int:
                index = self.ui.list_files.currentRow()

            if index < 0:
                return

            self.ui.table_preview.setRowCount(len(self.schema["data"][index]["input_data"]))

            i = 0
            for item in self.schema["data"][index]["input_data"]:
                self.ui.table_preview.setItem(i, 0, QTableWidgetItem(str(item[0])))
                self.ui.table_preview.setItem(i, 1, QTableWidgetItem(str(item[1])))
                i += 1
        except Exception as err:
            self.api.send_system_message("Ошибка", "Не удалось отобразить данные")

    def delete_all_files(self):
        """
        Удаление всех файлов из списка импортируемых файлов
        :return:
        """
        try:
            result = self.api.show_variants(u"Удалить все файлы?")

            if result == QMessageBox.Yes:
                self.schema["data"] = []
                self.set_list_files()
        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось удалить все файлы")

    def delete_current_file(self):
        """
        Удаление выбранного файла
        :return:
        """
        try:
            current_index = self.ui.list_files.currentRow()
            if current_index > -1:
                result = self.api.show_variants_to_delete_node()
                if result == QMessageBox.Yes:
                    self.schema["data"].pop(current_index)
                    self.set_list_files()
            else:
                self.api.send_system_message("Предупреждение", "Файл не выбран")
        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось удалить выбранный файл")

    # Import data ---------------------------

    def add_file_dialog(self):
        try:
            paths = self.api.show_open_data_dialog(self)
            if paths and len(paths[0]) > 0:
                paths = set(paths[0])

                exist_files = [x["path"] for x in self.schema["data"]]
                exist_files = set(exist_files)

                paths.difference_update(exist_files)
                self.add_list_items(paths)

                return paths

        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось загрузить файлы")
        return []

    def check_files(self):
        try:
            self.parent.schema = self.schema
            self.parent.set_list_files(self.parent.ui.list_files)
            self.parent.set_list_files(self.parent.ui.output_files, type_files="output")
            self.parent.reset_chart()

            self.api.send_system_message(u"Импорт", u"Данные успешно зафиксированны")

        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось зафиксировать данные")

    def read_file(self, path):
        array = []

        try:
            with open(path, 'r') as fp:
                reader = csv.reader(fp, delimiter=',', quotechar='"')
                for row in reader:
                    array.append([float(cell) for cell in row])
        except Exception as err:
            self.api.send_system_message("Ошибка", "Неудалось прочитать данные из файла '%s',"
                                                   "данные могли иметь не вервый формат" % path)

        return array
