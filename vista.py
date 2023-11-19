from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import os

class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('base.ui', self)
    
    def setup(self):
        self.comboBox.currentIndexChanged.connect(self.cargar)
        self.carpeta = 'images'
        lista_archivos = os.listdir(self.carpeta)
        #self.slider.valueChanged.connect(self.cargar)
        #self.current_index = self.slider.value() - 1
        for archivo in lista_archivos:
            self.comboBox.addItem(archivo)
    
    def addControler(self,c):
        self.__mi_coordinador=c
        self.setup()

    def cargar(self):
        imagen = self.comboBox.currentText()
        self.__mi_coordinador.img_conextion(imagen)
        pixmap = QPixmap("temp_image.png")
        self.img.setPixmap(pixmap)
        os.remove('temp_image.png')
