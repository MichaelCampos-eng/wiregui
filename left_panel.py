from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QMessageBox
)

from PyQt6.QtGui import QAction, QIcon
from schematic_views import *

class LeftPanelView(QWidget):

    def __init__(self, parent):
        super().__init__()
        left_panel_layout = QVBoxLayout()
        self.schematic = SchematicView()
        self.open = self.schematic.show_check_box.clicked
        left_panel_layout.addWidget(self.schematic)
        self.setLayout(left_panel_layout)

        open_pdf_action = QAction(QIcon("open.png"), "&Document", self)
        open_pdf_action.setStatusTip(f"Open schematic")
        open_pdf_action.triggered.connect(self.__open_pdf_dialog__)
        parent.open_menu.addAction(open_pdf_action)

        open_img_action = QAction(QIcon("open.png"), "&Image", self)
        open_img_action.setStatusTip(f"Open schematic")
        open_img_action.triggered.connect(self.__open_img_dialog__)
        parent.open_menu.addAction(open_img_action)


    def __open_img_dialog__(self):
        pass
    
    def __open_pdf_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getOpenFileName(self,
                                              "Open scbematic",
                                              "",
                                              "PDF Files (*.pdf)")
        if file_path:
            try:
                self.schematic.import_schematic(file_path)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

        
    def isChecked(self):
        return self.schematic.show_check_box.isChecked()