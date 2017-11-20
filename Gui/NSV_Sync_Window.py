# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Sync_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from Exception.NSVExceptions import SimulationFinishException
from PyQt5 import QtCore, QtGui, QtWidgets


class SimulatorUi(object):
    def __init__(self, dialog):
        self.setup_ui(dialog)
        dialog.show()

    def setup_ui(self, form):
        form.setObjectName("form")
        form.setFixedSize(771, 516)

        self.graphics_view = QtWidgets.QGraphicsView(form)
        self.graphics_scene = QtWidgets.QGraphicsScene(self.graphics_view)
        self.graphics_scene.setSceneRect(5, 11, 769, 441)
        self.graphics_view.setScene(self.graphics_scene)

        self.horizontal_layout_widget = QtWidgets.QWidget(form)
        self.horizontal_layout_widget.setGeometry(QtCore.QRect(10, 460, 751, 51))
        self.horizontal_layout_widget.setObjectName("horizontalLayoutWidget")

        self.horizontal_layout = QtWidgets.QHBoxLayout(self.horizontal_layout_widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontalLayout")

        self.push_button = QtWidgets.QPushButton(self.horizontal_layout_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.push_button.sizePolicy().hasHeightForWidth())
        self.push_button.setSizePolicy(size_policy)
        self.push_button.setObjectName("pushButton")
        self.push_button.clicked.connect(self.finish_simulation)
        self.horizontal_layout.addWidget(self.push_button)

        self.translate_ui(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def translate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "KU NSV"))
        self.push_button.setText(_translate("Form", "Finish Simulation & Save result Data"))

    def node_update(self, datas, agent_a, agent_b, data):
        temp_list = self.graphics_scene.items()
        for idx, item in enumerate(sorted(temp_list, key=self.node_numb_key)[:len(temp_list) - 2]):
            if datas[idx][0] == agent_a or data[idx][0] == agent_b:
                item.setPos(datas[idx][1] - 15, datas[idx][2] - 15)
            else:
                item.setPos(datas[idx][1] - 7.5, datas[idx][2] - 7.5)
            print(str(idx) + " " + str(datas[idx][1]) + " " + str(datas[idx][2]))

        self.graphics_view.updateSceneRect(self.graphics_scene.sceneRect())
        QtCore.QCoreApplication.processEvents()

    def node_numb_key(self, _item):
        return _item.zValue()

    def draw_nodes(self, _graphics_scene, agent_A, agent_B, datas):

        for data in datas:
            if data[0] == agent_A or data[0] == agent_B:
                a = QtWidgets.QGraphicsEllipseItem(1, 1, 30, 30)
                a.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                a.setBrush(QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern))
                a.setZValue(data[0])
                self.graphics_scene.addItem(a)
            else:
                b = QtWidgets.QGraphicsEllipseItem(1, 1, 15, 15)
                b.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                b.setBrush(QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern))
                b.setZValue(data[0])
                self.graphics_scene.addItem(b)

        len_data = len(datas)
        for i in range(len_data, len_data+2):
            if i is len_data:
                c = QtWidgets.QGraphicsEllipseItem(105, 55, 300, 300)
            if i is len_data+1:
                c = QtWidgets.QGraphicsEllipseItem(356, 55, 300, 300)
            c.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            c.setZValue(i)
            _graphics_scene.addItem(c)

    def finish_simulation(self):
        raise SimulationFinishException
