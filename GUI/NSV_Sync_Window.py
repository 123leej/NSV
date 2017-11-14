# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Sync_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class SimulatorUi(object):
    def setup_ui(self, form):
        form.setObjectName("form")
        form.resize(771, 516)

        self.graphics_view = QtWidgets.QGraphicsView(form)
        self.graphics_view.setGeometry(QtCore.QRect(5, 11, 761, 441))
        self.graphics_view.setObjectName("graphicsView")

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

    def translate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "Form"))
        self.push_button.setText(_translate("Form", "Summary"))


