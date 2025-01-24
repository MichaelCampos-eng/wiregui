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
        self.setWindowTitle("New Project")
        self.resize(1000, 600)

        main_layout = QHBoxLayout()


        left_panel_layout = QVBoxLayout()
        self.schematic = SchematicView()
        self.schematic.import_schematic("schem.pdf")
        left_panel_layout.addWidget(self.schematic)
        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(WireListView())
        right_panel_layout.addWidget(UnusedListView())
        right_panel_layout.addWidget(GroundListView())
        right_panel_layout.addStretch()

        left_panel_widget = QWidget()
        left_panel_widget.setLayout(left_panel_layout)
        right_panel_widget = QWidget()
        right_panel_widget.setLayout(right_panel_layout)

        self.schematic.show_check_box.clicked.connect(self.rearrange)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(left_panel_widget)
        self.splitter.addWidget(right_panel_widget)
        self.splitter.setSizes([400, 100])
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(self.splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        import_menu = menu.addMenu("&Import")
        export_menu = menu.addMenu("&Export")
    
    def rearrange(self):
        if self.schematic.show_check_box.isChecked():
            self.splitter.setOrientation(Qt.Orientation.Horizontal)
            self.splitter.setSizes([400, 100])
            self.splitter.setStretchFactor(0, 2)
            self.splitter.setStretchFactor(1, 1)
            self.resize(1000, 600)
        else:
            self.splitter.setOrientation(Qt.Orientation.Vertical)
            self.splitter.setSizes([100, 1000])
            self.splitter.setStretchFactor(0, 1)
            self.splitter.setStretchFactor(1, 10)
            self.resize(300, 600)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()