from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from schematic_views import *

class LeftPanel(QWidget):

    def __init__(self):
        super().__init__()
        left_panel_layout = QVBoxLayout()
        self.schematic = SchematicView()
        self.open = self.schematic.show_check_box.clicked
        self.schematic.import_schematic("schem.pdf")
        left_panel_layout.addWidget(self.schematic)
        self.setLayout(left_panel_layout)
        
    def isChecked(self):
        return self.schematic.show_check_box.isChecked()