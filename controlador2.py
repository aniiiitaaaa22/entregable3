from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import os
import sys
import pydicom
from messagebox import msg_error
from vista import VistaImagen, WelcomeScreenView, GuiAccessView
from modelo import Modelo
from fon import *
import json
import numpy as np
widget = None

class Controlador_imagen:
    def __init__(self, vista, modelo):
        self.vista_imagen = vista
        self.modelo = modelo
        self.vista_imagen.comboBox.addItems(self.modelo.obtener_carpetas_dicom())
        self.vista_imagen.comboBox.currentIndexChanged.connect(self.actualizar_imagen)
        self.vista_imagen.slider.valueChanged.connect(self.actualizar_imagen)
        self.vista_imagen.salir.clicked.connect(self.regresar_login)  ### Conectar el botón "Salir"
        self.actualizar_imagen()
        self.vista_imagen.show()

    def regresar_login(self):
        self.vista_imagen.hide()
        welcome_controller.widget.show()

    def actualizar_imagen(self):
        carpeta_seleccionada = self.vista_imagen.comboBox.currentText()
        archivos_dicom = self.modelo.obtener_archivos_dicom(carpeta_seleccionada)
        slices = [pydicom.dcmread(f'{carpeta_seleccionada}/{archivo}') for archivo in archivos_dicom]
        slices.sort(key=lambda x: int(x.ImagePositionPatient[2]))
        indice_imagen = self.vista_imagen.slider.value()

        if 0 <= indice_imagen < len(slices):
            ds = slices[indice_imagen]
            imagen_array = self.normalize_pixels(ds.pixel_array)
            q_image = self.array_to_pixmap(imagen_array)
            self.vista_imagen.img.setPixmap(q_image)
            self.vista_imagen.slider.setRange(0, len(slices) - 1)

            info_paciente = self.modelo.obtener_info_paciente(ds)
            self.actualizar_info_paciente(info_paciente)

    def normalize_pixels(self, imagen_array):
        min_percentile = np.percentile(imagen_array, 1)
        max_percentile = np.percentile(imagen_array, 99)
        normalized_array = 255 * (imagen_array - min_percentile) / (max_percentile - min_percentile)
        return normalized_array.astype('uint8')

    # def normalize_pixels(self, imagen_array):
        # min_pixel = imagen_array.min()
        # max_pixel = imagen_array.max()
        # normalized_array = 255 * (imagen_array - min_pixel) / (max_pixel - min_pixel)
        # return normalized_array.astype('uint8')

    def array_to_pixmap(self, imagen_array):
        if len(imagen_array.shape) == 2:
            height, width = imagen_array.shape
            q_image = QImage(imagen_array.data, width, height, width, QImage.Format_Grayscale8)
        elif len(imagen_array.shape) == 3:
            height, width, channel = imagen_array.shape
            q_image = QImage(imagen_array.data, width, height, 3 * width, QImage.Format_Indexed8)
        else:
            raise ValueError("Formato de imagen no compatible")

        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.vista_imagen.img.width(), self.vista_imagen.img.height(),
                            Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    def actualizar_info_paciente(self, info_paciente):
        self.vista_imagen.lista.setRowCount(0)
        for etiqueta, valor in info_paciente.items():
            num_filas = self.vista_imagen.lista.rowCount()
            self.vista_imagen.lista.insertRow(num_filas)
            self.vista_imagen.lista.setItem(num_filas, 0, QTableWidgetItem(etiqueta))
            self.vista_imagen.lista.setItem(num_filas, 1, QTableWidgetItem(str(valor)))
            self.vista_imagen.lista.resizeColumnsToContents()

class WelcomeScreenController:
    def __init__(self, view, gui_access_controller, widget):
        self.view = view()
        self.gui_access_controller = gui_access_controller
        self.widget = widget
        self.view.pushButton.clicked.connect(self.gui_login)

    def gui_login(self):
        name = self.view.lineEdit.text()
        password = self.view.lineEdit_2.text()

        if len(name) == 0 or len(password) == 0:
            msg_error("Error", "No hay datos")
        else:
            # Cargar datos de usuarios desde el archivo JSON
            try:
                with open('usu.json', 'r') as file:
                    user_data = json.load(file)

                # Verificar las credenciales
                if name == user_data["usuario"] and password == user_data["password"]:
                    global controlador_imagen
                    controlador_imagen = Controlador_imagen(VistaImagen(), Modelo())
                    controlador_imagen.vista_imagen.show()
                    self.widget.hide()
                else:
                    msg_error("Error", "Los datos no coinciden")

            except FileNotFoundError:
                msg_error("Error", "Archivo 'usu.json' no encontrado")
            except json.JSONDecodeError:
                msg_error("Error", "Error al decodificar el archivo JSON")
        # elif name == "medicoAnalitico" and password == "bio12345":
        #     global controlador_imagen
        #     controlador_imagen = Controlador_imagen(VistaImagen(), Modelo())
        #     controlador_imagen.vista_imagen.show()
        #     self.widget.hide()
        # else:
        #     msg_error("Error", "Los datos no coinciden")

class GuiAccessController:
    def __init__(self, view, widget):
        self.view = view()
        self.widget = widget
        self.view.pushButton.clicked.connect(self.regresar_login)

    def regresar_login(self):
        self.hide()
        global controlador_imagen
        controlador_imagen = Controlador_imagen(VistaImagen(), Modelo())
        controlador_imagen.vista_imagen.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    gui_access_controller = GuiAccessController(GuiAccessView, widget)
    welcome_controller = WelcomeScreenController(WelcomeScreenView, gui_access_controller, widget)

    widget.addWidget(welcome_controller.view)
    widget.move(400, 80)
    widget.setFixedHeight(500)
    widget.setFixedWidth(500)
    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Saliendo")
