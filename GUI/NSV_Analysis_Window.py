# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NSV_Analysis_Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# TODO Ui dosen't show up
# TODO button event accept -> analysis window


class AnalysisResultUi(object):
    def setup_ui(self, form):
        form.setObjectName("Form")
        form.resize(400, 300)

        self.text_browser = QtWidgets.QTextBrowser(form)
        self.text_browser.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.text_browser.setObjectName("textBrowser")

        self.translate_ui(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def translate_ui(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "Form"))


def get_analysis_result_window():
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = AnalysisResultUi()
    ui.setup_ui(form)
    form.show()
    sys.exit(app.exec_())

