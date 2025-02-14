from PyQt6.QtWidgets import (  
    QMainWindow, 
    QWidget,
    QHBoxLayout,
    QSplitter,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt

from ..view_models.main_view_model import MainViewModel
from .right_panel import RightPanelView
from .left_panel import LeftPanelView

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.view_model = MainViewModel()
        self.view_model.data_changed.connect(self.__toggle_save__)

        central_widget = QWidget()
        self.setWindowTitle(self.view_model.get_name())
        self.resize(1000, 600)
        self.__set_menu_bar__()
        self
    
        main_layout = QHBoxLayout()

        self.right_panel_widget = RightPanelView(self, self.view_model.get_right_panel_model())
        self.left_panel_widget = LeftPanelView(self, self.view_model.get_left_panel_model())
        self.left_panel_widget.open.connect(self.__rearrange__)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.left_panel_widget)
        self.splitter.addWidget(self.right_panel_widget)
        self.splitter.setSizes([400, 100])
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(self.splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def __set_menu_bar__(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        self.open_menu = file_menu.addMenu("&Open")

        open_project_action = QAction(QIcon("open.png"), "&Project", self)
        open_project_action.setStatusTip("Open Project")
        open_project_action.triggered.connect(self.__open_project__)

        self.open_menu.addAction(open_project_action)

        self.new_proj_action = QAction(QIcon("open.png"), "&New Project", self)
        self.new_proj_action.setStatusTip("Create a new project")
        self.new_proj_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_proj_action.triggered.connect(self.__create_new__)
        self.new_proj_action.setEnabled(False)

        self.save_action = QAction(QIcon("open.png"), "&Save", self)
        self.save_action.setStatusTip("Save")
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_action.triggered.connect(self.__save__)
        self.save_action.setEnabled(False)

        save_as_action = QAction(QIcon("open.png"), "&Save As", self)
        save_as_action.setStatusTip("Save As")
        save_as_action.triggered.connect(self.__save_as__)

        file_menu.addAction(self.new_proj_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(save_as_action)

        self.import_menu = menu.addMenu("&Import")
        self.export_menu = menu.addMenu("&Export")

    def __toggle_save__(self):
        self.save_action.setEnabled(True)
        self.new_proj_action.setEnabled(True)
        self.setWindowTitle(f"{self.view_model.get_name()} *")

    def __open_project__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getOpenFileName(self, 
                                              "Open Project",
                                              ".",
                                              "Project Files (*.tb)")
        if file_path:
            try:
                self.view_model.open_project(file_path)
                self.save_action.setEnabled(False)
                self.new_proj_action.setEnabled(True)
                self.setWindowTitle(self.view_model.get_name())
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
            
    def __save_as__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self,
                                              "Save File",
                                              "new_project.tb",
                                              "TB Files (*.tb)")
        if file_path:
            self.view_model.save_as(file_path)
            self.setWindowTitle(self.view_model.get_name())

    def __save__(self):
        try:
            if self.view_model.is_new_file():
                self.__save_as__()
            else:   
                self.view_model.save()
                self.save_action.setEnabled(False)
                self.new_proj_action.setEnabled(True)
                self.setWindowTitle(self.view_model.get_name())
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def __create_new__(self):
        if self.save_action.isEnabled():
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "Your project hasn't been saved. Do you want to save before continuing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Cancel:
                return
            if reply == QMessageBox.StandardButton.Yes:
                if self.view_model.is_new_file():
                    self.__save_as__()
                else:
                    self.__save__()
        self.view_model.reset()
        self.setWindowTitle(self.view_model.get_name())
        self.new_proj_action.setEnabled(False)
        self.save_action.setEnabled(False)

    def __rearrange__(self):
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

    def closeEvent(self, event):
        if self.save_action.isEnabled():
            reply = QMessageBox.question(self, "Unsaved Changes",
                                            "Your project hasn't been saved. Do you want to save before closing?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                            QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.__save_as__()
                event.accept()  # Accept the close event and close the window
            else:
                event.accept()