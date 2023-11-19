from PyQt5.QtWidgets import QApplication
from vista import Vista
from modelo import Modelo
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QTableWidgetItem
import os
import sys
import pydicom
class Controlador:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.vista.comboBox.addItems(self.modelo.obtener_carpetas_dicom())
        self.vista.comboBox.currentIndexChanged.connect(self.actualizar_imagen)
        self.vista.slider.valueChanged.connect(self.actualizar_imagen)
#        self.vista.salir.clicked.connect() ####################  salir para ir a login

        self.actualizar_imagen()

        self.vista.show()

    def actualizar_imagen(self):
        carpeta_seleccionada = self.vista.comboBox.currentText()
        archivos_dicom = self.modelo.obtener_archivos_dicom(carpeta_seleccionada)
        indice_imagen = self.vista.slider.value()

        if 0 <= indice_imagen < len(archivos_dicom):
            ruta_dicom = os.path.join(carpeta_seleccionada, archivos_dicom[indice_imagen])
            ds = pydicom.dcmread(ruta_dicom)
            imagen_array = self.normalize_pixels(ds.pixel_array)
            q_image = self.array_to_pixmap(imagen_array)
            self.vista.img.setPixmap(q_image)
            self.vista.slider.setRange(0, len(archivos_dicom) - 1)

            info_paciente = self.modelo.obtener_info_paciente(ds)
            self.actualizar_info_paciente(info_paciente)

    def normalize_pixels(self, imagen_array):
        min_pixel = imagen_array.min()
        max_pixel = imagen_array.max()
        normalized_array = 255 * (imagen_array - min_pixel) / (max_pixel - min_pixel)
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
        pixmap = pixmap.scaled(self.vista.img.width(), self.vista.img.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    def actualizar_info_paciente(self, info_paciente):
        self.vista.lista.setRowCount(0)
        for etiqueta, valor in info_paciente.items():
            num_filas = self.vista.lista.rowCount()
            self.vista.lista.insertRow(num_filas)
            self.vista.lista.setItem(num_filas, 0, QTableWidgetItem(etiqueta))
            self.vista.lista.setItem(num_filas, 1, QTableWidgetItem(str(valor)))

if __name__ == '__main__':
    app = QApplication([])
    modelo = Modelo()
    vista = Vista()
    controlador = Controlador(vista, modelo)
    app.exec_()
