from PyQt6.QtWidgets import ( 
    QApplication, 
    QMainWindow, 
    QWidget,
    QHBoxLayout,
    QSplitter,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from PIL import Image


from right_panel import RightPanelView
from left_panel import LeftPanelView

import zipfile
import json
import io
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.project_name = "New Project"

        central_widget = QWidget()
        self.setWindowTitle(self.project_name)
        self.resize(1000, 600)
        self.__set_menu_bar__()
    
        main_layout = QHBoxLayout()

        self.right_panel_widget = RightPanelView(self)
        self.left_panel_widget = LeftPanelView(self)
        self.left_panel_widget.open.connect(self.rearrange)
        self.left_panel_widget.view_changed.connect(self.__toggle_menu__)
        self.right_panel_widget.view_changed.connect(self.__toggle_menu__)

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
        self.new_proj_action.triggered.connect(self.__create_new__)
        self.new_proj_action.setEnabled(False)

        self.save_action = QAction(QIcon("open.png"), "&Save", self)
        self.save_action.setStatusTip("Save")
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

    def __toggle_menu__(self):
        self.setWindowTitle(f"{self.project_name} *")
        self.save_action.setEnabled(True)

    def __open_project__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getOpenFileName(self, 
                                              "Open Project",
                                              ".",
                                              "Project Files (*.tb)")
        if file_path:
            try:
                with zipfile.ZipFile(file_path, "r") as zf:
                    imgs = []
                    for file_name in zf.namelist():
                        with zf.open(file_name) as file:
                            if file_name.endswith(".png"):
                                imgs.append(Image.open(io.BytesIO(file.read())))
                            elif file_name.endswith(".parquet"):
                                self.right_panel_widget.view_model.open_parquet(file_name, file)
                            elif file_name.endswith(".json"):
                                self.__load_meta_data__(file)
                    self.left_panel_widget.view_model.open_images(imgs)
                    self.new_proj_action.setEnabled(True)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
            
    def __save_as__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self,
                                              "Save File",
                                              "new_project.tb",
                                              "TB Files (*.tb)")
        if file_path:
            if self.file_path == "":
                self.file_path = file_path
                self.project_name = os.path.basename(file_path).split(".")[0]
                self.setWindowTitle(self.project_name)
                self.__save__()
            else:
                root = self.file_path
                self.file_path = file_path
                self.__save__()
                self.file_path = root

    def __save__(self):
        try:
            with zipfile.ZipFile(self.file_path, "w") as zf:
                self.__save_meta_data__(zf)
                self.right_panel_widget.view_model.save(zf)
                self.left_panel_widget.view_model.save(zf)
                self.save_action.setEnabled(False)
                self.new_proj_action.setEnabled(True)
                self.setWindowTitle(self.project_name)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def __save_meta_data__(self, zf: zipfile.ZipFile):
        meta_data = {
            "project_name": self.project_name,
            "file_path": self.file_path
        }
        json_str = json.dumps(meta_data, indent=4)
        buffer = io.BytesIO()
        buffer.write(json_str.encode("utf-8"))
        buffer.seek(0)
        zf.writestr("metadata.json", buffer.getvalue())

    def __load_meta_data__(self, file: zipfile.ZipExtFile):
        meta_data = json.load(file)
        self.project_name = meta_data["project_name"]
        self.file_path = meta_data["file_path"]
        self.setWindowTitle(self.project_name)

    def __is_new_file__(self):
        return not self.file_path

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
                if self.__is_new_file__():
                    self.__save_as__()
                else:
                    self.__save__()
        self.project_name = "New Project"
        self.file_path = ""
        self.left_panel_widget.view_model.clear()
        self.right_panel_widget.view_model.clear()
                    

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