from PyQt6.QtWidgets import ( 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QCheckBox,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QPalette, QKeyEvent, QIcon
from schematic_view_model import SchematicViewModel
import qtawesome as qta

class SchematicView(QWidget):
    view_changed = pyqtSignal()

    def __init__(self, grandparent):
        super().__init__()
        self.view_model = SchematicViewModel()

        layout = QVBoxLayout()

        open_pdf_action = QAction(QIcon("open.png"), "&Document", self)
        open_pdf_action.setStatusTip(f"Open schematic")
        open_pdf_action.triggered.connect(self.__open_pdf_dialog__)
        grandparent.open_menu.addAction(open_pdf_action)

        open_img_action = QAction(QIcon("open.png"), "&Image", self)
        open_img_action.setStatusTip(f"Open schematic")
        open_img_action.triggered.connect(self.__open_img_dialog__)
        grandparent.open_menu.addAction(open_img_action)

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
        left_arrow.setIcon(qta.icon("fa.arrow-circle-left"))
        left_arrow.setToolTip("Previous page")
        left_arrow.clicked.connect(self.__traverse_left__)
        right_arrow = QPushButton()
        right_arrow.setIcon(qta.icon("fa.arrow-circle-right"))
        right_arrow.setToolTip("Next page")
        right_arrow.clicked.connect(self.__traverse_right__)
        self.page_num = QLabel(f"Page {self.view_model.get_page_num()}")

        btns_layout.addWidget(left_arrow)
        btns_layout.addWidget(self.page_num)
        btns_layout.addWidget(right_arrow)

        btns_layout.addStretch()

        mag_min = QPushButton()
        mag_min.setIcon(qta.icon("fa.minus-circle"))
        mag_min.setToolTip("Zoom out")
        mag_min.clicked.connect(self.__zoom_out__)
        mag_plus = QPushButton()
        mag_plus.setIcon(qta.icon("fa.plus-circle"))
        mag_plus.setToolTip("Zoom in")
        mag_plus.clicked.connect(self.__zoom_in__)

        btns_layout.addWidget(mag_min)
        btns_layout.addWidget(mag_plus)

        self.btns_widget.setLayout(btns_layout)

        layout.addLayout(display_layout)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.btns_widget)
        self.setLayout(layout)

    def __import_schematic__(self, path: str):
        self.view_model.import_as_img(pdf_file_path=path)
        self.__set_tool_bar__()
        self.view_changed.emit()
    
    def __toggle_img__(self):
        self.__show_image__() if self.show_check_box.isChecked() else self.__hide_image__()

    def __hide_image__(self):
        self.scroll_area.hide(), self.btns_widget.hide()
    
    def __show_image__(self):
        self.scroll_area.show(), self.btns_widget.show()

    def __traverse_left__(self):
        self.view_model.decrease_index()
        self.__set_tool_bar__()

    def __traverse_right__(self):
        self.view_model.increase_index()
        self.__set_tool_bar__()

    def __set_tool_bar__(self):
        img_label = self.view_model.get_image()
        self.scroll_area.setWidget(img_label)
        self.page_num.setText(f"Page {self.view_model.get_page_num()}")
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() in [Qt.Key.Key_Plus, Qt.Key.Key_Equal]:
                self.__zoom_in__()
            elif event.key() == Qt.Key.Key_Minus:
                self.__zoom_out__()
    
    def __zoom_in__(self):
        self.view_model.scale_up()
        self.scroll_area.setWidget(self.view_model.get_image())
    
    def __zoom_out__(self):
        self.view_model.scale_down()
        self.scroll_area.setWidget(self.view_model.get_image())

    def __open_img_dialog__(self):
        pass

    def __open_pdf_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getOpenFileName(self,
                                              "Open schematic",
                                              "",
                                              "PDF Files (*.pdf)")
        try:
            self.__import_schematic__(path=file_path)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))