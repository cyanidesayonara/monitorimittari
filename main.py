from shutil import copyfile
from win32com import client
from pywinusb import hid
from openpyxl import load_workbook
from time import sleep
import styles
from config import backupConfig
import json
import warnings
import sys
import os
from ui import Ui_MainWindow
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot, QRect, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QStyleFactory, QPushButton
from PyQt5.QtGui import QIcon
shell = client.Dispatch("WScript.Shell")


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
        self.setWindowIcon(QIcon("./" + "icon.png"))
        self.ui.forwardButton.clicked.connect(self.addResult)
        self.ui.backwardButton.clicked.connect(self.removeResult)
        self.ui.leftMonitorSelect.clicked.connect(
            lambda: self.setMonitor("left"))
        self.ui.rightMonitorSelect.clicked.connect(
            lambda: self.setMonitor("right"))
        self.ui.deviceBox.activated.connect(self.selectDevice)
        self.all_hids = hid.find_all_hid_devices()
        self.currentIndex = 0
        self.ui.leftLNumberInput.textEdited.connect(
            lambda: self.changeText(self.ui.leftLNumberInput))
        self.ui.rightLNumberInput.textEdited.connect(
            lambda: self.changeText(self.ui.rightLNumberInput))
        self.ui.lightThemeButton.toggled.connect(
            lambda: self.setTheme("light"))
        self.ui.darkThemeButton.toggled.connect(
            lambda: self.setTheme("dark"))
        self.threadpool = QThreadPool()
        self.mappings = {}
        self.config = {}
        self.device = None
        self.currentMeasurement = None
        self.rawValue = None

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
            stylesheet = styles.base + styles.dark
            self.config["theme"] = "dark"
        else:
            stylesheet = styles.base + styles.light
            self.config["theme"] = "light"
        self.setStyleSheet(stylesheet)

    def configure(self):
        configFile = "config.json"

        # if config file doesn't exist, create it from backup
        if not os.path.isfile(configFile):
            with open(configFile, "w+") as f:
                f.write(json.dumps(backupConfig))

        # open and load config
        with open(configFile) as f:
            self.config = json.loads(f.read())

        theme = self.config["theme"]
        self.setTheme(theme)
        self.setMonitor("left")

        if theme == "dark":
            self.ui.darkThemeButton.setChecked(True)
        else:
            self.ui.lightThemeButton.setChecked(True)

        # set mappings
        self.mappings = self.config[self.config["mappings"]]

        # set measurements
        self.measurements = self.mappings["left"]["measurements"] + \
            self.mappings["right"]["measurements"]

        # config tables
        self.ui.leftTableWidget.setRowCount(len(self.measurements) / 2)
        self.ui.rightTableWidget.setRowCount(len(self.measurements) / 2)
        self.ui.leftTableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.leftTableWidget.setHorizontalHeaderLabels(
            ['Nimi', 'Arvo', 'Solu'])
        self.ui.rightTableWidget.setHorizontalHeaderLabels(
            ['Nimi', 'Arvo', 'Solu'])
        # self.ui.leftTableWidget.setGeometry(
        #     self.left, self.top, self.width, self.height)
        # self.ui.leftTableWidget.setGeometry(
        #     self.ui.left, self.ui.top, self.ui.width, len(self.measurements) / 2 * 21)
        self.ui.leftTableWidget.setAlternatingRowColors(True)
        self.ui.rightTableWidget.setAlternatingRowColors(True)

        # populate tables
        for index, measurement in enumerate(self.mappings["left"]["measurements"]):
            self.ui.leftTableWidget.setItem(
                index, 0, QTableWidgetItem(measurement["name"]))
            self.ui.leftTableWidget.setItem(
                index, 2, QTableWidgetItem(measurement["cell"]))

        for index, measurement in enumerate(self.mappings["right"]["measurements"]):
            self.ui.rightTableWidget.setItem(
                index, 0, QTableWidgetItem(measurement["name"]))
            self.ui.rightTableWidget.setItem(
                index, 2, QTableWidgetItem(measurement["cell"]))

    def changeText(self, textInput):
        if textInput == self.ui.leftLNumberInput:
            self.mappings["left"]["monitor"]["value"] = textInput.text()
        if textInput == self.ui.rightLNumberInput:
            self.mappings["right"]["monitor"]["value"] = textInput.text()

    def formatExcel(self):
        try:
            # suppress excel warnings
            warnings.filterwarnings("ignore")

            # make a copy of base excel file
            copyfile(self.config["excelInputFile"],
                     self.config["excelOutputFile"])

            # load workbook and activate worksheet
            workbook = load_workbook(
                self.config["excelOutputFile"], keep_vba=True)
            worksheet = workbook.active

            worksheet[self.mappings["left"]["monitor"]["cell"]
                      ] = self.mappings["left"]["monitor"]["value"]

            worksheet[self.mappings["right"]["monitor"]["cell"]
                      ] = self.mappings["right"]["monitor"]["value"]

            # input measurements
            for measurement in self.measurements:
                worksheet[measurement["cell"]] = float(measurement["value"])

            # save excel
            workbook.save(self.config["excelOutputFile"])

            # sleep(1)
            # os.startfile(self.config["excelOutputFile"])
            # sleep(1)
            # # TODO focus on excel
            # # shell.SendKeys("%{F4}", 0)
            # shell.SendKeys("{ENTER}", 0)
            # sleep(1)
            # shell.SendKeys("%", 0)
            # sleep(0.1)
            # shell.SendKeys("o", 0)
            # sleep(0.1)
            # shell.SendKeys("u", 0)
            # sleep(0.1)
            # shell.SendKeys("m", 0)
            # sleep(0.1)
            # shell.SendKeys("p", 0)
            # sleep(0.1)
            # shell.SendKeys("p", 0)
            # sleep(0.1)
            # shell.SendKeys("{ENTER}", 0)
            # sleep(0.1)
            # shell.SendKeys("^+f", 0)
            # sleep(0.1)
            # shell.SendKeys("{F2}", 0)
            # sleep(0.1)
            # shell.SendKeys("+{HOME}", 0)
            # sleep(0.1)
            # shell.SendKeys("^c", 0)
            # sleep(0.1)
            # shell.SendKeys("{ESC}", 0)
            # sleep(0.1)
            # shell.SendKeys("%", 0)
            # sleep(0.1)
            # shell.SendKeys("o", 0)
            # sleep(0.1)
            # shell.SendKeys("u", 0)
            # sleep(0.1)
            # shell.SendKeys("m", 0)
            # sleep(0.1)
            # shell.SendKeys("u", 0)
            # sleep(0.1)
            # shell.SendKeys("{ENTER}", 0)
            # sleep(0.1)
            # shell.SendKeys("{F12}", 0)
            # sleep(2)
            # shell.SendKeys("^v", 0)
            # sleep(0.1)
            # shell.SendKeys("{ENTER}", 0)
            # sleep(0.1)
            # shell.SendKeys("^g", 0)
            # sleep(0.1)
            # shell.SendKeys("A", 0)
            # # sleep(0.1)
            # shell.SendKeys("9", 0)
            # # sleep(0.1)
            # shell.SendKeys("9", 0)
            # # sleep(0.1)
            # shell.SendKeys("{ENTER}", 0)
            # sleep(0.1)
            # shell.SendKeys("^g", 0)
            # sleep(0.1)
            # shell.SendKeys("h", 0)
            # # sleep(0.1)
            # shell.SendKeys("6", 0)
            # # sleep(0.1)
            # shell.SendKeys("5", 0)
            # # sleep(0.1)
            # shell.SendKeys("{ENTER}", 0)
            # sleep(0.1)
            # shell.SendKeys("{F2}", 0)
            # sleep(0.1)
            # shell.AppActivate('Get Value 0.5')
            # sleep(0.1)
            print("Done!")
        # if file is used by another process
        except PermissionError as e:
            print(e)
            print(
                "Excel-tiedosto on auki toisessa ikkunassa. Ole hyvä ja sulje tiedosto.")
            self.close()
        # if base excel file doesn't exist
        except FileNotFoundError as e:
            print(e)
            print(
                "Excel-tiedostoa ei löydy. Ole hyvä ja valitse tiedosto uudelleen.")
            self.close()

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

            # pop-up: waiting for data

            while self.device.is_plugged():
                buffer = [0x00, 0x46, 0x30, 0x0d, 0x0a, 0x00, 0x00, 0x00, 0x00]
                out_report.set_raw_data(buffer)
                out_report.send()
                # just keep the device opened to receive events
                sleep(0.5)
        # wrong input device
        except Exception as e:
            print(str(e))
            # popup: No input data, try another device
        self.device.close()

    def selectDevice(self, selection):
        # if another device is open, close it
        if self.device:
            self.device.close()

        self.device = self.all_hids[selection]

        # use worker class to send data to handler in another thread
        worker = Worker(self.sendData)
        self.threadpool.start(worker)

    def sample_handler(self, data):
        """
        receive and handle incoming data from device
        """

        # if all measurements taken, format excel and exit program
        if self.currentIndex == len(self.measurements):
            self.formatExcel()
            self.close()

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
                self.measurements[self.currentIndex]["name"])
        except Exception as e:
            print(str(e))

    def addResult(self):
        if self.currentMeasurement:
            if self.currentIndex < len(self.measurements) / 2:
                self.ui.leftTableWidget.setItem(
                    self.currentIndex, 1, QTableWidgetItem(self.currentMeasurement))
                self.setMonitor("left")
            else:
                self.ui.rightTableWidget.setItem(
                    self.currentIndex - len(self.measurements) / 2, 1, QTableWidgetItem(self.currentMeasurement))
                self.setMonitor("right")

            self.measurements[self.currentIndex]["value"] = self.rawValue
            self.currentIndex = self.currentIndex + 1
            self.currentMeasurement = None
            self.ui.progressBar.setValue(
                self.currentIndex / len(self.measurements) * 100)

    def removeResult(self):
        if self.currentIndex > 0:
            if self.currentIndex <= len(self.measurements) / 2:
                item = self.ui.leftTableWidget.takeItem(
                    self.currentIndex - 1, 1)
                self.setMonitor("left")
            else:
                item = self.ui.rightTableWidget.takeItem(
                    self.currentIndex - 1 - len(self.measurements) / 2, 1)
                self.setMonitor("right")
            del item

            del self.measurements[self.currentIndex - 1]["value"]
            self.currentIndex = self.currentIndex - 1
            self.currentMeasurement = None
            self.ui.progressBar.setValue(
                self.currentIndex / len(self.measurements) * 100)

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
