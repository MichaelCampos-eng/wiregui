from PyQt6.QtWidgets import ( 
    QApplication, 
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter
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
        self.setWindowTitle("Schematic Test Converter")
        self.resize(1000, 500)

        main_layout = QHBoxLayout()

        left_panel = SchematicView()
        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(WireListView())
        right_panel_layout.addWidget(UnusedListView())
        right_panel_layout.addWidget(GroundListView())
        right_panel_layout.addStretch()
        right_panel = QWidget()
        right_panel.setLayout(right_panel_layout)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()