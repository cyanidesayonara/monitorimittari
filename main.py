from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui import Ui_MainWindow
import os
import sys
import warnings
import signal
import json
from time import sleep
from openpyxl import load_workbook
from pywinusb import hid
from win32com import client
from shutil import copyfile
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
        self.ui.forwardButton.clicked.connect(self.addResult)
        self.ui.backwardButton.clicked.connect(self.removeResult)
        self.ui.deviceBox.activated.connect(self.selectDevice)
        self.all_hids = hid.find_all_hid_devices()
        self.currentIndex = 0
        # self.ui.monitorLineEdit_1.textChanged.connect()
        self.threadpool = QThreadPool()
        self.mappings = {}
        self.settings = {}
        self.device = None
        self.currentMeasurement = None
        self.rawValue = None

    def setup(self):
        with open("setup.json") as f:
            self.settings = json.loads(f.read())

        with open(self.settings["mappings"]) as f:
            self.mappings = json.loads(f.read())

        self.measurements = self.mappings["left"]["measurements"] + \
            self.mappings["right"]["measurements"]

        self.ui.tableWidgetLeft.setRowCount(len(self.measurements) / 2)
        self.ui.tableWidgetRight.setRowCount(len(self.measurements) / 2)
        self.ui.tableWidgetLeft.setHorizontalHeaderLabels(
            ['Name', 'Value', 'Cell'])
        self.ui.tableWidgetRight.setHorizontalHeaderLabels(
            ['Name', 'Value', 'Cell'])

    def formatExcel(self):
        try:
            # suppress excel warnings
            warnings.filterwarnings("ignore")

            # make a copy of base excel file
            copyfile(self.settings.excelInputFile,
                     self.settings.excelOutputFile)

            # load workbook and activate worksheet
            workbook = load_workbook(
                self.settings.excelOutputFile, keep_vba=True)
            worksheet = workbook.active

            # input measurements
            for measurement in self.measurements:
                worksheet[measurement["cell"]] = float(measurement["value"])

            # save excel
            workbook.save(self.excelOutputFile)

            # sleep(1)
            # os.startfile(self.excelOutputFile)
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
            # print("Done!")
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
            self.currentMeasurement = str(
                round(float(self.rawValue), 3))

            self.ui.lcdNumber.display(self.currentMeasurement)
            self.ui.measurementLabel.setText(
                self.measurements[self.currentIndex]["name"])
        except Exception as e:
            print(str(e))

    def addResult(self):
        if self.currentMeasurement:
            if self.currentIndex < len(self.measurements) / 2:
                self.ui.resultList_1.addItem(self.currentMeasurement)
            else:
                self.ui.resultList_2.addItem(self.currentMeasurement)

            self.currentIndex = self.currentIndex + 1
            self.currentMeasurement = None

    def removeResult(self):
        if self.currentIndex > 0:
            if self.currentIndex <= len(self.measurements) / 2:
                item = self.ui.resultList_1.takeItem(
                    len(self.ui.resultList_1) - 1)
            else:
                item = self.ui.resultList_2.takeItem(
                    len(self.ui.resultList_2) - 1)
            del item

            self.currentIndex = self.currentIndex - 1
            self.currentMeasurement = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.addResult()
        if event.key() == Qt.Key_Backspace:
            self.removeResult()
        if event.key() == Qt.Key_Escape:
            self.close()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setup()
    window.showDevices()
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
