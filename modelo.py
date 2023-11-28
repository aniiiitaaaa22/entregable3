import os
import mysql.connector
class db_mysql:
    def __init__(self , data):
        self.datos = data
        self.db = mysql.connector.connect(
            host = "127.0.0.1",
            user= "root",
            password = "",
            database = "SanrioMedical")
        self.cursor = self.db.cursor()
        self.subida()
        self.cursor.close() #
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
    #constructor que recibe los datos, si no se entregan por defectos estaran 
    #vacios
    def __init__(self,data = None):
        if data is not None:
            self.asignarDatos(data)
        else:
            self.data = []
            self.canales = 0
            self.puntos = 0
    
    def asignarDatos(self,data):
        self.data = data # Matriz 2D
        self.canales = data.shape[0] #8 canales 
        self.puntos = data.shape[1]  #360000 puntos  
    #esta funcion nos permitira movernos en el tiempo xmin y xman
    def devolver_segmento(self, x_min, x_max):
        if x_min >= x_max:
            return None
        return self.data[:,x_min:x_max]
    #esta funcion nos permitira cambiar la amplitud de la senal

    def escalar_senal(self,x_min,x_max, escala):
        #el slicing no genera copia de los datos sino que devuelve un segmento de los originales
        #para no modificar el original se debe hacer una copia
        if x_min >= x_max:
            return None
        copia_data = self.data[:,x_min:x_max].copy()
        return copia_data*escala