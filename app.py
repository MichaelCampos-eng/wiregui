from PyQt6.QtWidgets import ( 
    QApplication, 
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QToolBar
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

import sys

from left_panel import LeftPanel
from right_panel import RightPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = ""

        central_widget = QWidget()
        self.setWindowTitle("New Project")
        self.resize(1000, 600)
        self.__set_menu_bar__()
    
        main_layout = QHBoxLayout()

        right_panel_widget = RightPanel(self)
        self.left_panel_widget = LeftPanel()
        self.left_panel_widget.open.connect(self.rearrange)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.left_panel_widget)
        self.splitter.addWidget(right_panel_widget)
        self.splitter.setSizes([400, 100])
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(self.splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        
    def __set_menu_bar__(self):
        open_action = QAction(QIcon("open.png"), "&Open", self)
        open_action.setStatusTip("Open project")
        open_action.triggered.connect(self.open)
        open_action.setCheckable(True)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(open_action)
        self.import_menu = menu.addMenu("&Import")
        self.export_menu = menu.addMenu("&Export")
        

    def open(self):
        pass

    def rearrange(self):
        if self.left_panel_widget.isChecked():
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