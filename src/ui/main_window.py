# ui/main_window.py
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from serial.tools import list_ports


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the .ui file dynamically
        ui_file = QFile("ui/main_window.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Access widgets
        self.combo_ports = self.ui.findChild(type(self.ui.comboBox_ports), "comboBox_ports")
        self.button_connect = self.ui.findChild(type(self.ui.pushButton_connect), "pushButton_connect")
        self.button_refresh = self.ui.findChild(type(self.ui.pushButton_refresh), "pushButton_refresh")

        # Connect signals
        self.button_refresh.clicked.connect(self.refresh_ports)
        self.button_connect.clicked.connect(self.on_connect)

        # Fill the ports dropdown initially
        self.refresh_ports()

    def refresh_ports(self):
        """Fill the combo box with all /dev/ttyACM* devices."""
        self.combo_ports.clear()
        ports = list_ports.comports()
        acm_ports = [p.device for p in ports if "ACM" in p.device]
        self.combo_ports.addItems(acm_ports)

    def on_connect(self):
        port = self.combo_ports.currentText()
        if port:
            print(f"Connecting to {port}...")
        else:
            print("No port selected!")