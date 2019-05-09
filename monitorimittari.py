from PyQt5 import QtCore, QtGui, QtWidgets
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


def close(sig, frame):
    """
    when ctrl-c is pressed, display message and shut down
    """

    print("\nHei hei")
    sys.exit(0)


signal.signal(signal.SIGINT, close)

# comes from gui
currentIndex = 0

# TODO enable user to use differen configuration
excelInputFile = "C:/Mittaus/mittaus.xlsm"
excelOutputFile = "C:/Mittaus/output.xlsm"

shelfFile = "default"

mittaukset = [
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


def formatShelf():
    """
    format shelf and clear values
    """

    for index, mittaus in enumerate(mittaukset):
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

        measurements = shelve.open(shelfFile)
        temp = measurements[str(index)]
        temp = {"name": mittaus, "value": None, "cell": cell}
        measurements[str(index)] = temp
        measurements.close()


def sample_handler(data):
    """
    receive and handle incoming data from device
    """

    global currentIndex

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
        # if currentIndex == len(measurements):
        if currentIndex == 3:
            # suppress excel warnings
            warnings.filterwarnings("ignore")

            # make a copy of base excel file
            copyfile(excelInputFile, excelOutputFile)

            workbook = load_workbook(excelOutputFile, keep_vba=True)
            worksheet = workbook.active

            measurements = shelve.open(shelfFile)

            # input measurements
            for measurement in measurements:
                if measurements[str(measurement)]["value"] != None:
                    worksheet[measurements[str(measurement)]["cell"]] = float(
                        measurements[str(measurement)]["value"])

            # save excel
            workbook.save(excelOutputFile)

            measurements.close()

            sleep(1)
            os.startfile(excelOutputFile)
            sleep(1)
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
            # shell.SendKeys("^c", 0)

        # if user has pressed enter, save measurement
        elif kbhit():
            measurements = shelve.open(shelfFile)

            sys.stdout.flush()
            prompt = "\r" + str(round(float(value), 3)
                                ).ljust(5, "0") + "\t" + measurements[str(currentIndex)]["name"] + "\t" + "Tallennettu"
            raw_input(prompt)

            # update value of measurement
            measurement = measurements[str(currentIndex)]
            measurement["value"] = value
            measurements[str(currentIndex)] = measurement

            measurements.close()

            currentIndex = currentIndex + 1

        # show updated measurement
        else:
            measurements = shelve.open(shelfFile)
            sys.stdout.flush()
            sys.stdout.write("\r" + str(round(float(value), 3)
                                        ).ljust(5, "0") + "\t" + measurements[str(currentIndex)]["name"])
            measurements.close()

    # if file is used by another process
    except PermissionError as e:
        print(e)
        print("Excel-tiedosto on auki toisessa ikkunassa. Ole hyvä ja sulje tiedosto.")
        shell.SendKeys("^c", 0)

    # if base excel file doesn't exist
    except FileNotFoundError as e:
        print(e)
        print("Excel-tiedostoa ei löydy. Ole hyvä ja valitse tiedosto uudelleen.")
        shell.SendKeys("^c", 0)


def raw_test():
    """
    show all devices connected by usb
    """

    formatShelf()

    all_hids = hid.find_all_hid_devices()

    if all_hids:
        while True:
            print("Valitse mittalaite:")
            print("\n")
            print("0 => Lopetus")

            # print out all connected usb devices
            for index, device in enumerate(all_hids, 1):
                device_name = unicode("{0.vendor_name} {0.product_name}"
                                      "(vID=0x{1:04x}, pID=0x{2:04x})"
                                      "".format(device, device.vendor_id, device.product_id))
                print("{0} => {1}".format(index, device_name))

            print("\tLaite ('0' - '%d', '0' Lopettaaksesi?) "
                  "[Anna numero ja paina Enter]:" % len(all_hids))

            index_option = raw_input()

            # selection
            if index_option.isdigit():
                index_option = int(index_option)
                if index_option <= len(all_hids):
                    break

        device = all_hids[index_option - 1]

        if index_option > 0 and index_option <= len(all_hids) - 1:
            try:
                device.open()
                out_report = device.find_output_reports()
                # set custom raw data handler
                device.set_raw_data_handler(sample_handler)

                print("\nOdotetaan dataa...")

                while device.is_plugged():
                    buffer = [0x00, 0x46, 0x30, 0x0d,
                              0x0a, 0x00, 0x00, 0x00, 0x00]
                    out_report[0].set_raw_data(buffer)
                    out_report[0].send()
                    # just keep the device opened to receive events
                    sleep(0.2)
                return
                device.close()
            except Exception as e:
                print(str(e))
        else:
            print("\nHei hei")
    else:
        raw_input("Laitevirhe. Kytke laite ja aloita ohjelma uudelleen.")


if __name__ == '__main__':
    # first be kind with local encodings

    # allow to show encoded strings
    if sys.version_info < (3,):
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    # as is, don't handle unicodes
    else:
        unicode = str
        raw_input = input
    raw_test()
