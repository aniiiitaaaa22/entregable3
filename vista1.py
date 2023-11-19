#vista
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QSlider, QLabel, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView

class LoginView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')

        self.lblUsername = QLabel('User: ', self)
        self.txtUsername = QLineEdit(self)

        self.lblPassword = QLabel('Password: ', self)
        self.txtPassword = QLineEdit(self)
        self.txtPassword.setEchoMode (QLineEdit.Password)

        self.btnLogin = QPushButton('Login', self)
        self.btnLogin.clicked.connect(self.controller.login)

        layout = QVBoxLayout()
        layout.addWidget(self.lblUsername)
        layout.addWidget(self.txtUsername)
        layout.addWidget(self.lblPassword)
        layout.addWidget(self.txtPassword)
        layout.addWidget(self.btnLogin)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)