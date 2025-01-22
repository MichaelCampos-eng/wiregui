from PyQt6.QtWidgets import ( 
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QCheckBox
)

import sys
from wrman.converter.ditmco_test import *
from wrman.pin_management.list_manager import *
from table_views import *
from schematic_views import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        central_widget = QWidget()
        
        main_layout = QHBoxLayout()
        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(WireListView()), right_panel_layout.addWidget(UnusedListView()), right_panel_layout.addWidget(GroundListView())
        main_layout.addWidget(SchematicView(self.file_path))
        left_panel = SchematicView(self.file_path)
        main_layout.addWidget(left_panel), main_layout.addLayout(right_panel_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()