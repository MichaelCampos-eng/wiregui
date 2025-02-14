from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout
)

from nexport.views.schematic_views import *
from nexport.view_models.panel_view_model import LeftPanelViewModel

class LeftPanelView(QWidget):

    def __init__(self, parent, view_model: LeftPanelViewModel):
        super().__init__()
        self.view_model = view_model

        left_panel_layout = QVBoxLayout()
        self.schematic = SchematicView(parent, self.view_model.get_sch_model())
        self.open = self.schematic.show_check_box.clicked
        left_panel_layout.addWidget(self.schematic)
        self.setLayout(left_panel_layout)

    def isChecked(self):
        return self.schematic.show_check_box.isChecked()