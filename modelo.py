import os

class Modelo:
    def __init__(self):
        self.carpetas_dicom = [carpeta for carpeta in os.listdir() if os.path.isdir(carpeta) and all(f.lower().endswith('.dcm') for f in os.listdir(carpeta))]

    def obtener_carpetas_dicom(self):
        return self.carpetas_dicom

    def obtener_archivos_dicom(self, carpeta_seleccionada):
        return [f for f in os.listdir(carpeta_seleccionada) if f.lower().endswith('.dcm')]

    def obtener_info_paciente(self, ds):
        return {
            "Imagen Numero": str(ds.InstanceNumber),
            "Nombre del paciente": ds.PatientName,
            "ID del paciente": ds.PatientID,
            "Sexo del paciente": ds.PatientSex,
            "Tipo de estudio": ds.Modality
        }
