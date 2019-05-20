from shutil import copyfile
from win32com import client
from pywinusb import hid
from openpyxl import load_workbook
from time import sleep
import styles
from repository import Repository
from defaults import defaults
import json
import warnings
import sys
import os
from ui import Ui_MainWindow
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QFont
shell = client.Dispatch("WScript.Shell")


def resource_path(relative_path):
    """ Get absolute path to resource for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Worker(QRunnable):
    """
    Worker is passed a function from MainWindow which runs in a separate thread
    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon_path = resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.ui.messageBox = QMessageBox(self.ui.centralwidget)
        self.ui.messageBox.setWindowTitle(" ")
        self.all_hids = hid.find_all_hid_devices()
        self.currentIndex = 0

        # selects
        self.ui.deviceBox.activated.connect(self.selectDevice)

        # buttons
        self.ui.forwardButton.clicked.connect(self.addResult)
        self.ui.backwardButton.clicked.connect(self.removeResult)
        self.ui.leftMonitorSelect.clicked.connect(
            lambda: self.setMonitor("left"))
        self.ui.rightMonitorSelect.clicked.connect(
            lambda: self.setMonitor("right"))
        self.ui.lightThemeButton.clicked.connect(
            lambda: self.setTheme("light"))
        self.ui.darkThemeButton.clicked.connect(
            lambda: self.setTheme("dark"))
        self.ui.saveButton.clicked.connect(self.saveData)
        self.ui.inputFileButton.clicked.connect(self.chooseInputFile)
        self.ui.outputFileButton.clicked.connect(self.chooseOutputFile)
        self.ui.resetButton.clicked.connect(self.resetValues)
        self.ui.restoreButton.clicked.connect(self.restoreConfig)

        # inputs
        self.ui.leftLNumberInput.textEdited.connect(
            lambda: self.changeText(self.ui.leftLNumberInput))
        self.ui.rightLNumberInput.textEdited.connect(
            lambda: self.changeText(self.ui.rightLNumberInput))
        self.ui.leftTesterInput.textEdited.connect(
            lambda: self.changeText(self.ui.leftTesterInput))
        self.ui.rightTesterInput.textEdited.connect(
            lambda: self.changeText(self.ui.rightTesterInput))

        self.threadpool = QThreadPool()
        self.device = None
        self.currentMeasurement = None
        self.rawValue = None

    def restoreConfig(self):
        configFile = "config.json"
        with open(configFile, "w+") as f:
            f.write(json.dumps(defaults))
        self.configure()

    def resetValues(self):
        for index, result in enumerate(self.db.results):
            if index < len(self.db.leftResults):
                item = self.ui.leftTableWidget.takeItem(
                    index, 1)
            else:
                item = self.ui.rightTableWidget.takeItem(
                    index - len(self.db.leftResults), 1)
            del item

            try:
                result.value = ""
            except KeyError:
                pass

        self.currentIndex = 0

        self.ui.progressBar.setValue(
            self.currentIndex / len(self.db.results) * 100)

        self.setMonitor("left")

    def chooseInputFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "", "C:/Mittaus", "Excel file(*.xls *.xlsx *.xlsm)", options=options)
        if fileName:
            self.ui.inputFileLabel.setText(fileName.split("/")[-1])
        self.db.inputFile = fileName
        self.db.freeze()

    def chooseOutputFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "", "C:/Mittaus", "Excel file(*.xls *.xlsx *.xlsm)", options=options)
        if fileName:
            if "." not in fileName:
                fileName = fileName + ".xlsm"
            elif not fileName.split(".")[-1] == "xlsm":
                fileName = ".".join(fileName.split(".")[:-1] + "xlsm")
            self.ui.outputFileLabel.setText(fileName.split("/")[-1])
            self.db.outputFile = fileName
            self.db.freeze()

    def saveData(self):
        try:
            # suppress excel warnings
            warnings.filterwarnings("ignore")

            # make a copy of base excel file
            copyfile(self.db.inputFile,
                     self.db.outputFile)

            # load workbook and activate worksheet
            workbook = load_workbook(
                self.db.outputFile, keep_vba=True)
            worksheet = workbook.active

            if self.db.leftLNumber.value:
                worksheet[self.db.leftLNumber.cell
                          ] = self.db.leftLNumber.value

            if self.db.rightLNumber.value:
                worksheet[self.db.rightLNumber.cell
                          ] = self.db.rightLNumber.value

            if self.db.leftTester.value:
                worksheet[self.db.leftTester.cell
                          ] = self.db.leftTester.value

            if self.db.rightTester.value:
                worksheet[self.db.rightTester.cell
                          ] = self.db.rightTester.value

            # input measurements
            for result in self.db.results:
                if result.value:
                    worksheet[result.cell] = float(
                        result.value)

            # save excel
            workbook.save(self.db.outputFile)
            self.ui.messageBox.setText(
                "Tallennettu tiedostoon {0}.".format(self.db.outputFile))
            self.ui.messageBox.show()

        # if file is used by another process
        except PermissionError as e:
            self.ui.messageBox.setText(
                "Excel-tiedosto on auki toisessa ikkunassa. Ole hyvä ja sulje tiedosto.")
            self.ui.messageBox.show()
        # if base excel file doesn't exist
        except FileNotFoundError as e:
            self.ui.messageBox.setText(
                "Excel-tiedostoa ei löydy. Ole hyvä ja valitse tiedosto uudelleen.")
            self.ui.messageBox.show()

    def setMonitor(self, monitor):
        if monitor == "right":
            self.ui.leftTableWidget.hide()
            self.ui.rightTableWidget.show()
            self.ui.leftMonitorSelect.setChecked(False)
            self.ui.rightMonitorSelect.setChecked(True)
        else:
            self.ui.leftTableWidget.show()
            self.ui.rightTableWidget.hide()
            self.ui.leftMonitorSelect.setChecked(True)
            self.ui.rightMonitorSelect.setChecked(False)

    def setTheme(self, theme):
        if theme == "dark":
            self.ui.darkThemeButton.setChecked(True)
            stylesheet = styles.base + styles.dark
        else:
            self.ui.lightThemeButton.setChecked(True)
            stylesheet = styles.base + styles.light
        self.setStyleSheet(stylesheet)
        self.db.theme = theme
        self.db.freeze()

    def setCurrentIndex(self, row):
        if self.ui.leftMonitorSelect.isChecked() == True:
            self.currentIndex = row.row()
        else:
            self.currentIndex = row.row() + len(self.db.leftResults)

    def configure(self):
        self.db = Repository()
        self.setTheme(self.db.theme)
        self.setMonitor("left")

        # config tables
        self.ui.leftTableWidget.setRowCount(len(self.db.leftResults))
        self.ui.rightTableWidget.setRowCount(len(self.db.rightResults))
        self.ui.rightTableWidget.clicked.connect(self.setCurrentIndex)
        self.ui.leftTableWidget.clicked.connect(self.setCurrentIndex)
        self.ui.leftTableWidget.setHorizontalHeaderLabels(
            ['Nimi', 'Arvo', 'Solu'])
        self.ui.rightTableWidget.setHorizontalHeaderLabels(
            ['Nimi', 'Arvo', 'Solu'])

        self.ui.leftTableWidget.setAlternatingRowColors(True)
        self.ui.rightTableWidget.setAlternatingRowColors(True)

        # populate tables
        for index, result in enumerate(self.db.leftResults):
            self.ui.leftTableWidget.setItem(
                index, 0, QTableWidgetItem(result.name))
            self.ui.leftTableWidget.setItem(
                index, 2, QTableWidgetItem(result.cell))

        for index, result in enumerate(self.db.rightResults):
            self.ui.rightTableWidget.setItem(
                index, 0, QTableWidgetItem(result.name))
            self.ui.rightTableWidget.setItem(
                index, 2, QTableWidgetItem(result.cell))

        self.ui.leftTableWidget.itemChanged.connect(
            self.saveTableItem)
        self.ui.rightTableWidget.itemChanged.connect(
            self.saveTableItem)

        self.ui.inputFileLabel.setText(
            self.db.inputFile.split("/")[-1])
        self.ui.outputFileLabel.setText(
            self.db.outputFile.split("/")[-1])

    def saveTableItem(self, item):
        if not item.column() == 1:
            if "left" in item.tableWidget().objectName():
                if item.column() == 0:
                    self.db.leftResults[item.row()].name = item.text()
                elif item.column() == 2:
                    self.db.leftResults[item.row()].cell = item.text()
            else:
                if item.column() == 0:
                    self.db.rightResults[item.row()].name = item.text()
                elif item.column() == 2:
                    self.db.rightResults[item.row()].cell = item.text()
            self.db.freeze()

    def changeText(self, textInput):
        if textInput == self.ui.leftLNumberInput:
            self.db.leftLNumber.value = textInput.text()
        if textInput == self.ui.rightLNumberInput:
            self.db.rightTester.value = textInput.text()
        if textInput == self.ui.leftTesterInput:
            self.db.leftTester.value = textInput.text()
        if textInput == self.ui.rightTesterInput:
            self.db.rightTester.value = textInput.text()

    def showDevices(self):
        """
        list connected usb devices
        """

        for index, device in enumerate(self.all_hids, 1):
            device_name = unicode("{0.vendor_name} {0.product_name}".format(
                device, device.vendor_id, device.product_id))
            self.ui.deviceBox.addItem(
                "{0} => {1}".format(index, device_name))

    def sendData(self):
        """
        configure data handler and send data
        """

        try:
            self.device.open()
            out_report = self.device.find_output_reports()[0]
            # set custom raw data handler
            self.device.set_raw_data_handler(self.sample_handler)

            while self.device.is_plugged():
                buffer = [0x00, 0x46, 0x30, 0x0d, 0x0a, 0x00, 0x00, 0x00, 0x00]
                out_report.set_raw_data(buffer)
                out_report.send()
                # just keep the device opened to receive events
                sleep(0.5)
        # wrong input device
        except Exception as e:
            self.ui.measurementLabel.setText("Ei signaalia")
            self.currentMeasurement = None
            self.ui.lcdNumber.display(0)
            self.ui.leftMonitorLabel.setText("VASEN MONITORI")
            self.ui.rightMonitorLabel.setText("OIKEA MONITORI")
            print(str(e))
            # popup: No input data, try another device
        self.device.close()

    def selectDevice(self, selection):
        # if another device is open, close it
        if self.device:
            self.device.close()

        self.device = self.all_hids[selection]

        # use worker class to send data to handler in another thread
        self.worker = Worker(self.sendData)
        self.threadpool.start(self.worker)

        self.setFocus()

    def sample_handler(self, data):
        """
        receive and handle incoming data from device
        """

        # if all measurements taken, format excel and exit program
        if self.currentIndex >= len(self.db.results):
            return

        try:
            # format value to string #.########
            self.rawValue = chr(data[2]) + "." + \
                chr(data[4]) + \
                chr(data[5]) + \
                chr(data[6]) + \
                chr(data[7]) + \
                chr(data[8]) + \
                chr(data[9]) + \
                chr(data[10]) + \
                chr(data[11])
            self.currentMeasurement = "{:.3f}".format(
                round(float(self.rawValue), 3))

            self.ui.lcdNumber.display(self.currentMeasurement)

            self.ui.measurementLabel.setText(
                self.db.results[self.currentIndex].name)

            if self.currentIndex < len(self.db.leftResults):
                self.ui.leftMonitorLabel.setText(
                    self.db.results[self.currentIndex].name)
                self.ui.rightMonitorLabel.setText("OIKEA MONITORI")
            else:
                self.ui.leftMonitorLabel.setText("VASEN MONITORI")
                self.ui.rightMonitorLabel.setText(
                    self.db.results[self.currentIndex].name)
        except Exception as e:
            print(str(e))

    def addResult(self):
        if self.currentMeasurement:
            if self.currentIndex < len(self.db.leftResults):
                self.ui.leftTableWidget.setItem(
                    self.currentIndex, 1, QTableWidgetItem(self.currentMeasurement))
                self.setMonitor("left")
            else:
                self.ui.rightTableWidget.setItem(
                    self.currentIndex - len(self.db.leftResults), 1, QTableWidgetItem(self.currentMeasurement))
                self.setMonitor("right")

            try:
                self.db.results[self.currentIndex].value = self.rawValue
                self.currentIndex = self.currentIndex + 1

                self.ui.progressBar.setValue(
                    self.currentIndex / len(self.db.results) * 100)
            except IndexError as e:
                print(str(e))

            if self.currentIndex >= len(self.db.results):
                self.ui.measurementLabel.setText("Valmis")
                self.ui.leftMonitorLabel.setText("VASEN MONITORI")
                self.ui.rightMonitorLabel.setText("OIKEA MONITORI")
                self.saveData()

    def removeResult(self):
        if self.currentIndex > 0:
            if self.currentIndex - 1 < len(self.db.leftResults):
                item = self.ui.leftTableWidget.takeItem(
                    self.currentIndex - 1, 1)
                self.setMonitor("left")
            else:
                item = self.ui.rightTableWidget.takeItem(
                    self.currentIndex - 1 - len(self.db.leftResults), 1)
                self.setMonitor("right")
            del item

            try:
                self.db.results[self.currentIndex - 1].value = ""
            except KeyError:
                pass

            self.currentIndex = self.currentIndex - 1

            self.ui.progressBar.setValue(
                self.currentIndex / len(self.db.results) * 100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            python = sys.executable
            os.execl(python, python, * sys.argv)
        if event.key() == Qt.Key_Return:
            self.addResult()
        if event.key() == Qt.Key_Backspace:
            self.removeResult()
        if event.key() == Qt.Key_Escape:
            self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWindow()
    window.configure()
    window.showDevices()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # first be kind with local encodings
    # allow to show encoded strings
    if sys.version_info < (3,):
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    # as is, don't handle unicodes
    else:
        unicode = str
        raw_input = input
    main()
