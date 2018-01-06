# -*- coding: utf-8 -*-

from gui.apiOS import ApiOS

import file_extension


def get_outputs(schema, path_to_dir):
    '''
    Получение наборов данных, и названий файлов для экспорта
    :param schema: Все данные
    :param path_to_dir: Путь к папке для экспорта
    :return: Набор данные/путь к файлу
    '''
    outputs = []
    for item in schema["data"]:
        if not item["output_data"] or (len(item["output_data"]) <= 0):
            continue
        name, ext = file_extension.split_path(item["path"])
        path = path_to_dir + "/" + name + "_OUT.csv"

        arr = {
            "path": path,
            "data": item["output_data"]
        }

        outputs.append(arr)

    return outputs


def write_output(outputs):
    """
    Запись списка данных в файлы
    :param outputs: Набор данные:путь к файлу
    :return: None
    """
    try:
        for item in outputs:
            file = open(item["path"], "w")
            for row in item["data"]:
                file.write("%s,%s\n" % (row["point"][0], row["point"][1]))
            file.close()
    except Exception as err:
        ApiOS().send_system_message("Ошибка", "Ошибка при записи данных")


def push(schema, path_to_dir):
    """
    Пакетный экспорт данных в указанную папку
    :param schema: Данные для экспорта
    :param path_to_dir: Путь к папке
    :return: None
    """
    try:
        res = get_outputs(schema, path_to_dir)
        write_output(res)
    except Exception as err:
        ApiOS().send_system_message("Ошибка", "Ошибка при записи данных")