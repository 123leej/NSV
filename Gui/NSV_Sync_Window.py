# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Sync_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
from Exception.NSVExceptions import SimulationFinishException
from PyQt5 import QtCore, QtGui, QtWidgets


class SimulatorUi(object):
    def setup_ui(self, form):
        form.setObjectName("form")
        form.resize(771, 516)

        graphics_view = QtWidgets.QGraphicsView(form)
        graphics_scene = QtWidgets.QGraphicsScene(graphics_view)
        graphics_scene.setSceneRect(5, 11, 769, 441)
        graphics_view.setScene(graphics_scene)

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
        self.horizontal_layout.addWidget(self.push_button)

        self.translate_ui(form)
        QtCore.QMetaObject.connectSlotsByName(form)

        return graphics_view, graphics_scene

    def translate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "KU NSV"))
        self.push_button.setText(_translate("Form", "Finish Simulation & Save result Data"))

    def node_update(self, _graphics_view, _graphics_scene, datas):
        for idx, item in enumerate(sorted(_graphics_scene.items(), key = self.node_numb_key)):
            item.setPos(datas[idx][1], datas[idx][2])

        _graphics_view.updateSceneRect(_graphics_scene.sceneRect())
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
                _graphics_scene.addItem(a)
            else:
                b = QtWidgets.QGraphicsEllipseItem(1, 1, 15, 15)
                b.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                b.setBrush(QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern))
                b.setZValue(data[0])
                _graphics_scene.addItem(b)

    def finish_simulation(self):
        raise SimulationFinishException
