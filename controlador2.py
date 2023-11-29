from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import os
import sys
import pydicom
from messagebox import msg_error
from vista import VistaImagen_dcm, WelcomeScreenView, GuiAccessView, MenuVista , InterfazGrafico_mat
from modelo import Modelo_dcm , Biosenal, db_mysql
from fon import *
from mi import *
import cv2


import json
import numpy as np

import numpy as np
 
widget = None

class Coordinador_mat(object): ### para el objeto llama esto con InterfazGrafico_mat() y Bioseñal()
    def __init__(self, vista, biosenal):
        self.__mi_vista = vista
        self.__mi_biosenal = biosenal
    def recibirDatosSenal(self,data):
        self.__mi_biosenal.asignarDatos(data)
    def devolverDatosSenal(self, x_min, x_max):
        return self.__mi_biosenal.devolver_segmento(x_min, x_max)
    def escalarSenal(self,x_min,x_max, escala):
        return self.__mi_biosenal.escalar_senal(x_min, x_max, escala)
class Controlador_imagen_dcm:
    def __init__(self, vista, modelo):
        self.vista_imagen = vista
        self.modelo = modelo
        self.vista_imagen.comboBox.addItems(self.modelo.obtener_carpetas_dicom())
        self.vista_imagen.comboBox.currentIndexChanged.connect(lambda: self.vista_imagen.slider.setValue(0))
        self.vista_imagen.comboBox.currentIndexChanged.connect(lambda: self.actualizar_imagen(corte= self.vista_imagen.tipo_corte.currentText()))
        self.vista_imagen.slider.valueChanged.connect(lambda: self.actualizar_imagen(corte= self.vista_imagen.tipo_corte.currentText()))
        self.vista_imagen.tipo_corte.currentIndexChanged.connect(lambda: self.vista_imagen.slider.setValue(0))
        self.vista_imagen.tipo_corte.currentIndexChanged.connect(lambda: self.actualizar_imagen(corte= self.vista_imagen.tipo_corte.currentText()))
        self.vista_imagen.salir.clicked.connect(self.regresar_login)  ### Conectar el botón "Salir"
        self.actualizar_imagen()
#        self.vista_imagen.show()

#CONEXIÓN ENTRE INTERFACES IMPORTANTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    def regresar_login(self):
        self.vista_imagen.hide()
        welcome_controller.widget.show()    ## OBJETO DE LA VENTANA PRINCIPAL   

    def actualizar_imagen(self,corte=None):
        carpeta_seleccionada = self.vista_imagen.comboBox.currentText()
        archivos_dicom = self.modelo.obtener_archivos_dicom(carpeta_seleccionada)
        slices = [pydicom.dcmread(f'{carpeta_seleccionada}/{archivo}') for archivo in archivos_dicom]
        slices.sort(key=lambda x: int(x.ImagePositionPatient[2]))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        for s in slices:
            s.SliceThickness = slice_thickness
        volum = np.stack([s.pixel_array for s in slices])
        volum = volum.astype(np.int16)
        volum[volum == -2000] = 0
        stacked_slices=np.array(volum, dtype=np.int16)    
        indice_imagen = self.vista_imagen.slider.value()
        if corte == 'Axial':
            largo_corte = int(stacked_slices.shape[0])
        elif corte == 'Coronal':
            largo_corte = int(stacked_slices.shape[1])
        elif corte == 'Sagital':
            largo_corte = int(stacked_slices.shape[2])
        elif corte == None:
            largo_corte = int(stacked_slices.shape[0])
        if 0 <= indice_imagen < largo_corte:
            if corte == 'Axial':
                ds = stacked_slices[indice_imagen,:,:]   #corte axial
            elif corte == 'Coronal':
                ds = stacked_slices[:,indice_imagen,:]   #corte coronal
            elif corte == 'Sagital':
                ds = stacked_slices[:,:,indice_imagen]   #corte sagital
            else:
                ds = stacked_slices[indice_imagen,:,:]
            imagen = self.normalize_pixels(ds)
            imagen_array = cv2.resize(imagen,(491,351))
            q_image = self.array_to_pixmap(imagen_array)
            self.vista_imagen.img.setPixmap(q_image)
            self.vista_imagen.slider.setRange(0, largo_corte - 1)
            info_paciente = self.modelo.obtener_info_paciente(slices[0])
#            db_mysql(data = info_paciente )
            self.actualizar_info_paciente(info_paciente)

    def normalize_pixels(self, imagen_array):
        min_percentile = np.percentile(imagen_array, 1)
        max_percentile = np.percentile(imagen_array, 99)
        mask = (max_percentile - min_percentile) != 0
        normalized_array = np.zeros_like(imagen_array, dtype='float64')
        normalized_array[mask] = 255 * (imagen_array[mask] - min_percentile) / (max_percentile - min_percentile)
        return normalized_array.astype('uint8')
    def array_to_pixmap(self, imagen_array):
        if len(imagen_array.shape) == 2:
            height, width = imagen_array.shape
            q_image = QImage(imagen_array.data, width, height, width, QImage.Format_Grayscale8)
        elif len(imagen_array.shape) == 3:
            height, width, channel = imagen_array.shape
            q_image = QImage(imagen_array.data, width, height, 3 * width, QImage.Format_RGB888)
        else:
            raise ValueError("Formato de imagen no compatible")
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.vista_imagen.img.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
                    global MenuControlleri
                    MenuControlleri = MenuController(MenuVista(), self.widget)
                    MenuControlleri.viewM.show()
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
class MenuController:
    def __init__(self, viewM,  widgetM):
        self.viewM = viewM
        self.widgetM = widgetM
        self.viewM.pushButton.clicked.connect(self.login)        
    def login(self):
        self.viewM.hide()
        welcome_controller.widget.show()
    def DCM(self):
        self.viewM.hide()                     ######################
        global controlador_imagen             ######################
        controlador_imagen.vista_imagen.show()######################

    def JPG(self):
        pass
    def CSV(self):
        pass
    def MAT(self):
        pass
class GuiAccessController:
    def __init__(self, view, widget):
        self.view = view()
        self.widget = widget
        self.view.pushButton.clicked.connect(self.regresar_login)

    def regresar_login(self):
        self.hide()
        global controlador_imagen
        controlador_imagen = Controlador_imagen_dcm(VistaImagen_dcm(), Modelo_dcm())
        controlador_imagen.vista_imagen.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    gui_access_controller = GuiAccessController(GuiAccessView, widget)
    welcome_controller = WelcomeScreenController(WelcomeScreenView, gui_access_controller, widget)
    controlador_imagen = Controlador_imagen_dcm(vista=VistaImagen_dcm() , modelo=Modelo_dcm())
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
