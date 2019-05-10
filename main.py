from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui import Ui_MainWindow
import os
import sys
import warnings
import signal
import shelve
from time import sleep
from msvcrt import kbhit
from openpyxl import load_workbook
from pywinusb import hid
from win32com import client
from shutil import copyfile
shell = client.Dispatch("WScript.Shell")


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)
        print("Thread start")
        sleep(5)
        print("Thread complete")


class MainWindow(QMainWindow):
    def __init__(self):
        self.i = 0
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.forwardButton.clicked.connect(self.addResult)
        self.ui.backwardButton.clicked.connect(self.removeResult)
        self.all_hids = hid.find_all_hid_devices()
        self.showDevices()
        self.ui.deviceBox.activated.connect(self.selectDevice)
        self.currentIndex = 0
        # TODO enable user to use differen configuration
        self.excelInputFile = "C:/Mittaus/mittaus.xlsm"
        self.excelOutputFile = "C:/Mittaus/output.xlsm"
        self.shelfFile = "default"
        self.mittaukset = [
            "Vasen L1",
            "Vasen L2",
            "Vasen L3",
            "Vasen L4",
            "Vasen L5",
            "Vasen L6",
            "Vasen L7",
            "Vasen L8",
            "Vasen L9",
            "Vasen L10",
            "Vasen L11",
            "Vasen L12",
            "Vasen L13",
            "Vasen L14",
            "Vasen L15",
            "Vasen L16",
            "Vasen L17",
            "Vasen L18",
            "Vasen TT K",
            "Vasen TT OY",
            "Vasen TT VY",
            "Vasen TT OA",
            "Vasen TT VA",
            "Vasen KT K",
            "Vasen KT OY",
            "Vasen KT VY",
            "Vasen KT OA",
            "Vasen KT VA",
            "Oikea L1",
            "Oikea L2",
            "Oikea L3",
            "Oikea L4",
            "Oikea L5",
            "Oikea L6",
            "Oikea L7",
            "Oikea L8",
            "Oikea L9",
            "Oikea L10",
            "Oikea L11",
            "Oikea L12",
            "Oikea L13",
            "Oikea L14",
            "Oikea L15",
            "Oikea L16",
            "Oikea L17",
            "Oikea L18",
            "Oikea TT K",
            "Oikea TT OY",
            "Oikea TT VY",
            "Oikea TT OA",
            "Oikea TT VA",
            "Oikea KT K",
            "Oikea KT OY",
            "Oikea KT VY",
            "Oikea KT OA",
            "Oikea KT VA"
        ]
        self.threadpool = QThreadPool()
        self.device = None

    def showDevices(self):
        for index, device in enumerate(self.all_hids, 1):
            device_name = unicode("{0.vendor_name} {0.product_name}".format(
                device, device.vendor_id, device.product_id))
            self.ui.deviceBox.addItem(
                "{0} => {1}".format(index, device_name))

    def sendData(self):
        try:
            self.device.open()
            out_report = self.device.find_output_reports()
            # set custom raw data handler
            self.device.set_raw_data_handler(self.sample_handler)

            self.ui.label.setText("Odotetaan dataa...")

            while self.device.is_plugged():
                buffer = [0x00, 0x46, 0x30, 0x0d,
                          0x0a, 0x00, 0x00, 0x00, 0x00]
                out_report[0].set_raw_data(buffer)
                out_report[0].send()
                # just keep the device opened to receive events
                sleep(0.5)
            self.device.close()

        except Exception as e:
            print(self.device)
            print(str(e))
            self.ui.label.setText("No input data")

    def selectDevice(self, selection):
        if self.device:
            self.device.close()
        self.ui.label.setText("xxx")
        self.device = self.all_hids[selection]

        worker = Worker(self.sendData)
        self.threadpool.start(worker)

    def formatShelf(self):
        """
        format shelf and clear values
        """

        for index, mittaus in enumerate(self.mittaukset):
            if index < 18:
                cell = "B%d" % (index + 21)
            elif index >= 18 and index < 23:
                cell = "B%d" % (index + 31)
            elif index >= 23 and index < 28:
                cell = "B%d" % (index + 34)
            elif index >= 28 and index < 46:
                cell = "F%d" % (index - 7)
            elif index >= 46 and index < 51:
                cell = "F%d" % (index + 3)
            elif index >= 51 and index < 56:
                cell = "F%d" % (index + 6)

            measurements = shelve.open(self.shelfFile)
            temp = measurements[str(index)]
            temp = {"name": mittaus, "value": None, "cell": cell}
            measurements[str(index)] = temp
            measurements.close()

    def sample_handler(self, data):
        """
        receive and handle incoming data from device
        """

        # format value to string #.########
        value = chr(data[2]) + "." + \
            chr(data[4]) + \
            chr(data[5]) + \
            chr(data[6]) + \
            chr(data[7]) + \
            chr(data[8]) + \
            chr(data[9]) + \
            chr(data[10]) + \
            chr(data[11])

        try:
            # if all measurements taken, format excel and exit program
            # if self.currentIndex == len(measurements):
            if self.currentIndex == 3:
                # suppress excel warnings
                warnings.filterwarnings("ignore")

                # make a copy of base excel file
                copyfile(self.excelInputFile, self.excelOutputFile)

                workbook = load_workbook(self.excelOutputFile, keep_vba=True)
                worksheet = workbook.active

                measurements = shelve.open(self.shelfFile)

                # input measurements
                for measurement in measurements:
                    if measurements[str(measurement)]["value"] != None:
                        worksheet[measurements[str(measurement)]["cell"]] = float(
                            measurements[str(measurement)]["value"])

                # save excel
                workbook.save(self.excelOutputFile)

                measurements.close()

                sleep(1)
                os.startfile(self.excelOutputFile)
                sleep(1)
                # TODO focus on excel
                # shell.SendKeys("%{F4}", 0)
                shell.SendKeys("{ENTER}", 0)
                sleep(1)
                shell.SendKeys("%", 0)
                sleep(0.1)
                shell.SendKeys("o", 0)
                sleep(0.1)
                shell.SendKeys("u", 0)
                sleep(0.1)
                shell.SendKeys("m", 0)
                sleep(0.1)
                shell.SendKeys("p", 0)
                sleep(0.1)
                shell.SendKeys("p", 0)
                sleep(0.1)
                shell.SendKeys("{ENTER}", 0)
                sleep(0.1)
                shell.SendKeys("^+f", 0)
                sleep(0.1)
                shell.SendKeys("{F2}", 0)
                sleep(0.1)
                shell.SendKeys("+{HOME}", 0)
                sleep(0.1)
                shell.SendKeys("^c", 0)
                sleep(0.1)
                shell.SendKeys("{ESC}", 0)
                sleep(0.1)
                shell.SendKeys("%", 0)
                sleep(0.1)
                shell.SendKeys("o", 0)
                sleep(0.1)
                shell.SendKeys("u", 0)
                sleep(0.1)
                shell.SendKeys("m", 0)
                sleep(0.1)
                shell.SendKeys("u", 0)
                sleep(0.1)
                shell.SendKeys("{ENTER}", 0)
                sleep(0.1)
                shell.SendKeys("{F12}", 0)
                sleep(2)
                shell.SendKeys("^v", 0)
                sleep(0.1)
                shell.SendKeys("{ENTER}", 0)
                sleep(0.1)
                shell.SendKeys("^g", 0)
                sleep(0.1)
                shell.SendKeys("A", 0)
                # sleep(0.1)
                shell.SendKeys("9", 0)
                # sleep(0.1)
                shell.SendKeys("9", 0)
                # sleep(0.1)
                shell.SendKeys("{ENTER}", 0)
                sleep(0.1)
                shell.SendKeys("^g", 0)
                sleep(0.1)
                shell.SendKeys("h", 0)
                # sleep(0.1)
                shell.SendKeys("6", 0)
                # sleep(0.1)
                shell.SendKeys("5", 0)
                # sleep(0.1)
                shell.SendKeys("{ENTER}", 0)
                sleep(0.1)
                shell.SendKeys("{F2}", 0)
                sleep(0.1)
                shell.AppActivate('Get Value 0.5')
                sleep(0.1)
                print("Done!")
                sleep(0.1)
                self.close()

            # if user has pressed enter, save measurement
            elif kbhit():
                measurements = shelve.open(self.shelfFile)

                sys.stdout.flush()
                prompt = "\r" + str(round(float(value), 3)
                                    ).ljust(5, "0") + "\t" + measurements[str(self.currentIndex)]["name"] + "\t" + "Tallennettu"
                raw_input(prompt)

                # update value of measurement
                measurement = measurements[str(self.currentIndex)]
                measurement["value"] = value
                measurements[str(self.currentIndex)] = measurement

                measurements.close()

                self.currentIndex = self.currentIndex + 1

            # show updated measurement
            else:
                measurements = shelve.open(self.shelfFile)
                measurement = str(round(float(value), 3)
                                  ).ljust(5, "0") + "\t" + measurements[str(self.currentIndex)]["name"]
                self.ui.label.setText(measurement)
                measurements.close()

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

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        event.accept()

    def addResult(self):
        value = "hello world"
        self.ui.measurementList.addItem(value + " " + str(self.i))
        self.i = self.i + 1

    def removeResult(self):
        if self.i > 0:
            item = self.ui.measurementList.takeItem(
                len(self.ui.measurementList) - 1)
            del item
            self.i = self.i - 1

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.addResult()
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Backspace:
            self.removeResult()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
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
