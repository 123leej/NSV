# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Analysis_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# TODO it must have get_parameter function link with NSV_First_Dialog there is example in NSV_Sync_Dialog
# TODO get_parameter must return {'file_path': selected file path(string)}


class SetResultDataUi(object):
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
        dialog.setWindowTitle(_translate("Dialog", "KU NSV"))
        self.label.setText(_translate("Dialog", "Select File"))


def get_alalysis_result_dialog():
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = SetResultDataUi()
    ui.setup_ui(dialog)
    dialog.show()
    sys.exit(app.exec_())

