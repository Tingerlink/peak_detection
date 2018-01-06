# -*- coding: utf-8 -*-

import time
import math


def detect_peaks(input_data, beta, width_segment):
    """
    :param input_data:
    :param beta: Минимальная ширина прогиба/пика
    :param width_segment: Кол-во сегментов
    :return:
    """

    axis_domain = get_axis_domain(input_data)
    count_segment = get_count_segment(axis_domain, width_segment)

    t_set = get_max_min_set(input_data, width_segment, count_segment)

    t_set = sorted(t_set, key=lambda x: (x["point"][0], x["pos"] ))

    count = 1
    while count != 0:
        t_set, count = delete_middle(t_set)

    count = 1
    while count != 0:
        t_set, count = delete_two_min(t_set)

    count = 1
    while count != 0:
        t_set, count = delete_two_max(t_set)

    count = 1
    while count != 0:
        t_set, count = delete_type_1_4_class(t_set, beta)

    count = 1
    while count != 0:
        t_set, count = delete_type_5_class(t_set, beta)

    count = 1
    while count != 0:
        t_set, count = delete_type_6_class(t_set, beta)

    return t_set


def get_axis_domain(data):
    max_x = max([x[0] for x in data])
    min_x = min([x[0] for x in data])

    return min_x, max_x


def get_count_segment(axis_domain, width_segment):
    length = int(math.ceil((axis_domain[1] - axis_domain[0]) / width_segment))

    return length


def get_max_min_set(input_data, width_segment, count_segment):
    if not input_data or (len(input_data) == 0):
        return

    t_set = []
    input_len = len(input_data)
    index = 0
    start_position = input_data[0][0]

    for i in range(count_segment):
        max_in_segment = None
        min_in_segment = None

        segment_limit = start_position + (i + 1) * width_segment

        while (input_data[index][0] <= segment_limit) and (input_len > (index + 1)):
            index += 1

            if not max_in_segment:
                max_in_segment = input_data[index]

            if not min_in_segment:
                min_in_segment = input_data[index]

            if max_in_segment[1] < input_data[index][1]:
                max_in_segment = input_data[index]

            if min_in_segment[1] > input_data[index][1]:
                min_in_segment = input_data[index]

        if (not max_in_segment) or (not min_in_segment):
            continue

        if max_in_segment[0] > min_in_segment[0]:
            t_set.append({"point": max_in_segment, "type": "max", "pos": "right"})
            t_set.append({"point": min_in_segment, "type": "min", "pos": "left"})
        else:
            t_set.append({"point": max_in_segment, "type": "max", "pos": "left"})
            t_set.append({"point": min_in_segment, "type": "min", "pos": "right"})

    return t_set


def delete_middle(t_set):
    count = len(t_set)
    del_count = 0
    for index in range(count):
        if index >= len(t_set) - 1:
            break

        if ((t_set[index]["pos"] == "right") and (t_set[index + 1]["pos"] == "left") and
                (t_set[index]["type"] != t_set[index + 1]["type"])):
            t_set.pop(index)
            t_set.pop(index)
            del_count += 2

    return t_set, del_count


def delete_two_min(t_set):
    count = len(t_set)
    del_count = 0
    for index in range(count):
        if index >= len(t_set) - 1:
            break

        if t_set[index]["type"] == t_set[index + 1]["type"] == "min":
            del_index = index if (t_set[index]["point"][1] > t_set[index + 1]["point"][1]) else (index + 1)
            t_set.pop(del_index)
            del_count += 1

    return t_set, del_count


def delete_two_max(t_set):
    count = len(t_set)
    del_count = 0
    for index in range(count):
        if index >= len(t_set) - 1:
            break

        if (t_set[index]["type"] == t_set[index + 1]["type"] == "max"):
            del_index = index if (t_set[index]["point"][1] < t_set[index + 1]["point"][1]) else (index + 1)
            t_set.pop(del_index)
            del_count += 1

    return t_set, del_count


def delete_type_1_4_class(t_set, beta):
    index = 0
    count_del = 0
    arr = []
    while (index + 4) < len(t_set):
        s = ShapeFiveType(t_set[index:index+5])
        type_shape = s.get_type()
        t = TreatmentExtremePoints(t_set[index:index + 5], beta, type_shape)
        if type_shape:
            t.go()
            count_del += 5 - len(t.T)
        arr += t.T
        index += 5

    while index < len(t_set):
        arr.append(t_set[index])
        index += 1

    return arr, count_del


def delete_type_5_class(t_set, beta):
    index = 0
    count_del = 0
    arr = []
    while (index + 5) < len(t_set):
        s = ShapeSixType(t_set[index:index+6])
        type_shape = s.get_type()
        t = TreatmentExtremePoints(t_set[index:index + 6], beta, type_shape)
        if s.get_type():
            t.go()
            count_del += 6 - len(t.T)
        arr += t.T
        index += 6

    while index < len(t_set):
        arr.append(t_set[index])
        index += 1

    return arr, count_del


def delete_type_6_class(t_set, beta):
    index = 0
    count_del = 0
    arr = []
    while (index + 6) < len(t_set):
        s = ShapeSevenType(t_set[index:index+7])
        type_shape = s.get_type()
        t = TreatmentExtremePoints(t_set[index:index + 7], beta, type_shape)
        if s.get_type():
            t.go()
            count_del += 7 - len(t.T)
        arr += t.T
        index += 7

    while index < len(t_set):
        arr.append(t_set[index])
        index += 1

    return arr, count_del


class TreatmentExtremePoints:
    def __init__(self, points, beta, type_shape):
        self.T = points
        self.beta = beta
        self.type_shape = ShapeFiveType(points).get_type()

    def go(self):
        if self.type_shape in ["type1", "type2", "type3", "type4"]:
            self.go_class_3()

        if self.type_shape in ["type5", "type6", "type7", "type8"]:
            self.go_class_4()

        if self.type_shape in ["type9", "type10"]:
            self.go_class_5()

        if self.type_shape in ["type11", "type12"]:
            self.go_class_6()

    def go_class_3(self):
        if ((self.dis(self.T[0], self.T[2]) < self.beta) or (self.dis(self.T[1], self.T[3]) < self.beta)
                or (self.dis(self.T[2], self.T[4]) < self.beta)):
            self.T.pop(2)
            self.concat_max(1, 3)

    def go_class_4(self):
        if ((self.dis(self.T[0], self.T[2]) < self.beta) or (self.dis(self.T[1], self.T[3]) < self.beta)
                or (self.dis(self.T[2], self.T[4]) < self.beta)):
            self.T.pop(2)
            self.concat_min(1, 3)

    def go_class_5(self):
        if self.dis(self.T[1], self.T[2]) > self.dis(self.T[3], self.T[4]):
            self.T.pop(3)
            self.T.pop(3)
        else:
            self.T.pop(1)
            self.T.pop(1)

    def go_class_6(self):

        delete_index = []

        if (self.T[0]["point"][1] < self.T[2]["point"][1]) and (self.T[4]["point"][1] < self.T[6]["point"][1]):
            if self.dis(self.T[0], self.T[3]) > self.dis(self.T[3], self.T[6]):
                delete_index.append(4)
                delete_index.append(5)
            else:
                delete_index.append(1)
                delete_index.append(2)
        else:
            if self.T[0]["point"][1] < self.T[2]["point"][1]:
                delete_index.append(1)
                delete_index.append(2)

            if self.T[4]["point"][1] < self.T[6]["point"][1]:
                delete_index.append(4)
                delete_index.append(5)

        if (self.T[0]["point"][1] > self.T[2]["point"][1]) and (self.T[4]["point"][1] < self.T[6]["point"][1]):
            if self.dis(self.T[0], self.T[3]) > self.dis(self.T[3], self.T[6]):
                delete_index.append(4)
                delete_index.append(5)
            else:
                delete_index.append(1)
                delete_index.append(2)
        else:
            if self.T[0]["point"][1] > self.T[2]["point"][1]:
                delete_index.append(1)
                delete_index.append(2)
            if self.T[4]["point"][1] < self.T[6]["point"][1]:
                delete_index.append(4)
                delete_index.append(5)

        t = reversed(list(set(delete_index)))

        for index in t:
            self.T.pop(index)

    def concat_max(self, index_1, index_2):
        if self.T[index_1]["point"][1] > self.T[index_2]["point"][1]:
            self.T.pop(index_1)
        else:
            self.T.pop(index_2)

    def concat_min(self, index_1, index_2):
        if self.T[index_1]["point"][1] < self.T[index_2]["point"][1]:
            self.T.pop(index_1)
        else:
            self.T.pop(index_2)

    def dis(self, x0, x1):
        return math.fabs(x1["point"][0] - x0["point"][0])


class ShapeFiveType:
    def __init__(self, points):
        self.T = points

    def get_type(self):
        mask = self.mask()
        if mask == 1:
            if self.is_type_1():
                return "type1"
            if self.is_type_2():
                return "type2"
            if self.is_type_3():
                return "type3"
            if self.is_type_4():
                return "type4"
        elif mask == 0:
            if self.is_type_5():
                return "type5"
            if self.is_type_6():
                return "type6"
            if self.is_type_7():
                return "type7"
            if self.is_type_8():
                return "type8"
        else:
            return None

    def mask(self):
        if ((self.T[0]["type"] == self.T[2]["type"] == self.T[4]["type"] == "max") and
                (self.T[1]["type"] == self.T[3]["type"] == "min")):
            return 1

        if ((self.T[0]["type"] == self.T[2]["type"] == self.T[4]["type"] == "min") and
                (self.T[1]["type"] == self.T[3]["type"] == "max")):
            return 0

        return -1

    def is_type_1(self):
        return self.T[0]["point"][1] > self.T[2]["point"][1] > self.T[4]["point"][1]

    def is_type_2(self):
        return (self.T[0]["point"][1] > self.T[2]["point"][1]) and (self.T[4]["point"][1] > self.T[2]["point"][1])

    def is_type_3(self):
        return self.T[0]["point"][1] < self.T[2]["point"][1] < self.T[4]["point"][1]

    def is_type_4(self):
        return (self.T[0]["point"][1] < self.T[2]["point"][1]) and (self.T[4]["point"][1] > self.T[2]["point"][1])

    def is_type_5(self):
        return self.T[0]["point"][1] < self.T[2]["point"][1] < self.T[4]["point"][1]

    def is_type_6(self):
        return (self.T[0]["point"][1] < self.T[2]["point"][1]) and (self.T[4]["point"][1] > self.T[2]["point"][1])

    def is_type_7(self):
        return self.T[0]["point"][1] > self.T[2]["point"][1] > self.T[4]["point"][1]

    def is_type_8(self):
        return (self.T[0]["point"][1] > self.T[2]["point"][1]) and (self.T[4]["point"][1] > self.T[2]["point"][1])


class ShapeSixType:
    def __init__(self, points):
        self.T = points

    def get_type(self):
        mask = self.mask()
        if mask == 1:
            if self.is_type_1():
                return "type9"
        elif mask == 0:
            if self.is_type_2():
                return "type10"
        else:
            return None

    def mask(self):
        if ((self.T[0]["type"] == self.T[2]["type"] == self.T[4]["type"] == "max") and
                (self.T[1]["type"] == self.T[3]["type"] == self.T[5]["type"] == "min")):
            return 1

        if ((self.T[0]["type"] == self.T[2]["type"] == self.T[4]["type"] == "min") and
                (self.T[1]["type"] == self.T[3]["type"] == self.T[5]["type"] == "max")):
            return 0

        return -1

    def is_type_1(self):
        res = (self.T[0]["point"][1] < self.T[2]["point"][1] and
               self.T[4]["point"][1] < self.T[2]["point"][1] and
               self.T[1]["point"][1] > self.T[3]["point"][1] and
               self.T[5]["point"][1] > self.T[3]["point"][1])

        return res

    def is_type_2(self):
        res = (self.T[0]["point"][1] > self.T[2]["point"][1] and
               self.T[4]["point"][1] > self.T[2]["point"][1] and
               self.T[1]["point"][1] < self.T[3]["point"][1] and
               self.T[5]["point"][1] < self.T[3]["point"][1])

        return res


class ShapeSevenType:
    def __init__(self, points):
        self.T = points

    def get_type(self):
        mask = self.mask()
        if mask == 1:
            if self.is_type_1():
                return "type11"
        elif mask == 0:
            if self.is_type_2():
                return "type12"
        else:
            return None

    def mask(self):
        if ((self.T[0]["type"] == self.T[2]["type"] == self.T[4]["type"] == self.T[6]["type"] == "min") and
                (self.T[1]["type"] == self.T[3]["type"] == self.T[5]["type"] == "max")):
            return 1

        if ((self.T[0]["type"] == self.T[2]["type"] == self.T[4]["type"] == self.T[6]["type"] == "max") and
                (self.T[1]["type"] == self.T[3]["type"] == self.T[5]["type"] == "min")):
            return 0

        return -1

    def is_type_1(self):
        res = (self.T[0]["point"][1] > self.T[2]["point"][1] and
               self.T[4]["point"][1] > self.T[2]["point"][1] and
               self.T[1]["point"][1] < self.T[3]["point"][1] and
               self.T[5]["point"][1] < self.T[3]["point"][1])

        return res

    def is_type_2(self):
        res = (self.T[0]["point"][1] > self.T[2]["point"][1] and
               self.T[4]["point"][1] > self.T[2]["point"][1] and
               self.T[1]["point"][1] < self.T[3]["point"][1] and
               self.T[5]["point"][1] < self.T[3]["point"][1])

        return res