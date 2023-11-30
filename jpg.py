import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout

from messagebox import msg_about, msg_error  # Asegúrate de ajustar la importación según la ubicación de tu archivo messagebox


class OperacionesMorfologicas:
    def __init__(self):
        self.imagen_original = None
        self.imagen_procesada = None

    def cargar_imagen(self, ruta):
        self.imagen_original = cv2.imread(ruta)
        if self.imagen_original is None:
            msg_error("Error", "No se puede cargar la imagen desde {}".format(ruta))
            raise FileNotFoundError(f"No se puede cargar la imagen desde {ruta}")

    def convertir_a_escala_de_grises(self):
        self.imagen_original = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)

    def erosion(self, kernel_size=5, iterations=1):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.imagen_procesada = cv2.erode(self.imagen_original, kernel, iterations=iterations)

    def dilatacion(self, kernel_size=5, iterations=1):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.imagen_procesada = cv2.dilate(self.imagen_original, kernel, iterations=iterations)

    def apertura(self, kernel_size=5):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.imagen_procesada = cv2.morphologyEx(self.imagen_original, cv2.MORPH_OPEN, kernel)

    def cierre(self, kernel_size=5):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.imagen_procesada = cv2.morphologyEx(self.imagen_original, cv2.MORPH_CLOSE, kernel)

    def deteccion_contornos(self):
        # Convertir a escala de grises si la imagen original es a color
        if len(self.imagen_original.shape) == 3:
            imagen_gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        else:
            imagen_gris = self.imagen_original

        # Aplicar umbral
        _, umbral = cv2.threshold(imagen_gris, 127, 255, 0)

        # Encontrar contornos
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contornos en la imagen original
        imagen_contornos = self.imagen_original.copy()
        cv2.drawContours(imagen_contornos, contornos, -1, (0, 255, 0), 2)

        self.imagen_procesada = imagen_contornos


class MorfologiaApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Operaciones Morfológicas y Detección de Contornos")
        self.setGeometry(100, 100, 1200, 600)

        self.imagen_original_label = QLabel(self)
        self.imagen_original_label.setAlignment(Qt.AlignCenter)

        self.imagen_procesada_label = QLabel(self)
        self.imagen_procesada_label.setAlignment(Qt.AlignCenter)

        self.operaciones_morfologicas = OperacionesMorfologicas()

        self.cargar_imagen_button = QPushButton("Cargar Imagen", self)
        self.cargar_imagen_button.clicked.connect(self.cargar_imagen)
        self.estilo_boton(self.cargar_imagen_button)

        self.erosion_button = QPushButton("Erosión", self)
        self.erosion_button.clicked.connect(self.aplicar_erosion)
        self.estilo_boton(self.erosion_button)

        self.dilatacion_button = QPushButton("Dilatación", self)
        self.dilatacion_button.clicked.connect(self.aplicar_dilatacion)
        self.estilo_boton(self.dilatacion_button)

        self.apertura_button = QPushButton("Apertura", self)
        self.apertura_button.clicked.connect(self.aplicar_apertura)
        self.estilo_boton(self.apertura_button)

        self.cierre_button = QPushButton("Cierre", self)
        self.cierre_button.clicked.connect(self.aplicar_cierre)
        self.estilo_boton(self.cierre_button)

        self.det_contornos_button = QPushButton("Detección de Contornos", self)
        self.det_contornos_button.clicked.connect(self.aplicar_deteccion_contornos)
        self.estilo_boton(self.det_contornos_button)

        self.salir_button = QPushButton("Salir", self)
        self.salir_button.clicked.connect(self.close)
        self.estilo_boton(self.salir_button)

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
        label_procesada.setFont(QFont("Comic Sans MS", 14))  # Aplicar el estilo de fuente
        vbox_procesada.addWidget(label_procesada)
        vbox_procesada.addWidget(self.imagen_procesada_label)
        vbox_procesada.addStretch(1)


        layout.addLayout(vbox_original)
        layout.addLayout(vbox_procesada)

    def cargar_imagen(self):
        filtro = "Images (*.png *.jpg *.bmp);;All Files (*)"
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir Imagen", "", filtro)
        if ruta:
            try:
                self.operaciones_morfologicas.cargar_imagen(ruta)
                self.mostrar_imagen(self.operaciones_morfologicas.imagen_original, self.imagen_original_label)
            except FileNotFoundError as e:
                msg_error("Error", str(e))

    def mostrar_imagen(self, imagen, label):
        height, width, channel = imagen.shape  # Tomar las dimensiones de la imagen
        bytes_per_line = 3 * width  # Multiplicado por 3 para los canales de color (BGR)
        q_image = QImage(imagen.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_image.rgbSwapped())  # Swapped para convertir de BGR a RGB
        label.setPixmap(pixmap)

    def estilo_boton(self, boton):
        boton.setStyleSheet("background-color: rgb(177, 100, 182);"
                            "font: 14pt 'Comic Sans MS';"
                            "border-radius: 15px;")

    def aplicar_erosion(self):
        if self.operaciones_morfologicas.imagen_original is not None:
            self.operaciones_morfologicas.erosion()
            self.mostrar_imagen(self.operaciones_morfologicas.imagen_procesada, self.imagen_procesada_label)
        else:
            msg_about("Información", "Cargue una imagen primero.")

    def aplicar_dilatacion(self):
        if self.operaciones_morfologicas.imagen_original is not None:
            self.operaciones_morfologicas.dilatacion()
            self.mostrar_imagen(self.operaciones_morfologicas.imagen_procesada, self.imagen_procesada_label)
        else:
            msg_about("Información", "Cargue una imagen primero.")

    def aplicar_apertura(self):
        if self.operaciones_morfologicas.imagen_original is not None:
            self.operaciones_morfologicas.apertura()
            self.mostrar_imagen(self.operaciones_morfologicas.imagen_procesada, self.imagen_procesada_label)
        else:
            msg_about("Información", "Cargue una imagen primero.")

    def aplicar_cierre(self):
        if self.operaciones_morfologicas.imagen_original is not None:
            self.operaciones_morfologicas.cierre()
            self.mostrar_imagen(self.operaciones_morfologicas.imagen_procesada, self.imagen_procesada_label)
        else:
            msg_about("Información", "Cargue una imagen primero.")

    def aplicar_deteccion_contornos(self):
        if self.operaciones_morfologicas.imagen_original is not None:
            self.operaciones_morfologicas.deteccion_contornos()
            self.mostrar_imagen(self.operaciones_morfologicas.imagen_procesada, self.imagen_procesada_label)
        else:
            msg_about("Información", "Cargue una imagen primero.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MorfologiaApp()
    ventana.show()
    sys.exit(app.exec_())
