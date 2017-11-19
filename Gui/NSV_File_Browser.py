import sys
from PyQt5 import QtWidgets, QtCore


class FileBrowser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.file_name = ""
        self.init_ui()

    def init_ui(self):
        point = QtCore.QRect(self.left, self.top, self.width, self.height)
        self.setGeometry(QtCore.QRect(point.center(), point.size()))
        self.open_file_name_dialog()

    def open_file_name_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "../Algorithm/",
            "All Files (*);;",
            options=options
        )

    def get_filename(self):
        return self.file_name
