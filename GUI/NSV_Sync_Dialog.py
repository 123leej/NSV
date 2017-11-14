# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Sync_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

# TODO show empty label and beside of it there is button "..." this button event popup file browser
# TODO update label after "..." button event as set directory
# TODO SET LABEL location
# TODO add node parameter setting


class SetAlgorithmUi(object):
    def setup_ui(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(400, 300)

        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")

        self.vertical_layout_widget = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget.setGeometry(QtCore.QRect(9, 9, 381, 221))
        self.vertical_layout_widget.setObjectName("verticalLayoutWidget")

        self.vertical_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.vertical_layout_widget)
        self.label.setObjectName("label")
        self.vertical_layout.addWidget(self.label)

        self.translate_ui(dialog)
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def translate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Select Algorithm"))



