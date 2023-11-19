<<<<<<< HEAD
from PyQt5.QtCore import QObject
import pydicom
import matplotlib.pyplot as plt

class Modelo(QObject):
    def __init__(self):
        super().__init__()
        self.carpeta = 'images'

    def picture_creator(self, imagen):
        ds = pydicom.dcmread(self.carpeta+'/'+imagen)
        pixel_data = ds.pixel_array
        if (len(pixel_data.shape))==3:
            slice_index = pixel_data.shape[0] // 2
            selected_slice = pixel_data[slice_index, :, :]
            plt.imshow(selected_slice, cmap=plt.cm.bone)
        else:
            plt.imshow(imagen, cmap = plt.cm.bone)
        plt.axis('off')
        plt.savefig("temp_image.png")
    
=======
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
>>>>>>> 80b97d98510193c60c281a3ecfccd4c633db6514
