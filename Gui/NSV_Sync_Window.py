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
        self.running = True
        self.setup_ui(dialog)
        dialog.show()

    def setup_ui(self, form):
        form.setObjectName("form")
        form.setFixedSize(771, 606)

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
        self.push_button.setStyleSheet('QPushButton {color: black;}')
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.push_button.sizePolicy().hasHeightForWidth())
        self.push_button.setSizePolicy(size_policy)
        self.push_button.setObjectName("pushButton")
        self.push_button.clicked.connect(self.finish_simulation)
        self.horizontal_layout.addWidget(self.push_button)

        self.horizontal_layout_widget_2 = QtWidgets.QWidget(form)
        self.horizontal_layout_widget_2.setGeometry(QtCore.QRect(10, 521, 751, 80))
        self.horizontal_layout_widget_2.setObjectName("horizontalLayoutWidget2")

        self.horizontal_layout_2 = QtWidgets.QHBoxLayout(self.horizontal_layout_widget_2)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setObjectName("horizontalLayout2")

        self.log_box = QtWidgets.QTextEdit(self.horizontal_layout_widget_2)
        self.log_box.setFrameShape(QtWidgets.QFrame.Box)
        self.log_box.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.log_box.ensureCursorVisible()
        self.log_box.setReadOnly(True)
        self.log_box.setObjectName("logBox")
        self.horizontal_layout_2.addWidget(self.log_box)

        self.translate_ui(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def translate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "KU NSV"))
        self.push_button.setText(_translate("Form", "Finish Simulation & Save result Data"))

    def node_update(self, agent_a, agent_b, data):
        temp_list = self.graphics_scene.items()
        for idx, item in enumerate(sorted(temp_list, key=self.node_numb_key)[:len(temp_list) - 2]):
            if data[idx][0] == agent_a or data[idx][0] == agent_b:
                item.setPos(data[idx][1] - 15, data[idx][2] - 15)
            else:
                item.setPos(data[idx][1] - 7.5, data[idx][2] - 7.5)

        self.graphics_view.updateSceneRect(self.graphics_scene.sceneRect())
        QtCore.QCoreApplication.processEvents()

    def node_numb_key(self, _item):
        return _item.zValue()

    def get_logs(self, _log):
        self.log_box.setText(_log)

    def draw_nodes(self, agent_a, agent_b, zone_range, datas):
        temp_agent_a = []
        temp_agent_b = []
        for data in datas:
            if data[0] == agent_a or data[0] == agent_b:
                a = QtWidgets.QGraphicsEllipseItem(1, 1, 30, 30)
                a.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                a.setBrush(QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern))
                a.setZValue(data[0])
                if data[0] == agent_a:
                    temp_agent_a.append(data[1])
                    temp_agent_a.append(data[2])
                else:
                    temp_agent_b.append(data[1])
                    temp_agent_b.append(data[2])

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
                c = QtWidgets.QGraphicsEllipseItem(temp_agent_a[0]-zone_range, temp_agent_a[1]-zone_range, zone_range*2, zone_range*2)
            if i is len_data+1:
                c = QtWidgets.QGraphicsEllipseItem(temp_agent_b[0]-zone_range, temp_agent_b[1]-zone_range, zone_range*2, zone_range*2)
            c.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            c.setZValue(i)
            self.graphics_scene.addItem(c)

    def finish_simulation(self):
        self.running = False

    def get_runtime_flag(self):
        return self.running
