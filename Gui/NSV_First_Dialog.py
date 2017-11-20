# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_First_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from Gui.NSV_Sync_Dialog import SetAlgorithmUi
from Gui.NSV_Analysis_Dialog import SetResultDataUi
from PyQt5 import QtCore, QtGui, QtWidgets


class NSVUi(object):
    def setup_ui(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.setFixedSize(400, 226)

        self.vertical_layout_widget = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget.setGeometry(QtCore.QRect(9, 9, 381, 211))
        self.vertical_layout_widget.setObjectName("verticalLayoutWidget")

        self.vertical_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.vertical_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.vertical_layout.addWidget(self.label)
        self.horizontal_layout_3 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_3.setObjectName("horizontalLayout_3")

        self.push_button = QtWidgets.QPushButton(self.vertical_layout_widget)
        self.push_button.setStyleSheet('QPushButton {color: black;}')
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.push_button.sizePolicy().hasHeightForWidth())
        self.push_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.push_button.setFont(font)
        self.push_button.setObjectName("pushButton")
        self.horizontal_layout_3.addWidget(self.push_button)
        self.push_button.clicked.connect(self.btn1_clicked)

        self.push_button_2 = QtWidgets.QPushButton(self.vertical_layout_widget)
        self.push_button_2.setStyleSheet('QPushButton {color: black;}')
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.push_button_2.sizePolicy().hasHeightForWidth())
        self.push_button_2.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.push_button_2.setFont(font)
        self.push_button_2.setObjectName("pushButton_2")
        self.horizontal_layout_3.addWidget(self.push_button_2)
        self.push_button_2.clicked.connect(self.btn2_clicked)

        self.vertical_layout.addLayout(self.horizontal_layout_3)

        self.translate_ui(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def translate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "KU NSV"))
        self.label.setText(_translate("Dialog", "KU-NSV"))
        self.push_button.setText(_translate("Dialog", "Sync\nSimulation"))
        self.push_button_2.setText(_translate("Dialog", "Performance\nAnalysis"))

    def btn1_clicked(self):
        self.get_dialog_event(btn=1)

    def btn2_clicked(self):
        self.get_dialog_event(btn=2)

    def get_dialog_event(self, btn):
        self.dialog = QtWidgets.QDialog()

        if btn == 1:
            self.child = SetAlgorithmUi()

        if btn == 2:
            self.child = SetResultDataUi()

        self.child.setup_ui(self.dialog)
        self.dialog.show()

    def start(self):
        app = QtWidgets.QApplication(sys.argv)
        self.dialog = QtWidgets.QDialog()
        self.setup_ui(self.dialog)
        self.dialog.show()
        app.exec_()

        return self.child.get_parameter()

