from PyQt6.QtWidgets import ( 
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
    QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from typing import List
from pdf2image import convert_from_path

class SchematicView(QWidget):
    #File_path should point to a pdf convert it some images
    def __init__(self, file_path: str):
        super().__init__()
        self.index = 0
        self.pil_imgs = convert_from_path(file_path)
        
        
        

    def pil_to_qimage(pil_image):
        pil_image = pil_image.convert("RGBA")  # Ensure the image has RGBA mode
        data = pil_image.tobytes("raw", "RGBA")
        qim = QImage(data, pil_image.width, pil_image.height, pil_image.width * 4, QImage.Format.Format_RGBA8888)
        return qim