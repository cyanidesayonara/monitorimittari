base = """
    #MainWindow #lcdNumber,
    #MainWindow #measurementLabel,    
    #MainWindow #leftMonitorLabel,
    #MainWindow #rightMonitorLabel {
        color: #fff;
        background-color: #444;
    }
"""

light = """
"""

dark = """
    #MainWindow {
        background-color: #222;
        color: #fff;
    }
    #MainWindow > * > * {
        background-color: #444;
        color: #fff;
    }
    #MainWindow .QLabel,
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
    #MainWindow .QRadioButton {
        color: #fff;
    }
    #MainWindow .QRadioButton::indicator:checked {
        border: 3px solid white;
        border-radius: 7px;
        background-color: #000;
    }
    #MainWindow .QFileDialog {
        background-color: #444;
        color: #fff;
    }
    #MainWindow .QFileDialog .QLabel,
    #MainWindow .QMessageBox .QLabel {
        color: #fff;
        background-color: #444;
    }    
"""

pride = """
    #MainWindow #lcdNumber {
        color: pink;
        background: qlineargradient( x2:0 x1:0, y2:1 y1:0, stop:0 red, stop:.166 red, stop:.167 orange, stop:.333 orange, stop:.334 yellow, stop:.499 yellow, stop:.50 green, stop:.666 green, stop:.667 blue, stop:.833 blue, stop:.834 fuchsia, stop:1 fuchsia);
    }
"""
