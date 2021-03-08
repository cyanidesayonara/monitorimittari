import os
import sys
import json
import warnings
import datetime
from time import sleep
from shutil import copyfile
from pywinusb import hid
from editpyxl import Workbook
from win32com import client
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
from defaults import defaults
from repository import Repository, CONFIG_FILE
import styles
shell = client.Dispatch("WScript.Shell")

RESULTS_FOLDER = "C:/Mittaus"


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
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon_path = resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.ui.messageBox = QMessageBox(self.ui.centralwidget)
        self.ui.messageBox.setWindowTitle(" ")
        self.all_hids = hid.find_all_hid_devices()
        self.current_index = 0

        # selects
        self.ui.deviceBox.activated.connect(self.select_device)

        # buttons
        self.ui.forwardButton.clicked.connect(self.add_result)
        self.ui.backwardButton.clicked.connect(self.remove_result)
        self.ui.leftMonitorSelect.clicked.connect(lambda: self.set_monitor("left"))
        self.ui.rightMonitorSelect.clicked.connect(lambda: self.set_monitor("right"))
        self.ui.lightThemeButton.clicked.connect(lambda: self.set_theme("light"))
        self.ui.darkThemeButton.clicked.connect(lambda: self.set_theme("dark"))
        self.ui.prideThemeButton.clicked.connect(lambda: self.set_theme("pride"))
        self.ui.saveButton.clicked.connect(self.save_data)
        self.ui.inputFileButton.clicked.connect(self.choose_input_file)
        self.ui.outputFileButton.clicked.connect(self.choose_output_file)
        self.ui.inputFileButton.setStyleSheet('text-align:left;padding:5px;')
        self.ui.outputFileButton.setStyleSheet('text-align:left;padding:5px;')
        self.ui.resetButton.clicked.connect(self.reset_values)
        self.ui.restoreButton.clicked.connect(self.restore_config)

        # inputs
        self.ui.leftLNumberInput.textEdited.connect(lambda: self.change_text(self.ui.leftLNumberInput))
        self.ui.rightLNumberInput.textEdited.connect(lambda: self.change_text(self.ui.rightLNumberInput))
        self.ui.leftLNumberInput.textEdited.connect(self.change_output_filename)
        self.ui.rightLNumberInput.textEdited.connect(self.change_output_filename)
        self.ui.leftTesterInput.textEdited.connect(lambda: self.change_text(self.ui.leftTesterInput))
        self.ui.rightTesterInput.textEdited.connect(lambda: self.change_text(self.ui.rightTesterInput))

        self.thread_pool = QThreadPool()
        self.worker = None
        self.repository = None
        self.device = None
        self.current_measurement = None
        self.raw_value = None

    def configure(self):
        self.repository = Repository()
        self.set_theme(self.repository.theme)
        self.set_monitor("left")
        self.set_save_button_disabled()

        # config tables
        self.ui.leftTableWidget.setRowCount(len(self.repository.left_results))
        self.ui.rightTableWidget.setRowCount(len(self.repository.right_results))
        self.ui.rightTableWidget.clicked.connect(self.set_current_index)
        self.ui.leftTableWidget.clicked.connect(self.set_current_index)
        self.ui.leftTableWidget.setHorizontalHeaderLabels(['Nimi', 'Arvo', 'Solu'])
        self.ui.rightTableWidget.setHorizontalHeaderLabels(['Nimi', 'Arvo', 'Solu'])
        self.ui.leftTableWidget.setAlternatingRowColors(True)
        self.ui.rightTableWidget.setAlternatingRowColors(True)

        # populate tables
        for index, result in enumerate(self.repository.left_results):
            self.ui.leftTableWidget.setItem(index, 0, QTableWidgetItem(result.name))
            self.ui.leftTableWidget.setItem(index, 2, QTableWidgetItem(result.cell))

        for index, result in enumerate(self.repository.right_results):
            self.ui.rightTableWidget.setItem(index, 0, QTableWidgetItem(result.name))
            self.ui.rightTableWidget.setItem(index, 2, QTableWidgetItem(result.cell))

        self.ui.leftTableWidget.itemChanged.connect(self.save_table_item)
        self.ui.rightTableWidget.itemChanged.connect(self.save_table_item)

        if self.repository.input_file and os.path.isfile(self.repository.input_file):
            self.ui.inputFileButton.setText(self.repository.input_file)

    def restore_config(self):
        with open(CONFIG_FILE, "w+") as file:
            file.write(json.dumps(defaults, indent=2))
        self.configure()

    def reset_values(self):
        for index, result in enumerate(self.repository.results):
            if index < len(self.repository.left_results):
                item = self.ui.leftTableWidget.takeItem(index, 1)
            else:
                item = self.ui.rightTableWidget.takeItem(index - len(self.repository.left_results), 1)
            del item

            try:
                result.value = ""
            except KeyError:
                pass

        self.current_index = 0
        self.ui.progressBar.setValue(self.current_index / len(self.repository.results) * 100)
        self.set_monitor("left")

    def choose_input_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "", RESULTS_FOLDER, "Excel file(*.xls *.xlsx *.xlsm)", options=options)
        if file_name:
            self.ui.inputFileButton.setText(file_name)
            self.repository.input_file = file_name
            self.repository.freeze()
            self.set_save_button_disabled()

    def choose_output_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self, "", RESULTS_FOLDER, "Excel file(*.xls *.xlsx *.xlsm)", options=options)
        if file_name:
            if "." not in file_name:
                file_name = file_name + ".xlsx"
            elif not file_name.split(".")[-1] == "xlsx":
                file_name = ".".join(file_name.split(".")[:-1] + ["xlsx"])
            self.ui.outputFileButton.setText(file_name)
            self.repository.output_file = file_name
            self.set_save_button_disabled()

    def save_data(self):
        try:
            # suppress excel warnings
            warnings.filterwarnings("ignore")

            # make a copy of base excel file
            copyfile(self.repository.input_file, self.repository.output_file)

            # load workbook and activate worksheet
            workbook = Workbook()
            workbook.open(self.repository.output_file)
            worksheet = workbook.active

            if self.repository.left_l_number.value:
                worksheet.cell(self.repository.left_l_number.cell).value = str(self.repository.left_l_number.value)

            if self.repository.right_l_number.value:
                worksheet.cell(self.repository.right_l_number.cell).value = str(self.repository.right_l_number.value)

            if self.repository.left_tester.value:
                worksheet.cell(self.repository.left_tester.cell).value = str(self.repository.left_tester.value)

            if self.repository.right_tester.value:
                worksheet.cell(self.repository.right_tester.cell).value = str(self.repository.right_tester.value)

            # input measurements
            for result in self.repository.results:
                if result.value:
                    worksheet[result.cell] = float(result.value)

            # save excel
            workbook.save(self.repository.output_file)
            workbook.close()

            self.ui.messageBox.setText("Tallennettu tiedostoon {0}.".format(self.repository.output_file))
            self.ui.messageBox.show()

        # if file is used by another process
        except PermissionError:
            self.ui.messageBox.setText("Excel-tiedosto on auki toisessa ikkunassa. Ole hyvä ja sulje tiedosto.")
            self.ui.messageBox.show()
        # if base excel file doesn't exist
        except FileNotFoundError:
            self.ui.messageBox.setText("Excel-tiedostoa ei löydy. Ole hyvä ja valitse tiedosto uudelleen.")
            self.ui.messageBox.show()

    def set_monitor(self, monitor):
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

    def set_theme(self, theme):
        if theme == "dark":
            self.ui.darkThemeButton.setChecked(True)
            stylesheet = styles.base + styles.dark
        elif theme == "pride":
            self.ui.prideThemeButton.setChecked(True)
            stylesheet = styles.base + styles.pride
        else:
            self.ui.lightThemeButton.setChecked(True)
            stylesheet = styles.base + styles.light
        self.setStyleSheet(stylesheet)
        self.repository.theme = theme
        self.repository.freeze()

    def set_current_index(self, row):
        if self.ui.leftMonitorSelect.isChecked():
            self.current_index = row.row()
        else:
            self.current_index = row.row() + len(self.repository.left_results)

    def set_save_button_disabled(self):
        if self.repository.input_file == "" or self.repository.output_file == "":
            self.ui.saveButton.setDisabled(True)
        else:
            self.ui.saveButton.setDisabled(False)

    def save_table_item(self, item):
        if not item.column() == 1:
            if "left" in item.tableWidget().objectName():
                if item.column() == 0:
                    self.repository.left_results[item.row()].name = item.text()
                elif item.column() == 2:
                    self.repository.left_results[item.row()].cell = item.text()
            else:
                if item.column() == 0:
                    self.repository.right_results[item.row()].name = item.text()
                elif item.column() == 2:
                    self.repository.right_results[item.row()].cell = item.text()
            self.repository.freeze()

    def change_output_filename(self):
        basename = "/".join(self.repository.input_file.split("/")[0:-1])

        if not basename:
            basename = RESULTS_FOLDER

        timestamp = datetime.datetime.now().strftime("%d%m%y")
        left_l_number = self.repository.left_l_number.value
        right_l_number = self.repository.right_l_number.value

        filename = basename + "/" + left_l_number

        if right_l_number:
            if left_l_number == right_l_number:
                filename = filename + "-" + right_l_number
            elif left_l_number[:-1] == right_l_number[:-1]:
                filename = filename + "-" + right_l_number[-1:]
            elif left_l_number[:-2] == right_l_number[:-2]:
                filename = filename + "-" + right_l_number[-2:]
            else:
                filename = filename + "-" + right_l_number

        filename = filename + "_" + timestamp + ".xlsx"

        self.ui.outputFileButton.setText(filename)
        self.repository.output_file = filename
        self.set_save_button_disabled()

    def change_text(self, text_input):
        if text_input == self.ui.leftLNumberInput:
            self.repository.left_l_number.value = text_input.text()
        if text_input == self.ui.rightLNumberInput:
            self.repository.right_l_number.value = text_input.text()
        if text_input == self.ui.leftTesterInput:
            self.repository.left_tester.value = text_input.text()
        if text_input == self.ui.rightTesterInput:
            self.repository.right_tester.value = text_input.text()

    def show_devices(self):
        """
        list connected usb devices
        """

        for index, device in enumerate(self.all_hids, 1):
            device_name = unicode("{0.vendor_name} {0.product_name}".format(device))
            self.ui.deviceBox.addItem("{0} => {1}".format(index, device_name))

    def send_data(self):
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
        except Exception as error:
            self.ui.measurementLabel.setText("Ei signaalia")
            self.current_measurement = None
            self.ui.lcdNumber.display(0)
            self.ui.leftMonitorLabel.setText("VASEN MONITORI")
            self.ui.rightMonitorLabel.setText("OIKEA MONITORI")
            print(str(error))
            # popup: No input data, try another device
        self.device.close()

    def select_device(self, selection):
        # if another device is open, close it
        if self.device:
            self.device.close()

        self.device = self.all_hids[selection]

        # use worker class to send data to handler in another thread
        self.worker = Worker(self.send_data)
        self.thread_pool.start(self.worker)

        self.setFocus()

    def sample_handler(self, data):
        """
        receive and handle incoming data from device
        """

        # if all measurements taken, format excel and exit program
        if self.current_index >= len(self.repository.results):
            return

        try:
            # format value to string #.########
            self.raw_value = chr(data[2]) + "." + \
                chr(data[4]) + \
                chr(data[5]) + \
                chr(data[6]) + \
                chr(data[7]) + \
                chr(data[8]) + \
                chr(data[9]) + \
                chr(data[10]) + \
                chr(data[11])
            self.current_measurement = "{:.3f}".format(round(float(self.raw_value), 3))

            self.ui.lcdNumber.display(self.current_measurement)

            self.measuring_animation()

            if self.current_index < len(self.repository.left_results):
                self.ui.leftMonitorLabel.setText(self.repository.results[self.current_index].name)
                self.ui.rightMonitorLabel.setText("OIKEA MONITORI")
            else:
                self.ui.leftMonitorLabel.setText("VASEN MONITORI")
                self.ui.rightMonitorLabel.setText(self.repository.results[self.current_index].name)
        except Exception as error:
            print(str(error))

    def measuring_animation(self):
        if self.ui.measurementLabel.text() == "Mitataan":
            self.ui.measurementLabel.setText("Mitataan.")
        if self.ui.measurementLabel.text() == "Mitataan.":
            self.ui.measurementLabel.setText("Mitataan..")
        elif self.ui.measurementLabel.text() == "Mitataan..":
            self.ui.measurementLabel.setText("Mitataan...")
        else:
            self.ui.measurementLabel.setText("Mitataan")

    def add_result(self):
        if self.current_measurement:
            if self.current_index < len(self.repository.left_results):
                self.ui.leftTableWidget.setItem(
                    self.current_index, 1, QTableWidgetItem(self.current_measurement))
                self.set_monitor("left")
            else:
                self.ui.rightTableWidget.setItem(
                    self.current_index - len(self.repository.left_results), 1, QTableWidgetItem(
                        self.current_measurement))
                self.set_monitor("right")

            try:
                self.repository.results[self.current_index].value = self.raw_value
                self.current_index = self.current_index + 1

                self.ui.progressBar.setValue(self.current_index / len(self.repository.results) * 100)
            except IndexError as error:
                print(str(error))

            if self.current_index >= len(self.repository.results):
                self.ui.measurementLabel.setText("Valmis")
                self.ui.leftMonitorLabel.setText("VASEN MONITORI")
                self.ui.rightMonitorLabel.setText("OIKEA MONITORI")
                self.save_data()

    def remove_result(self):
        if self.current_index > 0:
            if self.current_index - 1 < len(self.repository.left_results):
                item = self.ui.leftTableWidget.takeItem(self.current_index - 1, 1)
                self.set_monitor("left")
            else:
                item = self.ui.rightTableWidget.takeItem(
                    self.current_index - 1 - len(self.repository.left_results), 1)
                self.set_monitor("right")
            del item

            try:
                self.repository.results[self.current_index - 1].value = ""
            except KeyError:
                pass

            self.current_index = self.current_index - 1

            self.ui.progressBar.setValue(self.current_index / len(self.repository.results) * 100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            python = sys.executable
            os.execl(python, python, * sys.argv)
        if event.key() == Qt.Key_Return:
            self.add_result()
        if event.key() == Qt.Key_Backspace:
            self.remove_result()
        if event.key() == Qt.Key_Escape:
            self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWindow()
    window.configure()
    window.show_devices()
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
