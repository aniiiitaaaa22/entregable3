import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTextEdit, QFileDialog, QComboBox, QAction
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class OperacionesConCSV:
    def __init__(self, archivo_csv):
        self.df = pd.read_csv(archivo_csv)

    def cargar_csv(self):
        return self.df

    def aplicar_funcion_seno(self, columna):
        self.df[columna] = np.sin(self.df[columna])
        return self.df

    def muestreo_aleatorio(self, n=10):
        return self.df.sample(n=n)

class GraficoDispersión(QWidget):
    def __init__(self, parent=None):
        super(GraficoDispersión, self).__init__(parent)
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

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.operaciones = None
        self.columna_seleccionada = None

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
        cargar_csv_button.clicked.connect(self.cargar_csv)
        cargar_csv_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(cargar_csv_button)

        self.combo_columnas = QComboBox(self)
        self.layout.addWidget(self.combo_columnas)

        seleccionar_columna_button = QPushButton('Seleccionar Columna', self)
        seleccionar_columna_button.clicked.connect(self.seleccionar_columna)
        seleccionar_columna_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(seleccionar_columna_button)

        aplicar_seno_button = QPushButton('Aplicar Seno', self)
        aplicar_seno_button.clicked.connect(self.aplicar_seno)
        aplicar_seno_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(aplicar_seno_button)

        muestreo_button = QPushButton('Muestreo Aleatorio', self)
        muestreo_button.clicked.connect(self.realizar_muestreo)
        muestreo_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(muestreo_button)

        graficar_button = QPushButton('Graficar', self)
        graficar_button.clicked.connect(self.graficar)
        graficar_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(graficar_button)

        salir_action = QAction('Salir', self)
        salir_action.triggered.connect(self.salir)
        salir_button = QPushButton('Salir', self)
        salir_button.clicked.connect(self.salir)
        salir_button.setStyleSheet("background-color: rgb(177, 100, 182); font: 14pt 'Comic Sans MS'; border-radius: 15px;")
        self.layout.addWidget(salir_button)

        self.grafico_dispersion = GraficoDispersión(self)
        self.layout.addWidget(self.grafico_dispersion)

        self.central_widget.setLayout(self.layout)

    def cargar_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Seleccionar archivo CSV', '', 'Archivos CSV (*.csv);;Todos los archivos (*)')

        if file_path:
            self.operaciones = OperacionesConCSV(file_path)
            self.cargar_columnas()
            self.mostrar_resultados()

    def cargar_columnas(self):
        self.combo_columnas.clear()
        self.combo_columnas.addItems(self.operaciones.df.columns.tolist())

    def seleccionar_columna(self):
        self.columna_seleccionada = self.combo_columnas.currentText()
        print(f"Columna seleccionada: {self.columna_seleccionada}")

    def aplicar_seno(self):
        if self.operaciones and self.columna_seleccionada:
            self.operaciones.aplicar_funcion_seno(self.columna_seleccionada)
            self.mostrar_resultados()

    def realizar_muestreo(self):
        if self.operaciones:
            self.mostrar_resultados(muestreo=True)

    def graficar(self):
        if self.operaciones and self.columna_seleccionada:
            x = self.operaciones.df.index  # Usamos los índices como valores x
            y = self.operaciones.df[self.columna_seleccionada]
            self.grafico_dispersion.actualizar_grafico(x, y)

    def mostrar_resultados(self, muestreo=False):
        result = ""
        if muestreo:
            df_resultado = self.operaciones.muestreo_aleatorio()
        else:
            df_resultado = self.operaciones.cargar_csv()

        result += "DataFrame:\n" + str(df_resultado) + "\n\n"
        result += "Información del DataFrame:\n" + str(df_resultado.info()) + "\n\n"
        self.text_output.setPlainText(result)

    def salir(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
