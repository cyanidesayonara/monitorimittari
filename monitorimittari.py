from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import warnings
import signal
from time import sleep
from msvcrt import kbhit
from openpyxl import load_workbook
from pywinusb import hid
from win32com import client
shell = client.Dispatch("WScript.Shell")


def close(sig, frame):
    try:
        os.remove("mittaus.txt")
    except (FileNotFoundError, PermissionError):
        pass
    print("\nHei hei")
    sys.exit(0)


signal.signal(signal.SIGINT, close)


def sample_handler(data):
    #print("Raw data: {0}".format(data))
    value = chr(data[2]) + "." + \
        chr(data[4]) + \
        chr(data[5]) + \
        chr(data[6]) + \
        chr(data[7]) + \
        chr(data[8]) + \
        chr(data[9]) + \
        chr(data[10]) + \
        chr(data[11])

    mittaus = [
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

    i = sum(1 for line in open('mittaus.txt'))

    if kbhit() and i < 56:  # if not kbhit()

        sys.stdout.flush()
        prompt = "\r" + str(round(float(value), 3)).ljust(
            5, "0") + "\t" + mittaus[i] + "\t" + "Tallennettu"

        raw_input(prompt)

        with open('mittaus.txt', 'a') as file:
            file.write(value + "\n")

        if i < 18:
            solu = "B%d" % (i + 29)
        elif i >= 18 and i < 23:
            solu = "B%d" % (i + 42)
        elif i >= 23 and i < 28:
            solu = "B%d" % (i + 45)
        elif i >= 28 and i < 46:
            solu = "F%d" % (i + 1)
        elif i >= 46 and i < 51:
            solu = "F%d" % (i + 14)
        elif i >= 51 and i < 56:
            solu = "F%d" % (i + 17)

        warnings.filterwarnings("ignore")
        wb = load_workbook(r"C:\Mittaus\mittaus.xlsm", keep_vba=True)
        ws = wb.active
        ws[solu] = float(value)
        wb.save(r"C:\Mittaus\mittaus.xlsm")
    else:
        try:
            sys.stdout.flush()
            sys.stdout.write("\r" + str(round(float(value), 3)
                                        ).ljust(5, "0") + "\t" + mittaus[i])

        # if all measurements taken, format excel and exit program
        except IndexError:
            sleep(1)
            os.startfile(r"C:\Mittaus\mittaus.xlsm")
            sleep(1)
            shell.SendKeys("%{F4}", 0)
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
            shell.SendKeys("^c", 0)


def raw_test():
    # show all devices connected by usb
    all_hids = hid.find_all_hid_devices()

    if all_hids:
        while True:
            print("Valitse mittalaite:")
            print("\n")
            print("0 => Lopetus")

            for index, device in enumerate(all_hids):
                device_name = unicode("{0.vendor_name} {0.product_name}"
                                      "(vID=0x{1:04x}, pID=0x{2:04x})"
                                      "".format(device, device.vendor_id, device.product_id))
                print("{0} => {1}".format(index + 1, device_name))

            print("\tLaite ('0' - '%d', '0' Lopettaaksesi?) "
                  "[Anna numero ja paina Enter]:" % len(all_hids))

            index_option = raw_input()

            # selection
            if index_option.isdigit():
                index_option = int(index_option)
                if index_option <= len(all_hids):
                    break

        device = all_hids[index_option - 1]

        if index_option > 0:
            with open('mittaus.txt', 'w') as file:
                pass
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
            finally:
                device.close()
        print("\nHei hei")
    else:
        raw_input("Laitevirhe. Kytke laite ja aloita ohjelma uudelleen.")


if __name__ == '__main__':
    # first be kind with local encodings
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    raw_test()