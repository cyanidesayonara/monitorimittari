light = ""
dark = """
    #MainWindow > * {
        background-color: #222;
        color: #fff;
    }
    #MainWindow > * > * {
        background-color: #444;
        color: #fff;
    }
    #MainWindow .QLabel,

    #MainWindow #verticalLayoutWidget,
    #MainWindow .QComboBox QAbstractItemView {
        background-color: #222;
        color: #fff;
    }
    #MainWindow .QTableWidget {
        alternate-background-color: #333;
    }
    #MainWindow .QHeaderView::section {
        background-color: #333;
        color: #fff
    }
    #MainWindow #measurementLabel,
    #MainWindow #leftMonitorLabel,
    #MainWindow #rightMonitorLabel,
    #MainWindow .QMessageBox QLabel {
        background-color: #444;
    }
    #MainWindow .QRadioButton {
        color: #fff;
    }
    #MainWindow .QRadioButton::indicator:checked {
        border: 3px solid white;
        border-radius: 7px;
        background-color: #000;
    }
"""

base = """

"""
