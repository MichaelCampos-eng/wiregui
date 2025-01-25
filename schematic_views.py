from PyQt6.QtWidgets import ( 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QWheelEvent, QKeySequence, QKeyEvent
from typing import List
from pdf2image import convert_from_path
from PIL import ImageQt, Image
import os

class SchematicView(QWidget):

    def __init__(self):
        super().__init__()
        self.index = 0
        self.pil_imgs: List[Image.Image] = None
        self.scale_factor = 1.0

        layout = QVBoxLayout()

        display_layout = QHBoxLayout()
        project_name = QLabel("Schematic")
        toggle_name = QLabel("Show")
        self.show_check_box = QCheckBox()
        self.show_check_box.setChecked(True)
        self.show_check_box.clicked.connect(self.__toggle_img__)
        display_layout.addWidget(project_name)
        display_layout.addStretch()
        display_layout.addWidget(toggle_name)
        display_layout.addWidget(self.show_check_box)
       
        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)

        btns_layout = QHBoxLayout()
        self.btns_widget = QWidget()
        left_arrow = QPushButton()
        left_arrow.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowLeft))
        left_arrow.setToolTip("Previous page")
        left_arrow.clicked.connect(self.__traverse_left__)
        right_arrow = QPushButton()
        right_arrow.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ArrowRight))
        right_arrow.setToolTip("Next page")
        right_arrow.clicked.connect(self.__traverse_right__)
        self.page_num = QLabel("Page " + str(self.index))
        btns_layout.addWidget(left_arrow)
        btns_layout.addWidget(self.page_num)
        btns_layout.addWidget(right_arrow)
        btns_layout.addStretch()
        self.btns_widget.setLayout(btns_layout)

        layout.addLayout(display_layout)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.btns_widget)
        self.setLayout(layout)

    def import_schematic(self, file_path: str):
        # name = os.path.splitext(file_path.split("/")[-1])[0]
        self.pil_imgs = convert_from_path(file_path)
        self.index = 0
        self.scale_factor = 1.0
        self.__set_tool_bar__()
    
    def __toggle_img__(self):
        self.__show_image__() if self.show_check_box.isChecked() else self.__hide_image__()

    def __hide_image__(self):
        self.scroll_area.hide(), self.btns_widget.hide()
    
    def __show_image__(self):
        self.scroll_area.show(), self.btns_widget.show()

    def __traverse_left__(self):
        if self.pil_imgs:
            self.index = max(0, self.index - 1)
            self.__set_tool_bar__()

    def __traverse_right__(self):
        if self.pil_imgs:
            self.index = min(len(self.pil_imgs) - 1, self.index + 1)
            self.__set_tool_bar__()

    def __set_tool_bar__(self):
        self.scale_factor = 1.0
        img_label = self.__get_image__()
        self.scroll_area.setWidget(img_label)
        self.page_num.setText("Page " + str(self.index))

    def __get_image__(self) -> QLabel:
        pil_img = self.pil_imgs[self.index].convert("RGBA")
        q_image = ImageQt.ImageQt(pil_img)
        img_label = QLabel()
        img_label.setPixmap(QPixmap.fromImage(q_image))
        img_label.setScaledContents(True)
        return img_label
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle zooming with the mouse wheel."""
        if event.angleDelta().y() > 0:  # Scroll up to zoom in
            self.scale_factor *= 1.1
        elif event.angleDelta().y() < 0:  # Scroll down to zoom out
            self.scale_factor /= 1.1

        # Limit zoom levels to reasonable bounds
        self.scale_factor = max(0.1, min(self.scale_factor, 10.0))

        # Resize the QLabel based on the scale factor
        
    
    def new_image_show(self):
        img = self.__get_image__()
        new_width = int(img.width() * self.scale_factor)
        new_height = int(img.height() * self.scale_factor)

        img.resize(new_width, new_height)
        self.scroll_area.setWidget(img)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle zooming with Ctrl + and Ctrl -."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Equal]:  # Ctrl +
                self.zoom_in()
            elif event.key() == Qt.Key.Key_Minus:  # Ctrl -
                self.zoom_out()
    
    def zoom_in(self):
        self.scale_factor = min(10.0, self.scale_factor * 1.1)
        self.new_image_show()
    
    def zoom_out(self):
        self.scale_factor = max(0.9, self.scale_factor/1.1)
        self.new_image_show()
