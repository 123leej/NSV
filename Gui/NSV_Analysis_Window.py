# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Analysis_window_tab.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class AnalysisResultUi(object):
    def __init__(self, dialog, _result_1, _result_2, _result_3, _log):
        self.result_1 = _result_1
        self.result_2 = _result_2
        self.result_3 = _result_3
        self.log = _log

        self.setup_ui(dialog)
        dialog.show()

    def setup_ui(self, form):
        form.setObjectName("Form")
        form.setFixedSize(574, 428)
        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)

        self.tabWidget = QtWidgets.QTabWidget(form)
        self.tabWidget.blockSignals(True)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.tab_event)
        self.tabWidget.setGeometry(QtCore.QRect(-2, -1, 581, 431))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(5, 4, 561, 281))
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setAutoFillBackground(True)
        self.label.setPalette(self.palette)
        self.label.setObjectName("label")

        self.text_box = QtWidgets.QTextEdit(self.tab)
        self.text_box.setGeometry(QtCore.QRect(5, 294, 561, 101))
        self.text_box.setFrameShape(QtWidgets.QFrame.Box)
        self.text_box.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.text_box.ensureCursorVisible()
        self.text_box.setReadOnly(True)
        self.text_box.setObjectName("textBox")
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(5, 4, 561, 281))
        self.label_2.setAlignment(QtCore.Qt.AlignRight)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_2.setAutoFillBackground(True)
        self.label_2.setPalette(self.palette)
        self.label_2.setObjectName("label_2")

        self.text_box_2 = QtWidgets.QTextEdit(self.tab_2)
        self.text_box_2.setGeometry(QtCore.QRect(5, 294, 561, 101))
        self.text_box_2.setFrameShape(QtWidgets.QFrame.Box)
        self.text_box_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.text_box_2.ensureCursorVisible()
        self.text_box_2.setReadOnly(True)
        self.text_box_2.setObjectName("textBox_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(5, 4, 561, 281))
        self.label_3.setAlignment(QtCore.Qt.AlignRight)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_3.setAutoFillBackground(True)
        self.label_3.setPalette(self.palette)
        self.label_3.setObjectName("label_3")

        self.text_box_3 = QtWidgets.QTextEdit(self.tab_3)
        self.text_box_3.setGeometry(QtCore.QRect(5, 294, 561, 101))
        self.text_box_3.setFrameShape(QtWidgets.QFrame.Box)
        self.text_box_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.text_box_3.ensureCursorVisible()
        self.text_box_3.setReadOnly(True)
        self.text_box_3.setObjectName("textBox_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.translate_ui(form)
        self.tabWidget.blockSignals(False)
        self.tab_event()
        QtCore.QMetaObject.connectSlotsByName(form)

    def translate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "KU NSV"))

        self.label.setText(_translate("Form", "TextLabel1"))
        self.text_box.setText(_translate("Form", "TextBox2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Node Sync"))

        self.label_2.setText(_translate("Form", "TextLabel2"))
        self.text_box_2.setText(_translate("Form", "TextBox3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Hand Over"))

        self.label_3.setText(_translate("Form", "TextLabel3"))
        self.text_box_3.setText(_translate("Form", "TextBox3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Node Info Sync"))

    def tab_event(self):
        if self.tabWidget.currentIndex() is 0:
            _image = self.result_1
        elif self.tabWidget.currentIndex() is 1:
            _image = self.result_2
        elif self.tabWidget.currentIndex() is 2:
            _image = self.result_3

        buffer = QtGui.QPixmap(_image)

        if self.tabWidget.currentIndex() is 0:
            self.label.setPixmap(buffer)
            self.text_box.setText(self.log[0])
        elif self.tabWidget.currentIndex() is 1:
            self.label_2.setPixmap(buffer)
            self.text_box_2.setText(self.log[1])
        elif self.tabWidget.currentIndex() is 2:
            self.label_3.setPixmap(buffer)
            self.text_box_3.setText(self.log[2])
