from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import os
import sys
import pydicom
from messagebox import msg_error
from vista import VistaImagen_dcm , WelcomeScreenView,Vista, GraficoDispersion, GuiAccessView, MenuVista , InterfazGrafico_mat, MorfologiaVista, Vista
from modelo import Modelo_dcm , Biosenal, db_mysql, OperacionesMorfologicas, Modelo
from fon import *
from mi import *
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np


 
widget = None

class Coordinador_mat(object): ### para el objeto llama esto con InterfazGrafico_mat() y Bioseñal()
    def __init__(self, vista, biosenal):
        self.mi_vista = vista
        self.mi_biosenal = biosenal
        self.mi_vista.salir.clicked.connect(self.regresar_login)

    def regresar_login(self):
        self.mi_vista.hide()
        global MenuControlleri
        global widget
        MenuControlleri = MenuController(MenuVista(), widget)
        MenuControlleri.viewM.show()
    def recibirDatosSenal(self,data):
        self.mi_biosenal.asignarDatos(data)
    def devolverDatosSenal(self, x_min, x_max):
        return self.mi_biosenal.devolver_segmento(x_min, x_max)
    def escalarSenal(self,x_min,x_max, escala):
        return self.mi_biosenal.escalar_senal(x_min, x_max, escala)
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
    def regresar_login(self):
        self.vista_imagen.hide()
        global MenuControlleri
        global widget
        MenuControlleri = MenuController(MenuVista(), widget)
        MenuControlleri.viewM.show()
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
        self.view.exitButton.clicked.connect(self.exit_application)

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
    
    def exit_application(self):
        sys.exit()
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
        self.controlador_imagen = controlador_imagen
        self.controlador_mat = controlador_mat
        self.controlador_jpg = controlador_jpg
        self.controlador_csv = controlador_csv
        self.viewM.pushButton.clicked.connect(self.login)
        self.viewM.DCM.clicked.connect(self.DCM)   #CAMBIARLE EL BOTON   
        self.viewM.MAT.clicked.connect(self.MAT) 
        self.viewM.JPG.clicked.connect(self.JPG)
        self.viewM.CSV.clicked.connect(self.CSV) 
    
    def mostrarMensaje(self):
        mensaje_box = QMessageBox()
        mensaje_box.setWindowTitle('Mensaje')
        mensaje_box.setText('Saliendo del menú principal')
        mensaje_box.setIcon(QMessageBox.Information)
        mensaje_box.setStandardButtons(QMessageBox.Ok)
        mensaje_box.exec_()
    def login(self):
        self.viewM.hide()
        welcome_controller.widget.show()
    def DCM(self):
        self.viewM.close()
        global controlador_imagen
        self.controlador_imagen.vista_imagen.show()

    def JPG(self):
        self.viewM.close()
        global controlador_jpg
        self.controlador_jpg.vista.show()
    def CSV(self):
        self.viewM.close()
        global controlador_csv
        self.controlador_csv.vista.show()
    def MAT(self):
        self.viewM.close()
        global controlador_mat
        self.controlador_mat.mi_vista.show()
        
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

class MorfologiaControlador:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.modelo = OperacionesMorfologicas()
        self.vista = MorfologiaVista()

        # Conectar señales y slots
        self.vista.cargar_imagen_button.clicked.connect(self.cargar_imagen)
        self.vista.erosion_button.clicked.connect(self.aplicar_erosion)
        self.vista.dilatacion_button.clicked.connect(self.aplicar_dilatacion)
        self.vista.apertura_button.clicked.connect(self.aplicar_apertura)
        self.vista.cierre_button.clicked.connect(self.aplicar_cierre)
        self.vista.det_contornos_button.clicked.connect(self.aplicar_deteccion_contornos)
        self.vista.salir_button.clicked.connect(self.regresar_login)

    def regresar_login(self):
        self.vista.hide()
        global MenuControlleri
        global widget
        MenuControlleri = MenuController(MenuVista(), widget)
        MenuControlleri.viewM.show()    

    def cargar_imagen(self):
        filtro = "Images (*.png *.jpg *.bmp);;All Files (*)"
        ruta, _ = QFileDialog.getOpenFileName(None, "Abrir Imagen", "", filtro)
        if ruta:
            try:
                self.modelo.cargar_imagen(ruta)
                self.mostrar_imagen(self.modelo.imagen_original, self.vista.imagen_original_label)
            except FileNotFoundError as e:
                self.vista.mostrar_mensaje_error("Error", str(e))

    def mostrar_imagen(self, imagen, label):
        height, width, channel = imagen.shape
        bytes_per_line = 3 * width
        q_image = QImage(imagen.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_image.rgbSwapped())
        label.setPixmap(pixmap)

    def estilo_boton(self, boton):
        boton.setStyleSheet("background-color: rgb(177, 100, 182);"
                            "font: 14pt 'Comic Sans MS';"
                            "border-radius: 15px;")

    def aplicar_erosion(self):
        if self.modelo.imagen_original is not None:
            self.modelo.erosion()
            self.mostrar_imagen(self.modelo.imagen_procesada, self.vista.imagen_procesada_label)
        else:
            self.vista.mostrar_mensaje_informacion("Información", "Cargue una imagen primero.")

    def aplicar_dilatacion(self):
        if self.modelo.imagen_original is not None:
            self.modelo.dilatacion()
            self.mostrar_imagen(self.modelo.imagen_procesada, self.vista.imagen_procesada_label)
        else:
            self.vista.mostrar_mensaje_informacion("Información", "Cargue una imagen primero.")

    def aplicar_apertura(self):
        if self.modelo.imagen_original is not None:
            self.modelo.apertura()
            self.mostrar_imagen(self.modelo.imagen_procesada, self.vista.imagen_procesada_label)
        else:
            self.vista.mostrar_mensaje_informacion("Información", "Cargue una imagen primero.")

    def aplicar_cierre(self):
        if self.modelo.imagen_original is not None:
            self.modelo.cierre()
            self.mostrar_imagen(self.modelo.imagen_procesada, self.vista.imagen_procesada_label)
        else:
            self.vista.mostrar_mensaje_informacion("Información", "Cargue una imagen primero.")

    def aplicar_deteccion_contornos(self):
        if self.modelo.imagen_original is not None:
            self.modelo.deteccion_contornos()
            self.mostrar_imagen(self.modelo.imagen_procesada, self.vista.imagen_procesada_label)
        else:
            self.vista.mostrar_mensaje_informacion("Información", "Cargue una imagen primero.")

    def ejecutar(self):
        self.vista.show()
        sys.exit(self.app.exec_())

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def cargar_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.vista, 'Seleccionar archivo CSV', '', 'Archivos CSV (*.csv);;Todos los archivos (*)')

        if file_path:
            self.modelo.cargar_csv(file_path)
            self.vista.combo_columnas.addItems(self.modelo.obtener_columnas())
            self.vista.mostrar_resultados("CSV cargado exitosamente.")

    def seleccionar_columna(self):
        columna_seleccionada = self.vista.combo_columnas.currentText()
        self.modelo.columna_seleccionada = columna_seleccionada
        self.vista.mostrar_resultados(f"Columna seleccionada: {columna_seleccionada}")

    def aplicar_seno(self):
        if self.modelo.df is not None and self.modelo.columna_seleccionada:
            self.modelo.aplicar_funcion_seno(self.modelo.columna_seleccionada)
            self.vista.mostrar_resultados("Función seno aplicada exitosamente.")

    def realizar_muestreo(self):
        if self.modelo.df is not None:
            df_resultado = self.modelo.muestreo_aleatorio()
            self.vista.mostrar_resultados(str(df_resultado))

    def graficar(self):
        if self.modelo.df is not None and self.modelo.columna_seleccionada:
            x = self.modelo.df.index
            y = self.modelo.df[self.modelo.columna_seleccionada]
            self.vista.grafico_dispersion.actualizar_grafico(x, y)

    def salir(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    gui_access_controller = GuiAccessController(GuiAccessView, widget)
    welcome_controller = WelcomeScreenController(WelcomeScreenView, gui_access_controller, widget)
    controlador_imagen = Controlador_imagen_dcm(vista=VistaImagen_dcm(), modelo=Modelo_dcm())
    vista_mat = InterfazGrafico_mat()
    controlador_mat = Coordinador_mat(vista= vista_mat,biosenal=Biosenal())
    vista_mat.asignarCoordinador(controlador_mat)
    controlador_jpg = MorfologiaControlador()

    controlador_csv = Controlador(modelo=Modelo(), vista=(None))
    vista_csv = Vista(controlador_csv)
    controlador_csv.vista = vista_csv

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
