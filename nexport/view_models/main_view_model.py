from PyQt6.QtCore import pyqtSignal, QObject
import zipfile
import json
import io
import os
from nexport.view_models.panel_view_model import *

class MainViewModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__right_panel_model__ = RightPanelViewModel()
        self.__left_panel_model__ = LeftPanelViewModel()

        self.__right_panel_model__.data_changed.connect(self.__data_change__)
        self.__left_panel_model__.data_changed.connect(self.__data_change__)

        self.__file_path__ = ""
        self.__project_name__ = "New Project"

    def __data_change__(self):
        self.data_changed.emit()
    
    def get_right_panel_model(self) -> RightPanelViewModel:
        return self.__right_panel_model__

    def get_left_panel_model(self) -> LeftPanelViewModel:
        return self.__left_panel_model__

    def get_name(self):
        return "NeXport | " + self.__project_name__
    
    def is_new_file(self):
        return not self.__file_path__
    
    def update_name(self, file_path):
        self.__project_name__ = os.path.basename(file_path).split(".")[0]

    def update_file_path(self, file_path):
        self.__file_path__ = file_path
    
    def save_meta_data(self, zf: zipfile.ZipFile):
        meta_data = {
            "project_name": self.__project_name__,
            "file_path": self.__file_path__
        }
        json_str = json.dumps(meta_data, indent=4)
        buffer = io.BytesIO()
        buffer.write(json_str.encode("utf-8"))
        buffer.seek(0)
        zf.writestr("metadata.json", buffer.getvalue())

    def load_meta_data(self, file: zipfile.ZipExtFile):
        meta_data = json.load(file)
        self.__project_name__ = meta_data["project_name"]
        self.__file_path__ = meta_data["file_path"]

    def save(self):
        with zipfile.ZipFile(self.__file_path__, "w") as zf:
                self.save_meta_data(zf)
                self.__left_panel_model__.save(zf)
                self.__right_panel_model__.save(zf)

    def save_as(self, file_path):
        if self.is_new_file():
            self.update_name(file_path)
            self.update_file_path(file_path)
            self.save()
        else:
            orig_path = self.__file_path__
            orig_name = self.get_name()
            self.update_file_path(file_path)
            self.update_name(file_path)
            self.save()
            self.update_file_path(orig_path)
            self.update_name(orig_name)
    
    def open_project(self, file_path):
        with zipfile.ZipFile(file_path, "r") as zf:
            imgs = []
            for file_name in zf.namelist():
                with zf.open(file_name) as file:
                    if file_name.endswith(".png"):
                        imgs.append(Image.open(io.BytesIO(file.read())))
                    elif file_name.endswith(".parquet"):
                        self.__right_panel_model__.open_parquet(file_name, file)
                    elif file_name.endswith(".json"):
                        self.load_meta_data(file)
            self.__left_panel_model__.open_images(imgs)
    
    def reset(self):
        self.__project_name__ = "New Project"
        self.__file_path__ = ""
        self.__left_panel_model__.clear()
        self.__right_panel_model__.clear()