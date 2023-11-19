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
    
