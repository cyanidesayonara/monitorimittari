import sys
from click_me import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    i = 0

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        event.accept()

    def addResult(self):
        value = "hello world "
        self.listWidget.addItem(value + str(self.i))
        self.i = self.i + 1

    def newOnkeyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.addResult()
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
