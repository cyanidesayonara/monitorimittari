# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setGeometry(QtCore.QRect(320, 680, 120, 30))
        self.backwardButton.setObjectName("backwardButton")
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(460, 680, 120, 30))
        self.forwardButton.setObjectName("forwardButton")
        self.deviceBox = QtWidgets.QComboBox(self.centralwidget)
        self.deviceBox.setGeometry(QtCore.QRect(320, 40, 260, 30))
        self.deviceBox.setObjectName("deviceBox")
        self.deviceBoxLabel = QtWidgets.QLabel(self.centralwidget)
        self.deviceBoxLabel.setGeometry(QtCore.QRect(320, 20, 260, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.deviceBoxLabel.setFont(font)
        self.deviceBoxLabel.setObjectName("deviceBoxLabel")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(320, 250, 260, 80))
        self.lcdNumber.setLineWidth(1)
        self.lcdNumber.setMidLineWidth(0)
        self.lcdNumber.setDigitCount(7)
        self.lcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcdNumber.setObjectName("lcdNumber")
        self.measurementLabel = QtWidgets.QLabel(self.centralwidget)
        self.measurementLabel.setGeometry(QtCore.QRect(320, 149, 260, 80))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.measurementLabel.setFont(font)
        self.measurementLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.measurementLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.measurementLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.measurementLabel.setObjectName("measurementLabel")
        self.rightTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.rightTableWidget.setGeometry(QtCore.QRect(20, 50, 272, 671))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rightTableWidget.setFont(font)
        self.rightTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rightTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rightTableWidget.setShowGrid(True)
        self.rightTableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.rightTableWidget.setRowCount(0)
        self.rightTableWidget.setColumnCount(3)
        self.rightTableWidget.setObjectName("rightTableWidget")
        self.rightTableWidget.horizontalHeader().setVisible(True)
        self.rightTableWidget.horizontalHeader().setDefaultSectionSize(90)
        self.rightTableWidget.verticalHeader().setVisible(False)
        self.rightTableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.rightTableWidget.verticalHeader().setDefaultSectionSize(20)
        self.rightTableWidget.verticalHeader().setMinimumSectionSize(20)
        self.leftLNumberInput = QtWidgets.QLineEdit(self.centralwidget)
        self.leftLNumberInput.setGeometry(QtCore.QRect(320, 500, 120, 20))
        self.leftLNumberInput.setObjectName("leftLNumberInput")
        self.rightLNumberInput = QtWidgets.QLineEdit(self.centralwidget)
        self.rightLNumberInput.setGeometry(QtCore.QRect(460, 500, 120, 20))
        self.rightLNumberInput.setObjectName("rightLNumberInput")
        self.leftMonitorLabel = QtWidgets.QLabel(self.centralwidget)
        self.leftMonitorLabel.setGeometry(QtCore.QRect(320, 350, 120, 120))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.leftMonitorLabel.setFont(font)
        self.leftMonitorLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.leftMonitorLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMonitorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.leftMonitorLabel.setWordWrap(True)
        self.leftMonitorLabel.setObjectName("leftMonitorLabel")
        self.rightMonitorLabel = QtWidgets.QLabel(self.centralwidget)
        self.rightMonitorLabel.setGeometry(QtCore.QRect(460, 350, 120, 120))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.rightMonitorLabel.setFont(font)
        self.rightMonitorLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.rightMonitorLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rightMonitorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rightMonitorLabel.setWordWrap(True)
        self.rightMonitorLabel.setObjectName("rightMonitorLabel")
        self.leftLNumberLabel = QtWidgets.QLabel(self.centralwidget)
        self.leftLNumberLabel.setGeometry(QtCore.QRect(320, 480, 120, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.leftLNumberLabel.setFont(font)
        self.leftLNumberLabel.setObjectName("leftLNumberLabel")
        self.rightLNumberLabel = QtWidgets.QLabel(self.centralwidget)
        self.rightLNumberLabel.setGeometry(QtCore.QRect(460, 480, 120, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.rightLNumberLabel.setFont(font)
        self.rightLNumberLabel.setObjectName("rightLNumberLabel")
        self.leftTesterLabel = QtWidgets.QLabel(self.centralwidget)
        self.leftTesterLabel.setGeometry(QtCore.QRect(320, 530, 120, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.leftTesterLabel.setFont(font)
        self.leftTesterLabel.setObjectName("leftTesterLabel")
        self.rightTesterLabel = QtWidgets.QLabel(self.centralwidget)
        self.rightTesterLabel.setGeometry(QtCore.QRect(460, 530, 120, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.rightTesterLabel.setFont(font)
        self.rightTesterLabel.setObjectName("rightTesterLabel")
        self.leftTesterInput = QtWidgets.QLineEdit(self.centralwidget)
        self.leftTesterInput.setGeometry(QtCore.QRect(320, 550, 120, 20))
        self.leftTesterInput.setObjectName("leftTesterInput")
        self.rightTesterInput = QtWidgets.QLineEdit(self.centralwidget)
        self.rightTesterInput.setGeometry(QtCore.QRect(460, 550, 120, 20))
        self.rightTesterInput.setObjectName("rightTesterInput")
        self.leftMonitorSelect = QtWidgets.QPushButton(self.centralwidget)
        self.leftMonitorSelect.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.leftMonitorSelect.setCheckable(True)
        self.leftMonitorSelect.setObjectName("leftMonitorSelect")
        self.leftTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.leftTableWidget.setGeometry(QtCore.QRect(20, 50, 272, 671))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.leftTableWidget.setFont(font)
        self.leftTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.leftTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.leftTableWidget.setShowGrid(True)
        self.leftTableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.leftTableWidget.setRowCount(0)
        self.leftTableWidget.setColumnCount(3)
        self.leftTableWidget.setObjectName("leftTableWidget")
        self.leftTableWidget.horizontalHeader().setVisible(True)
        self.leftTableWidget.horizontalHeader().setDefaultSectionSize(90)
        self.leftTableWidget.horizontalHeader().setHighlightSections(True)
        self.leftTableWidget.verticalHeader().setVisible(False)
        self.leftTableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.leftTableWidget.verticalHeader().setDefaultSectionSize(18)
        self.leftTableWidget.verticalHeader().setMinimumSectionSize(18)
        self.rightMonitorSelect = QtWidgets.QPushButton(self.centralwidget)
        self.rightMonitorSelect.setGeometry(QtCore.QRect(110, 20, 91, 31))
        self.rightMonitorSelect.setCheckable(True)
        self.rightMonitorSelect.setObjectName("rightMonitorSelect")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(200, 20, 92, 31))
        self.saveButton.setObjectName("saveButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(320, 730, 260, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.inputFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputFileLabel.setGeometry(QtCore.QRect(320, 75, 260, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.inputFileLabel.setFont(font)
        self.inputFileLabel.setObjectName("inputFileLabel")
        self.outputFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.outputFileLabel.setGeometry(QtCore.QRect(320, 575, 260, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.outputFileLabel.setFont(font)
        self.outputFileLabel.setObjectName("outputFileLabel")
        self.restoreButton = QtWidgets.QPushButton(self.centralwidget)
        self.restoreButton.setGeometry(QtCore.QRect(20, 720, 136, 31))
        self.restoreButton.setObjectName("restoreButton")
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(155, 720, 137, 31))
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(319, 640, 261, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.themeLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.themeLabel.setFont(font)
        self.themeLabel.setObjectName("themeLabel")
        self.horizontalLayout.addWidget(self.themeLabel)
        self.lightThemeButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.lightThemeButton.setObjectName("lightThemeButton")
        self.horizontalLayout.addWidget(self.lightThemeButton)
        self.darkThemeButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.darkThemeButton.setObjectName("darkThemeButton")
        self.horizontalLayout.addWidget(self.darkThemeButton)
        self.prideThemeButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.prideThemeButton.setObjectName("prideThemeButton")
        self.horizontalLayout.addWidget(self.prideThemeButton)
        self.outputFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.outputFileButton.setGeometry(QtCore.QRect(320, 600, 260, 30))
        self.outputFileButton.setObjectName("outputFileButton")
        self.inputFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.inputFileButton.setGeometry(QtCore.QRect(320, 100, 260, 30))
        self.inputFileButton.setObjectName("inputFileButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
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
        self.backwardButton.setText(_translate("MainWindow", "Edellinen [Backspace]"))
        self.forwardButton.setText(_translate("MainWindow", "Seuraava [Enter]"))
        self.deviceBoxLabel.setText(_translate("MainWindow", "Valitse laite"))
        self.measurementLabel.setText(_translate("MainWindow", "Ei signaalia"))
        self.leftMonitorLabel.setText(_translate("MainWindow", "VASEN MONITORI"))
        self.rightMonitorLabel.setText(_translate("MainWindow", "OIKEA MONITORI"))
        self.leftLNumberLabel.setText(_translate("MainWindow", "L-Numero"))
        self.rightLNumberLabel.setText(_translate("MainWindow", "L-Numero"))
        self.leftTesterLabel.setText(_translate("MainWindow", "Mittaaja(t)"))
        self.rightTesterLabel.setText(_translate("MainWindow", "Mittaaja(t)"))
        self.leftMonitorSelect.setText(_translate("MainWindow", "Vasen"))
        self.rightMonitorSelect.setText(_translate("MainWindow", "Oikea"))
        self.saveButton.setText(_translate("MainWindow", "Tallenna Exceliin"))
        self.inputFileLabel.setText(_translate("MainWindow", "Valitse excel-pohja"))
        self.outputFileLabel.setText(_translate("MainWindow", "Valitse luotava excel tai syötä L-Numero"))
        self.restoreButton.setText(_translate("MainWindow", "Palauta asetukset"))
        self.resetButton.setText(_translate("MainWindow", "Tyhjennä mittaukset"))
        self.themeLabel.setText(_translate("MainWindow", "Teema"))
        self.lightThemeButton.setText(_translate("MainWindow", "Vaalea"))
        self.darkThemeButton.setText(_translate("MainWindow", "Tumma"))
        self.prideThemeButton.setText(_translate("MainWindow", "Pride"))
        self.outputFileButton.setText(_translate("MainWindow", "Ei valittu"))
        self.inputFileButton.setText(_translate("MainWindow", "Ei valittu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
