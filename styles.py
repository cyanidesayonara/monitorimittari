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
    #MainWindow .QRadioButton,
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
    #MainWindow #rightMonitorLabel  {
        background-color: #444;
    }

"""

base = """

"""
