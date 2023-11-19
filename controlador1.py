#controlador
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QSlider, QLabel, QLineEdit, QApplication, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from modelo1 import DICOMModel
from vista1 import LoginView
import sys


class Controller:
    def __init__(self, app):
        self.app = app
        self.model = DICOMModel()
        self.login_view = LoginView(self)
#        self.main_view = MainView(self)
        self.show_login()

    def show_login(self):
        self.login_view.show()
#        self.main_view.hide()

#    def show_main(self):
#        self.login_view.hide()
#        self.main_view.show()

    def login(self):
        username = self.login_view.txtUsername.text()
        password = self.login_view.txtPassword.text()

        if username == 'medicoAnalitico' and password == 'bio12345':
            self.show_main()
        else:
            QMessageBox.warning(self.login_view, 'Error', 'Credenciales incorrectas.')

if __name__ == '__main__':
    app =QApplication(sys.argv)
    controlador = Controller(app)