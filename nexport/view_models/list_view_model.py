from PyQt6.QtCore import QObject, pyqtSignal
from wrman.conn_management.list_manager import *
from wrman.config_classes.config import *
from wrman.converter.ditmco_test import *
from ..utils.utils import *
import zipfile
import io

class ListViewModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__cfg__: Config
        self.__table__: DitmcoList
        self.__ro__: DitmcoRo

    def get_test(self):
        return self.__ro__.get_test()
    
    def is_table_empty(self):
        return self.__table__.manager.is_df_empty()
             
    def get_df(self):
        return self.__table__.manager.get_df()
    
    def get_name(self):
        return self.__table__.manager.get_table_name()
    
    def get_placeholder(self):
        return self.__table__.fetch_hint_txt()

    def append(self, arg):
        self.__table__.step(arg)
        self.data_changed.emit()
    
    def export_ro_file(self, file_path):
        try:
            self.__ro__.export(file_path)
        except ValueError as e:
            raise e

    def export_spreadsheet(self, file_path):
        try:
            if self.__table__.manager.is_df_empty():
                raise ValueError("Cannot export empty {}.".format(self.get_name()))
            self.__table__.save_list(file_path)
        except ValueError as e:
            raise e

    def import_spreadsheet(self, file_path):
        try:
            self.__table__.load_list(file_path)
            self.data_changed.emit()
        except ValueError as e:
            raise e
        
    def open_parquet(self, file: zipfile.ZipExtFile):
        self.__table__.load_parquet(file)
        self.data_changed.emit()

    def zip_parquet(self, zf: zipfile.ZipFile):
        buffer = io.BytesIO()
        df: pd.DataFrame = self.get_df()
        df.to_parquet(buffer, engine="pyarrow")
        buffer.seek(0)
        zf.writestr(f"{self.get_name()}.parquet", buffer.getvalue())

    def clear(self):
        self.__table__.clear()
        self.data_changed.emit()

class WireListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        cfg = fetch_wire_list_cfg()
        table = WireList()

        self.__cfg__ = cfg
        self.__table__ = table
        self.__ro__ = WireListRo(cfg, table.manager)

class UnusedListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        cfg = fetch_unused_list_cfg()
        table = IsolatedList()

        self.__cfg__ = cfg
        self.__table__ = table
        self.__ro__ = UnusedListRo(cfg, table.manager)
    

class GroundListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        cfg = fetch_grd_list_cfg()
        table = GroundList()

        self.__cfg__ = cfg
        self.__table__ = table
        self.__ro__ = GroundListRo(cfg, table.manager)