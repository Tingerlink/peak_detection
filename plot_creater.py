# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure

import matplotlib
import numpy as np
import matplotlib.ticker


def create_plot(data, type_graph="two", type_data="input"):
    """
    Построение графика в зависимости от его типа
    :param data: Набор координат
    :param type_graph: Тип графика (1/2 графика на одном)
    :param type_data: Тип данных (входной/выходной)
    :return: Виджет с графиком
    """
    dpi = 72

    graph_tab = QWidget()
    graph = Figure((18.0, 8.0), dpi=dpi, facecolor='w')

    canvas = FigureCanvas(graph)
    canvas.setParent(graph_tab)

    graph_area = graph.add_subplot(111)

    locator_x = matplotlib.ticker.LinearLocator(10)
    locator_y = matplotlib.ticker.LinearLocator(10)
    graph_area.xaxis.set_major_locator(locator_x)
    graph_area.yaxis.set_major_locator(locator_y)
    graph_area.grid(True)

    graph_toolbar = NavigationToolbar2QT(canvas, graph_tab)

    vertical_layout_tab = QVBoxLayout()
    vertical_layout_tab.setContentsMargins(0, 0, 0, 0)
    vertical_layout_tab.addWidget(canvas)
    vertical_layout_tab.addWidget(graph_toolbar)

    graph_tab.setLayout(vertical_layout_tab)
    graph_area.set_title(data["path"], size=14, family='verdana')

    graph_area.set_xlabel("x", family='verdana')
    graph_area.set_ylabel("y", family='verdana')

    if type_graph == "two":
        in_x = np.array([x[0] for x in data["input_data"]])
        in_y = np.array([y[1] for y in data["input_data"]])
        graph_area.plot(in_x, in_y, marker=' ', linestyle='-')

        out_x = np.array([x["point"][0] for x in data["output_data"]])
        out_y = np.array([y["point"][1] for y in data["output_data"]])
        graph_area.plot(out_x, out_y, marker='o', linestyle=' ')
        graph_area.legend(["input_data", "output_data"])

    else:
        if type_data == "input":
            in_x = np.array([x[0] for x in data["input_data"]])
            in_y = np.array([y[1] for y in data["input_data"]])
            graph_area.plot(in_x, in_y, marker=' ', linestyle='-')
            graph_area.legend(["input"])
        else:
            in_x = np.array([x[0] for x in data["input_data"]])
            in_y = np.array([y[1] for y in data["input_data"]])
            graph_area.plot(in_x, in_y, marker=' ', linestyle='--')

            out_x = np.array([x["point"][0] for x in data["output_data"]])
            out_y = np.array([y["point"][1] for y in data["output_data"]])
            graph_area.plot(out_x, out_y, marker='o', linestyle=' ')

            graph_area.legend(["input", "output"])

    canvas.draw()

    return graph_tab
