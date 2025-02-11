from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout
)

from schematic_views import *
from panel_view_model import LeftPanelViewModel

class LeftPanelView(QWidget):
    view_changed = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.view_model = LeftPanelViewModel()

        left_panel_layout = QVBoxLayout()
        self.schematic = SchematicView(parent, self.view_model.get_sch_model())
        self.schematic.view_changed.connect(self.__view_changed__)
        self.open = self.schematic.show_check_box.clicked
        left_panel_layout.addWidget(self.schematic)
        self.setLayout(left_panel_layout)

    def __view_changed__(self):
        self.view_changed.emit()

    def isChecked(self):
        return self.schematic.show_check_box.isChecked()