from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QSlider, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
from res import *
from icon import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from messagebox import msg_error


class WelcomeScreenView(QMainWindow):
    def __init__(self):
        super(WelcomeScreenView, self).__init__()
        loadUi("login.ui", self)
class GuiAccessView(QMainWindow):
    def __init__(self):
        super(GuiAccessView, self).__init__()
        loadUi("correct.ui", self)
class VistaImagen(QMainWindow):
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