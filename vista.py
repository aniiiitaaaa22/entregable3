from PyQt5.QtWidgets import QFileDialog,QMainWindow, QVBoxLayout, QWidget, QMessageBox ,QLabel, QComboBox, QSlider, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
from res import *
from icon import *
from mi import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from messagebox import msg_error
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import scipy.io as sio
import numpy as np

class WelcomeScreenView(QMainWindow):
    def __init__(self):
        super(WelcomeScreenView, self).__init__()
        loadUi("login.ui", self)
class MenuVista(QMainWindow):
    def __init__(self):
        super(MenuVista, self).__init__()
        loadUi("men.ui", self)

# class Menu(QMainWindow):
#     def __init__(self):
#         super(Menu, self).__init__()
#         loadUi("login - copia.ui", self)
class GuiAccessView(QMainWindow):
    def __init__(self):
        super(GuiAccessView, self).__init__()
        loadUi("correct.ui", self)
class VistaImagen_dcm(QMainWindow):
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
        layout.addWidget(self.tipo_corte)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Visor DICOM')

class MyGraphCanvas_mat(FigureCanvas):
    def __init__(self, parent= None,width=6, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self,self.fig)
    def graficar_senal(self, datos):
        self.axes.clear()
        for c in range(datos.shape[0]):
            self.axes.plot(datos[c,:] + c*10)
        self.axes.set_xlabel('Muestras')
        self.axes.set_ylabel('Voltaje (uV)')
        self.axes.set_title('Señales EEG')
        self.draw()  
class InterfazGrafico_mat(QMainWindow):
    def __init__(self):
        super(InterfazGrafico_mat,self).__init__()
        loadUi ('mats.ui',self)
        self.setup()
    def setup(self):
        self.layout = QVBoxLayout()
        self.grafico.setLayout(self.layout)
        self.sc = MyGraphCanvas_mat(self.grafico, width=5, height=4, dpi=100)
        self.layout.addWidget(self.sc)
        self.boton_cargar.clicked.connect(lambda: self.cargar_senal())
        self.mostrar.clicked.connect(self.mostrarSeg)

    def error_llave(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("la llave seleccionada no es la correspondiente al arreglo.")
        msg.setWindowTitle("Alerta")
        msg.exec_()
        sys.exit(self.app.exec_())

    def asignarCoordinador(self,c):
        self.__coordinador = c     
    def cargar_senal(self):
        archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Abrir señal","","Todos los archivos (*);;Archivos mat (*.mat);;Python (*.py)")
        if archivo_cargado != '':
            mat = sio.loadmat(archivo_cargado)
            self.llave.addItems(mat.keys())
            if str(type(mat[self.llave.currentText()])) == "<class 'numpy.ndarray'>":
                data = mat[self.llave.currentText()]
            elif str(type(mat[self.llave.currentText()])) != "<class 'numpy.ndarray'>":
                self.error_llave()
                return None
            sensores, puntos = data.shape
            try:
                ensayos = data.shape[2]
            except:
                ensayos = 1
            senal_continua = np.reshape(data,(sensores,puntos*ensayos),order = 'F') # Conveirte de 3D a 2D
            self.__coordinador.recibirDatosSenal(senal_continua)
            self.x_min = 0
            self.x_max = 2000
            self.sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.x_min, self.x_max))
        
         
    def mostrarSeg(self):
        self.x_max = int(self.maximo.text())
        self.x_min = int(self.minimo.text())
        self.sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.x_min, self.x_max))
 