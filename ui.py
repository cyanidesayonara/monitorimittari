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
        MainWindow.resize(780, 731)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setGeometry(QtCore.QRect(60, 20, 141, 41))
        self.backwardButton.setObjectName("backwardButton")
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(570, 20, 141, 41))
        self.forwardButton.setObjectName("forwardButton")
        self.deviceBox = QtWidgets.QComboBox(self.centralwidget)
        self.deviceBox.setGeometry(QtCore.QRect(260, 30, 261, 22))
        self.deviceBox.setObjectName("deviceBox")
        self.deviceBoxLabel = QtWidgets.QLabel(self.centralwidget)
        self.deviceBoxLabel.setGeometry(QtCore.QRect(260, 6, 91, 20))
        self.deviceBoxLabel.setObjectName("deviceBoxLabel")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(280, 240, 231, 101))
        self.lcdNumber.setObjectName("lcdNumber")
        self.measurementLabel = QtWidgets.QLabel(self.centralwidget)
        self.measurementLabel.setGeometry(QtCore.QRect(290, 150, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.measurementLabel.setFont(font)
        self.measurementLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.measurementLabel.setObjectName("measurementLabel")
        self.tableWidgetLeft = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidgetLeft.setGeometry(QtCore.QRect(20, 80, 250, 600))
        self.tableWidgetLeft.setShowGrid(True)
        self.tableWidgetLeft.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetLeft.setRowCount(28)
        self.tableWidgetLeft.setColumnCount(3)
        self.tableWidgetLeft.setObjectName("tableWidgetLeft")
        self.tableWidgetLeft.horizontalHeader().setVisible(True)
        self.tableWidgetLeft.horizontalHeader().setDefaultSectionSize(78)
        self.tableWidgetLeft.horizontalHeader().setMinimumSectionSize(39)
        self.tableWidgetLeft.verticalHeader().setVisible(False)
        self.tableWidgetLeft.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidgetLeft.verticalHeader().setDefaultSectionSize(20)
        self.tableWidgetLeft.verticalHeader().setMinimumSectionSize(20)
        self.tableWidgetRight = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidgetRight.setGeometry(QtCore.QRect(520, 80, 250, 600))
        self.tableWidgetRight.setShowGrid(True)
        self.tableWidgetRight.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetRight.setRowCount(28)
        self.tableWidgetRight.setColumnCount(3)
        self.tableWidgetRight.setObjectName("tableWidgetRight")
        self.tableWidgetRight.horizontalHeader().setVisible(True)
        self.tableWidgetRight.horizontalHeader().setDefaultSectionSize(78)
        self.tableWidgetRight.verticalHeader().setVisible(False)
        self.tableWidgetRight.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidgetRight.verticalHeader().setDefaultSectionSize(20)
        self.tableWidgetRight.verticalHeader().setMinimumSectionSize(20)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 21))
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
        self.deviceBoxLabel.setText(_translate("MainWindow", "Valitse laite"))
        self.measurementLabel.setText(_translate("MainWindow", "Mittaus"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

