# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ApiOS:
    FILE_EXTENDED = u'.csv'
    FILE_FORMAT_CSV = u'Comma-Separated Values [.csv] (*.csv)'

    MESSAGE_WARNING = u'Предупреждение'
    MESSAGE_ERROR = u'Ошибка'

    @staticmethod
    def get_list_format(formats):
        all_formats = ''
        for format_file in formats:
            all_formats += format_file + ';; '

        return all_formats[:-3]

    def show_open_data_dialog(self, parent_window):
        file_data_path = QFileDialog.getOpenFileNames(parent_window,
                                                      u"Импорт данных",
                                                      '',
                                                      self.get_list_format([self.FILE_FORMAT_CSV]))

        try:
            result = [x for x in file_data_path]
        except Exception as err:
            pass

        return result

    def show_open_dir_dialog(self, parent_window):
        dir_path = QFileDialog.getExistingDirectory(parent_window,
                                                    'Select a folder:',
                                                    'C:\\',
                                                    QFileDialog.ShowDirsOnly)
        return dir_path


    # Messages --------------------------

    def show_variants_to_delete_node(self):
        message_box = QMessageBox()
        message_box.setText(u'Вы действительно хотите удалить выбранный элемент?')
        message_box.setWindowTitle(self.MESSAGE_WARNING)
        message_box.addButton(QMessageBox.Yes)
        message_box.addButton(QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)
        return message_box.exec_()

    def show_variants(self, text):
        message_box = QMessageBox()
        message_box.setText(text)
        message_box.setWindowTitle(self.MESSAGE_WARNING)
        message_box.addButton(QMessageBox.Yes)
        message_box.addButton(QMessageBox.No)
        message_box.addButton(QMessageBox.Cancel)
        message_box.setDefaultButton(QMessageBox.Yes)
        return message_box.exec_()

    @staticmethod
    def send_system_message(title, text):
        message_box = QMessageBox()
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()