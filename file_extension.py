# -*- coding: utf-8 -*-

import os.path


def split_path(path):
    """
    Разделение пути и имени файла от его расширения
    :param path: Полный путь к файлу
    :return:
    """
    path_to_dir, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)

    return basename, extension
