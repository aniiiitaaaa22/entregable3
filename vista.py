from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QSlider, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        loadUi('base.ui' , self)

        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.img)
        layout.addWidget(self.slider)
        layout.addWidget(self.salir)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Visor DICOM')
