from PyQt5.QtWidgets import QApplication
from modelo import Modelo
from vista import Vista
import sys

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def img_conextion(self, imagen):
        self.modelo.picture_creator(imagen)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    modelo = Modelo()
    vista = Vista()
    mi_controlador=Controlador(modelo,vista)
    vista.addControler(mi_controlador)
    vista.show()
    sys.exit(app.exec_())