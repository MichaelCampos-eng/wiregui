from PyQt6.QtCore import pyqtSignal, QObject
from list_view_model import *
from schematic_view_model import SchematicViewModel
import zipfile
from PIL import Image

class LeftPanelViewModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.sch_model = SchematicViewModel()
        self.sch_model.data_changed.connect(self.__data_change__)

    def __data_change__(self):
        self.data_changed.emit()

    def save(self, zf: zipfile.ZipFile):
        self.sch_model.save(zf)

    def open_images(self, imgs: List[Image.Image]):
        self.sch_model.update_imgs(imgs)

    def get_sch_model(self):
        return self.sch_model
    
    def clear(self):
        self.sch_model.clear()

class RightPanelViewModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.error_str = "Empty tables"
        self.__name__ = "Tables"
        wire_model = WireListViewModel()
        isolated_model = UnusedListViewModel()
        grd_model = GroundListViewModel()

        self.__ro__: AggregateRo = AggregateRo(wire_model.get_test(),
                                               isolated_model.get_test(),
                                               grd_model.get_test())
        self.__wire_model__: WireListViewModel = wire_model
        self.__isolated_model__: UnusedListViewModel = isolated_model
        self.__grd_model__: GroundListViewModel = grd_model

        self.__wire_model__.data_changed.connect(self.__data_change__)
        self.__isolated_model__.data_changed.connect(self.__data_change__)
        self.__grd_model__.data_changed.connect(self.__data_change__)

    def __data_change__(self):
        self.data_changed.emit()

    def clear(self):
        self.__wire_model__.clear()
        self.__isolated_model__.clear()
        self.__grd_model__.clear()
            
    def get_name(self):
        return self.__name__
    
    def open_parquet(self, filename, file: zipfile.ZipExtFile):
        if self.__wire_model__.get_name() in filename:
            self.__wire_model__.open_parquet(file)
            self.__ro__.set_wire_test(self.__wire_model__.get_test())
        elif self.__isolated_model__.get_name() in filename:
            self.__isolated_model__.open_parquet(file)
            self.__ro__.set_iso_test(self.__isolated_model__.get_test())
        elif self.__grd_model__.get_name() in filename:
            self.__grd_model__.open_parquet(file)
            self.__ro__.set_grd_test(self.__grd_model__.get_test())
    
    def save(self, zf: zipfile.ZipFile):
        try:
            self.__wire_model__.zip_parquet(zf)
            self.__isolated_model__.zip_parquet(zf)
            self.__grd_model__.zip_parquet(zf)
        except ValueError as e:
            raise e

    def export_spreadsheets(self, folder_path: str):
        try:
            if not self.__wire_model__.is_table_empty():
                self.__wire_model__.export_spreadsheet(folder_path + f"/{self.__wire_model__.get_name()}.csv" )
            if not self.__isolated_model__.is_table_empty():
                self.__isolated_model__.export_spreadsheet(folder_path + f"/{self.__isolated_model__.get_name()}.csv")
            if not self.__grd_model__.is_table_empty():
                self.__grd_model__.export_spreadsheet(folder_path + f"/{self.__grd_model__.get_name()}.csv")
        except ValueError as e:
            raise e
        
    def export_ro_file(self, file_path: str):
        try:
            self.__ro__.export(file_path)
        except ValueError as e:
            raise e
    
    def get_wire_model(self):
        return self.__wire_model__

    def get_isolated_model(self):
        return self.__isolated_model__
    
    def get_grd_model(self):
        return self.__grd_model__
    