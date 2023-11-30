from PyQt5.QtWidgets import QFileDialog,QMainWindow, QVBoxLayout, QWidget,QTextEdit, QMessageBox ,QLabel, QComboBox, QSlider, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QFont
import sys
from res import *
from icon import *
from mi import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction
from messagebox import msg_error
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import scipy.io as sio
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

class WelcomeScreenView(QMainWindow):
    def __init__(self):
        super(WelcomeScreenView, self).__init__()
        loadUi("login.ui", self)
class MenuVista(QMainWindow):
    def __init__(self):
        super(MenuVista, self).__init__()
        loadUi("men.ui", self)

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
        #layout.addWidget(self.lista)
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
            senal_continua = np.reshape(data,(sensores,puntos*ensayos),order = 'F')
            self.__coordinador.recibirDatosSenal(senal_continua)
            self.x_min = 0
            self.x_max = 2000
            self.sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.x_min, self.x_max))
        
         
    def mostrarSeg(self):
        self.x_max = int(self.maximo.text())
        self.x_min = int(self.minimo.text())
        self.sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.x_min, self.x_max))

class MorfologiaVista(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Operaciones Morfológicas y Detección de Contornos")
        self.setGeometry(100, 100, 1200, 600)

        self.imagen_original_label = QLabel(self)
        self.imagen_original_label.setAlignment(Qt.AlignCenter)

        self.imagen_procesada_label = QLabel(self)
        self.imagen_procesada_label.setAlignment(Qt.AlignCenter)

        self.cargar_imagen_button = QPushButton("Cargar Imagen", self)
        self.cargar_imagen_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                                "font: 14pt 'Comic Sans MS';"
                                                "border-radius: 15px;")

        self.erosion_button = QPushButton("Erosión", self)
        self.erosion_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                          "font: 14pt 'Comic Sans MS';"
                                          "border-radius: 15px;")

        self.dilatacion_button = QPushButton("Dilatación", self)
        self.dilatacion_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                             "font: 14pt 'Comic Sans MS';"
                                             "border-radius: 15px;")

        self.apertura_button = QPushButton("Apertura", self)
        self.apertura_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                           "font: 14pt 'Comic Sans MS';"
                                           "border-radius: 15px;")

        self.cierre_button = QPushButton("Cierre", self)
        self.cierre_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                         "font: 14pt 'Comic Sans MS';"
                                         "border-radius: 15px;")

        self.det_contornos_button = QPushButton("Detección de Contornos", self)
        self.det_contornos_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                                "font: 14pt 'Comic Sans MS';"
                                                "border-radius: 15px;")

        self.salir_button = QPushButton("Salir", self)
        self.salir_button.setStyleSheet("background-color: rgb(177, 100, 182);"
                                        "font: 14pt 'Comic Sans MS';"
                                        "border-radius: 15px;")

        layout = QHBoxLayout(self)

        vbox_original = QVBoxLayout()
        vbox_original.addWidget(self.cargar_imagen_button)
        vbox_original.addWidget(self.erosion_button)
        vbox_original.addWidget(self.dilatacion_button)
        vbox_original.addWidget(self.apertura_button)
        vbox_original.addWidget(self.cierre_button)
        vbox_original.addWidget(self.det_contornos_button)
        vbox_original.addWidget(self.salir_button)
        vbox_original.addWidget(self.imagen_original_label)

        vbox_procesada = QVBoxLayout()
        label_procesada = QLabel("Imagen Procesada")
        label_procesada.setFont(QFont("Comic Sans MS", 14))
        vbox_procesada.addWidget(label_procesada)
        vbox_procesada.addWidget(self.imagen_procesada_label)
        vbox_procesada.addStretch(1)

        layout.addLayout(vbox_original)
        layout.addLayout(vbox_procesada)

class Vista(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Interfaz para Operaciones con CSV')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        cargar_csv_button = QPushButton('Cargar CSV', self)
        cargar_csv_button.clicked.connect(self.controlador.cargar_csv)
        cargar_csv_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(cargar_csv_button)

        self.combo_columnas = QComboBox(self)
        self.layout.addWidget(self.combo_columnas)

        seleccionar_columna_button = QPushButton('Seleccionar Columna', self)
        seleccionar_columna_button.clicked.connect(self.controlador.seleccionar_columna)
        seleccionar_columna_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(seleccionar_columna_button)

        aplicar_seno_button = QPushButton('Aplicar Seno', self)
        aplicar_seno_button.clicked.connect(self.controlador.aplicar_seno)
        aplicar_seno_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(aplicar_seno_button)

        muestreo_button = QPushButton('Muestreo Aleatorio', self)
        muestreo_button.clicked.connect(self.controlador.realizar_muestreo)
        muestreo_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(muestreo_button)

        graficar_button = QPushButton('Graficar', self)
        graficar_button.clicked.connect(self.controlador.graficar)
        graficar_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(graficar_button)

        salir_button = QPushButton('Salir', self)
        salir_button.clicked.connect(self.controlador.salir)
        salir_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(salir_button)

        self.grafico_dispersion = GraficoDispersion(self)
        self.layout.addWidget(self.grafico_dispersion)

        self.central_widget.setLayout(self.layout)

    def mostrar_resultados(self, resultados):
        self.text_output.setPlainText(resultados)


class GraficoDispersion(QWidget):
    def __init__(self, parent=None):
        super(GraficoDispersion, self).__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def actualizar_grafico(self, x, y):
        self.ax.clear()
        self.ax.scatter(x, y)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.canvas.draw()