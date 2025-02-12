from PyQt6.QtWidgets import (
    QLabel
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, QObject

from typing import List
from PIL import ImageQt, Image
from pdf2image import convert_from_path
import zipfile
import io

class SchematicViewModel(QObject):
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.__index__ = 0
        self.__pil_imgs__: List[Image.Image] = []
        self.__scale_factor__ = 1.0

    def save(self, zf: zipfile.ZipFile):
        try:
            for index, pil_img in enumerate(self.__pil_imgs__):
                img_buffer = io.BytesIO()
                pil_img.save(img_buffer, format="PNG")
                zf.writestr(f"{index}.png", img_buffer.getvalue())
        except ValueError as e:
            raise e
    
    def clear(self):
        self.update_imgs(imgs=[])

    def update_imgs(self, imgs: List[Image.Image]):
        self.__pil_imgs__ = imgs
        self.__index__ = 0
        self.__scale_factor__ = 1.0
        self.data_changed.emit()
    
    def import_as_img(self, pdf_file_path: str):
        self.__pil_imgs__ = convert_from_path(pdf_file_path)
        self.__index__ = 0
        self.__scale_factor__ = 1.0

    def increase_index(self):
        if self.__pil_imgs__:
            self.__index__ =  min(len(self.__pil_imgs__) - 1, self.__index__ + 1)
    
    def decrease_index(self):
        if self.__pil_imgs__:
            self.__index__ = max(0, self.__index__ - 1)
    
    def get_image(self) -> QLabel:
        if self.__pil_imgs__:
            pil_img = self.__pil_imgs__[self.__index__].convert("RGBA")
            q_image = ImageQt.ImageQt(pil_img)
            img_label = QLabel()
            img_label.setPixmap(QPixmap.fromImage(q_image))
            img_label.setScaledContents(True)
            new_width = int(img_label.width() * self.__scale_factor__)
            new_height = int(img_label.height() * self.__scale_factor__)
            img_label.resize(new_width, new_height)
            return img_label
    
    def scale_up(self):
        self.__scale_factor__ = min(10.0, self.__scale_factor__ * 1.1)
    
    def scale_down(self):
        self.__scale_factor__ = max(0.9, self.__scale_factor__/1.1)

    def get_page_num(self):
        return self.__index__ + 1