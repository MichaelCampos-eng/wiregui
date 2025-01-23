from PyQt6.QtWidgets import ( 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QIcon
from typing import List
from pdf2image import convert_from_path
from PIL import ImageQt, Image

class SchematicView(QWidget):
    #File_path should point to a pdf convert it some images
    def __init__(self):
        super().__init__()
        self.index = 0
        self.pil_imgs: List[Image.Image] = None

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)

        btns_layout = QHBoxLayout()
        left_arrow = QPushButton()
        left_arrow.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowLeft))
        left_arrow.setToolTip("Previous page")
        left_arrow.clicked.connect(self.__traverse_left__)
        right_arrow = QPushButton()
        right_arrow.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowRight))
        right_arrow.setToolTip("Next page")
        right_arrow.clicked.connect(self.__traverse_right__)
        self.page_num = QLabel("Page " + str(self.index))
        btns_layout.addWidget(left_arrow), btns_layout.addWidget(self.page_num), btns_layout.addWidget(right_arrow), btns_layout.addStretch()

        layout.addWidget(self.scroll_area), layout.addLayout(btns_layout)
        self.setLayout(layout)

    def import_schematic(self, file_path: str):
        convert_from_path(file_path)
        pass

    def __traverse_left__(self):
        if self.pil_imgs:
            self.index = max(0, self.index - 1)
            self.__set_tool_bar__()

    def __traverse_right__(self):
        if self.pil_imgs:
            self.index = min(len(self.pil_imgs) - 1, self.index + 1)
            self.__set_tool_bar__()

    def __set_tool_bar__(self):
        img_label = self.__get_image__()
        self.scroll_area.setWidget(img_label)
        self.page_num.setText("Page " + str(self.index))

    def __get_image__(self) -> QLabel:
        qimage = ImageQt.ImageQt(self.pil_imgs[self.index])
        img_label = QLabel()
        img_label.setPixmap(QPixmap.fromImage(qimage))
        return img_label
    

    # def pil_to_qimage(pil_image):
    #     pil_image = pil_image.convert("RGBA")  # Ensure the image has RGBA mode
    #     data = pil_image.tobytes("raw", "RGBA")
    #     qim = QImage(data, pil_image.width, pil_image.height, pil_image.width * 4, QImage.Format.Format_RGBA8888)
    #     return qim