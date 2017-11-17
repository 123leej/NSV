# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Sync_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

#[index, x, y, agent_A_distance, agent_B_distance]

data_set = [[1, 100, 100, 10, 200], [2, 150, 150, 10, 200], [3, 200, 200, 10, 200], [4, 250, 250, 10, 200], [5, 300, 300, 10, 200]]


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
        self.push_button.setText(_translate("Form", "Summary"))


    def node_update(self, _graphics_view, _graphics_scene):

            for data in data_set:
                node = QtWidgets.QGraphicsEllipseItem(1, 1, 15, 15)
                node.setPos(data[1], data[2])
                node.setPen(QtGui.QPen(QtCore.Qt.black, 2))
                node.setBrush(QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern))
                _graphics_scene.addItem(node)

            _graphics_view.setScene(_graphics_scene)


import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QDialog()
ui = SimulatorUi()
gv, gs = ui.setup_ui(window)
ui.node_update(gv, gs)

window.show()
sys.exit(app.exec_())