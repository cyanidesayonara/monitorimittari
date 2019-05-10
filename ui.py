# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(495, 398)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setGeometry(QtCore.QRect(140, 320, 75, 23))
        self.backwardButton.setObjectName("backwardButton")
        self.measurementList = QtWidgets.QListWidget(self.centralwidget)
        self.measurementList.setGeometry(QtCore.QRect(110, 110, 251, 191))
        self.measurementList.setObjectName("measurementList")
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(240, 320, 75, 23))
        self.forwardButton.setObjectName("forwardButton")
        self.deviceBox = QtWidgets.QComboBox(self.centralwidget)
        self.deviceBox.setGeometry(QtCore.QRect(110, 30, 251, 22))
        self.deviceBox.setObjectName("deviceBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(176, 70, 121, 20))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.deviceBoxLabel = QtWidgets.QLabel(self.centralwidget)
        self.deviceBoxLabel.setGeometry(QtCore.QRect(110, 6, 91, 20))
        self.deviceBoxLabel.setObjectName("deviceBoxLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 495, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Monitorimittari"))
        self.backwardButton.setText(_translate("MainWindow", "<-"))
        self.forwardButton.setText(_translate("MainWindow", "->"))
        self.deviceBoxLabel.setText(_translate("MainWindow", "Choose device"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

