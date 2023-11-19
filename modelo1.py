#modelo
from PyQt5.QtCore import QObject
import pydicom
import matplotlib.pyplot as plt
import os
class DICOMModel:
    def __init__(self):
            super().__init__()
            self.dicom_data = None

    def load_dicom_folder(self, folder_path):
        try:
            dicom_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.dcm')]
            self.dicom_data = [pydicom.dcmread(file) for file in dicom_files]
            return True
        except Exception as e:
            self.dicom_data = None
            return str(e)