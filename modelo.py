import os
import cv2 
import numpy as np
import pandas as pd
import mysql.connector

class db_mysql:
    def __init__(self , data):
        self.datos = data
        self.db = mysql.connector.connect(
            host = "%.%.%.%",
            user= "root",
            password = "",
            database = "SanrioMedical")
        self.cursor = self.db.cursor()
        self.subida()
        self.cursor.close()
        self.db.close()
    def subida(self):
        consulta = "SELECT * FROM `info paciente`"
        self.cursor.execute(consulta)
        resultados = self.cursor.fetchall()
        esta = False
        for i in resultados:
            if self.datos["Identificador Estancia de Estudio"] in i:
                esta = True
        if esta == False:
            subida = "INSERT INTO `info paciente` (`Nombre Paciente`, `ID Paciente`, `Tipo de Estudio`, `Fecha Estudio`, `Identificador Estancia de Estudio`) VALUES (%s, %s, %s, %s, %s)"
            datos_subida = (str(self.datos['Nombre Paciente']), self.datos['ID Paciente'], self.datos['Tipo de Estudio'], self.datos['Fecha Estudio'], self.datos['Identificador Estancia de Estudio'])
            self.cursor.execute(subida, datos_subida)
            self.db.commit()
class Modelo_dcm:
    def __init__(self):
        self.carpetas_dicom = [carpeta for carpeta in os.listdir() if os.path.isdir(carpeta) and all(f.lower().endswith('.dcm') for f in os.listdir(carpeta))]

    def obtener_carpetas_dicom(self):
        return self.carpetas_dicom

    def obtener_archivos_dicom(self, carpeta_seleccionada):
        return [f for f in os.listdir(carpeta_seleccionada) if f.lower().endswith('.dcm')]

    def obtener_info_paciente(self, ds):
        return {
            "ID Paciente": ds.PatientID,
            "Nombre Paciente": ds.PatientName,
            "Tipo de Estudio": ds.Modality,
            "Fecha Estudio" : ds.StudyDate,
            "Identificador Estancia de Estudio" : ds.StudyInstanceUID
        }

class Biosenal:
    def __init__(self,data = None):
        if data is not None:
            self.asignarDatos(data)
        else:
            self.data = []
            self.canales = 0
            self.puntos = 0
    
    def asignarDatos(self,data):
        self.data = data
        self.canales = data.shape[0]
        self.puntos = data.shape[1]
    def devolver_segmento(self, x_min, x_max):
        if x_min >= x_max:
            return None
        return self.data[:,x_min:x_max]
    def escalar_senal(self,x_min,x_max, escala):
        if x_min >= x_max:
            return None
        copia_data = self.data[:,x_min:x_max].copy()
        return copia_data*escala


class OperacionesMorfologicas:
    def __init__(self):
        self.imagen_original = None
        self.imagen_procesada = None

    def cargar_imagen(self, ruta):
        self.imagen_original = cv2.imread(ruta)
        if self.imagen_original is None:
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
        if len(self.imagen_original.shape) == 3:
            imagen_gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
        else:
            imagen_gris = self.imagen_original

        _, umbral = cv2.threshold(imagen_gris, 127, 255, 0)
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        imagen_contornos = self.imagen_original.copy()
        cv2.drawContours(imagen_contornos, contornos, -1, (0, 255, 0), 2)

        self.imagen_procesada = imagen_contornos

class Modelo:
    def __init__(self):
        self.df = None
        self.columna_seleccionada = None

    def cargar_csv(self, archivo_csv):
        self.df = pd.read_csv(archivo_csv)

    def obtener_columnas(self):
        return self.df.columns.tolist()

    def aplicar_funcion_seno(self, columna):
        self.df[columna] = np.sin(self.df[columna])

    def muestreo_aleatorio(self, n=10):
        return self.df.sample(n=n)