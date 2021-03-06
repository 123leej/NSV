# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Sync_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from Gui.NSV_File_Browser import FileBrowser
from PyQt5 import QtCore, QtGui, QtWidgets


class SetAlgorithmUi(object):
    def setup_ui(self, dialog):
        self.closer = dialog
        dialog.setObjectName("Dialog")
        dialog.setFixedSize(400, 300)

        self.vertical_layout_widget_1 = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget_1.setGeometry(QtCore.QRect(9, 9, 381, 20))
        self.vertical_layout_widget_1.setObjectName("verticalLayoutWidget1")

        self.vertical_layout_widget_2 = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget_2.setGeometry(QtCore.QRect(9, 29, 381, 30))
        self.vertical_layout_widget_2.setObjectName("verticalLayoutWidget2")

        self.vertical_layout_widget_3 = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget_3.setGeometry(QtCore.QRect(9, 59, 381, 50))
        self.vertical_layout_widget_3.setObjectName("verticalLayoutWidget3")

        self.vertical_layout_widget_4 = QtWidgets.QWidget(dialog)
        self.vertical_layout_widget_4.setGeometry(QtCore.QRect(9, 109, 381, 150))
        self.vertical_layout_widget_4.setObjectName("verticalLayoutWidget4")

        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("buttonBox")

        self.label_1_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget_1)
        self.label_1_layout.setContentsMargins(0, 0, 0, 0)
        self.label_1_layout.setObjectName("label1Layout")
        self.label_1 = QtWidgets.QLabel(self.vertical_layout_widget_1)
        self.label_1.setFixedSize(100, 16)
        self.label_1.setObjectName("label1")
        self.label_1_layout.addWidget(self.label_1)

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

        self.set_node_num_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget_3)
        self.set_node_num_layout.setContentsMargins(0, 0, 0, 0)
        self.set_node_num_layout.setObjectName("setNodeNumLayer")
        self.label_2 = QtWidgets.QLabel(self.vertical_layout_widget_3)
        self.label_2.setFixedSize(150, 16)
        self.label_2.setObjectName("label_2")
        self.set_node_num_layout.addWidget(self.label_2)
        self.node_num = QtWidgets.QComboBox(self.vertical_layout_widget_3)
        self.node_num.setFixedSize(100, 20)
        self.node_num.addItems(["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
        self.node_num.setObjectName("nodeNum")
        self.set_node_num_layout.addWidget(self.node_num)

        self.set_zone_range_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget_4)
        self.set_zone_range_layout.setContentsMargins(0, 0, 0, 0)
        self.set_zone_range_layout.setAlignment(QtCore.Qt.AlignTop)
        self.set_zone_range_layout.setObjectName("setZoneRangeLayer")
        self.label_3 = QtWidgets.QLabel(self.vertical_layout_widget_4)
        self.label_3.setFixedSize(150, 16)
        self.label_3.setObjectName("label_3")
        self.set_zone_range_layout.addWidget(self.label_3)
        self.zone_range_bar = QtWidgets.QSlider(self.vertical_layout_widget_4)
        self.zone_range_bar.setRange(50, 300)
        self.zone_range_bar.setValue(100)
        self.zone_range = self.zone_range_bar.value()
        self.zone_range_bar.setOrientation(QtCore.Qt.Horizontal)
        self.zone_range_bar.valueChanged.connect(self.slider_event)
        self.zone_range_bar.setObjectName("zoneRangeBar")
        self.set_zone_range_layout.addWidget(self.zone_range_bar)

        self.translate_ui(dialog)
        self.button_box.accepted.connect(self.set_parameter)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def translate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("KU_NSV", "KU NSV"))
        self.label_1.setText(_translate("Dialog", "Select Algorithm"))
        self.label_2.setText(_translate("Dialog", "Set number of Nodes"))
        self.label_3.setText(_translate("Dialog", "Zone range: 100"))

    def slider_event(self):
        self.zone_range = self.zone_range_bar.value()
        self.label_3.setText("Zone range: " + str(self.zone_range))

    def file_browse(self):
        self.child = FileBrowser()
        self.file_location.setText(self.child.get_filename())

    def set_parameter(self):
        self.algorithm_file_path = self.file_location.text()
        self.number_of_nodes = self.node_num.itemText(self.node_num.currentIndex())

        if self.algorithm_file_path == "":
            sys.exit(0)
        else:
            self.closer.done(0)

    def get_parameter(self):
        return {
            "file_path": self.algorithm_file_path,
            "number_of_nodes": self.number_of_nodes,
            "zone_range": self.zone_range,
            "flag": 1
        }
