# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Analysis_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from Gui.NSV_File_Browser import FileBrowser
from PyQt5 import QtCore, QtGui, QtWidgets

# TODO it must have get_parameter function link with NSV_First_Dialog there is example in NSV_Sync_Dialog
# TODO get_parameter must return {'file_path': selected file path(string)}


class SetResultDataUi(object):
    def setup_ui(self, dialog):
        self.closer = dialog
        dialog.setObjectName("Dialog")
        dialog.setFixedSize(400, 300)

        self.vertical_layout_widget_1 = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget_1.setGeometry(QtCore.QRect(9, 9, 381, 20))
        self.vertical_layout_widget_1.setObjectName("verticalLayoutWidget1")

        self.vertical_layout_widget_2 = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget_2.setGeometry(QtCore.QRect(9, 29, 381, 230))
        self.vertical_layout_widget_2.setObjectName("verticalLayoutWidget2")

        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")

        self.label_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget_1)
        self.label_layout.setContentsMargins(0, 0, 0, 0)
        self.label_layout.setObjectName("label1Layout")
        self.label = QtWidgets.QLabel(self.vertical_layout_widget_1)
        self.label.setFixedSize(100, 16)
        self.label.setObjectName("label1")
        self.label_layout.addWidget(self.label)

        self.file_browser_layout = QtWidgets.QHBoxLayout(self.vertical_layout_widget_2)
        self.file_browser_layout.setContentsMargins(0, 0, 0, 0)
        self.file_browser_layout.setAlignment(QtCore.Qt.AlignTop)
        self.file_browser_layout.setObjectName("fileBrowserLayout")
        self.file_location = QtWidgets.QLineEdit(self.vertical_layout_widget_2)
        self.file_location.setReadOnly(True)
        self.file_location.setFixedSize(350, 20)
        self.file_browser_layout.addWidget(self.file_location)
        self.browse_button = QtWidgets.QPushButton(self.vertical_layout_widget_2)
        self.browse_button.setText("•••")
        self.browse_button.setFixedSize(30, 20)
        self.browse_button.clicked.connect(self.file_browse)
        self.file_browser_layout.addWidget(self.browse_button)

        self.translate_ui(dialog)
        self.button_box.accepted.connect(self.set_parameter)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def translate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "KU NSV"))
        self.label.setText(_translate("Dialog", "Select File"))

    def file_browse(self):
        self.child = FileBrowser()
        self.file_location.setText(self.child.get_filename())

    def set_parameter(self):
        self.result_data_file_path = self.file_location.text()

        if self.result_data_file_path == "":
            sys.exit(0)
        else:
            self.closer.done(0)

    def get_parameter(self):
        return {
            "file_path": self.result_data_file_path,
            "flag": 2
        }
