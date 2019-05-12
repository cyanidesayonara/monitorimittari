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
        MainWindow.resize(780, 681)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setGeometry(QtCore.QRect(310, 610, 75, 23))
        self.backwardButton.setObjectName("backwardButton")
        self.resultList_1 = QtWidgets.QListWidget(self.centralwidget)
        self.resultList_1.setGeometry(QtCore.QRect(260, 110, 131, 491))
        self.resultList_1.setObjectName("resultList_1")
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(410, 610, 75, 23))
        self.forwardButton.setObjectName("forwardButton")
        self.deviceBox = QtWidgets.QComboBox(self.centralwidget)
        self.deviceBox.setGeometry(QtCore.QRect(260, 30, 251, 22))
        self.deviceBox.setObjectName("deviceBox")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(260, 60, 131, 20))
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.deviceBoxLabel = QtWidgets.QLabel(self.centralwidget)
        self.deviceBoxLabel.setGeometry(QtCore.QRect(260, 6, 91, 20))
        self.deviceBoxLabel.setObjectName("deviceBoxLabel")
        self.resultList_2 = QtWidgets.QListWidget(self.centralwidget)
        self.resultList_2.setGeometry(QtCore.QRect(400, 110, 131, 491))
        self.resultList_2.setObjectName("resultList_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 60, 121, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(270, 80, 113, 20))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(410, 80, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.monitorLabel_1 = QtWidgets.QLabel(self.centralwidget)
        self.monitorLabel_1.setGeometry(QtCore.QRect(56, 180, 131, 20))
        self.monitorLabel_1.setObjectName("monitorLabel_1")
        self.monitorLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.monitorLabel_2.setGeometry(QtCore.QRect(596, 180, 121, 20))
        self.monitorLabel_2.setObjectName("monitorLabel_2")
        self.monitorLineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.monitorLineEdit_1.setGeometry(QtCore.QRect(52, 200, 131, 20))
        self.monitorLineEdit_1.setObjectName("monitorLineEdit_1")
        self.monitorLineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.monitorLineEdit_2.setGeometry(QtCore.QRect(590, 200, 131, 20))
        self.monitorLineEdit_2.setObjectName("monitorLineEdit_2")
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
        self.label_1.setText(_translate("MainWindow", "Left"))
        self.deviceBoxLabel.setText(_translate("MainWindow", "Choose device"))
        self.label_2.setText(_translate("MainWindow", "Right"))
        self.monitorLabel_1.setText(_translate("MainWindow", "Vasen L-Numero"))
        self.monitorLabel_2.setText(_translate("MainWindow", "Oikea L-Numero"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

