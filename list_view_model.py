from wrman.conn_management.list_manager import *
from wrman.config_classes.config import *
from wrman.converter.ditmco_test import *

from utils import *

class ListViewModel:

    def __init__(self):
        self.__table__: DitmcoList
        self.__test__: DitmcoRo
             
    def get_df(self):
        return self.__table__.get_df()
    
    def append(self, arg):
        self.__table__.step(arg)
    
    def get_name(self):
        return self.__table__.get_list_name()
    
    def get_placeholder(self):
        return self.__table__.fetch_hint_txt()

    def export_test(self, file_path):
        try:
            self.__test__.export_test(file_path)
        except ValueError as e:
            raise e

    def export_spreadsheet(self, file_path):
        try:
            if self.__table__.get_df().empty:
                raise ValueError("Cannot export empty {}.".format(self.get_name()))
            self.__table__.save_list(file_path)
        except ValueError as e:
            raise e

    def import_spreadsheet(self, file_path):
        try:
            self.__table__.load_list(file_path)
        except ValueError as e:
            raise e

class WireListViewModel(ListViewModel):
    def __init__(self, cfg: Config):
        super().__init__()
        table = WireList()
        self.__table__ = table
        self.__test__ = WireListRo(cfg, table.get_df())

class UnusedListViewModel(ListViewModel):
    def __init__(self, cfg: Config):
        super().__init__()
        table = IsolatedList()
        self.__table__ = table
        self.__test__ = UnusedListRo(cfg, table.get_df())
    

class GroundListViewModel(ListViewModel):
    def __init__(self, cfg: Config):
        super().__init__()
        table = GroundList()
        self.__table__ = table
        self.__cfg__.continuity_cfg.update_block_name("GROUND_CONTINUITY_TESTS")
        self.__test__ = GroundListRo(self.__cfg__, table.get_df())