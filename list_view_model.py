from wrman.conn_management.list_manager import *
from wrman.config_classes.config import *
from wrman.converter.ditmco_test import *
from omegaconf import OmegaConf

class ListViewModel():

    def __init__(self):
        self.table: DitmcoList = None
        self.cfg: Config = None
        self.__set_config_default__()

    def __set_config_default__(self):
        with open("config.yaml", 'r') as file:
            self.cfg = OmegaConf.load(file)
            
    def get_df(self):
        return self.table.get_df()
    
    def append(self, arg):
        self.table.step(arg)
    
    def get_name(self):
        return self.table.get_list_name()
    
    def get_placeholder(self):
        return self.table.fetch_hint_txt()

    def export_test(self):
        pass

    def export_spreadsheet(self):
        try:
            self.table.save_list(self.cfg.results_path)
        except ValueError as e:
            raise e

    def import_spreadsheet(self):
        try:
            self.table.load_list(self.cfg.results_path)
        except ValueError as e:
            raise e

    def set_file_path(self, path):
        self.cfg.results_path = path

class WireListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        self.table = WireList()
    
    def export_test(self):
        try:
            test = WireListRo(self.cfg, self.table.get_df())
            test.export_test()
        except ValueError as e:
            raise e

    def import_list(self):
        pass

class UnusedListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        self.table = IsolatedList()
    
    def export_test(self):
        try:
            test = UnusedListRo(self.cfg, self.table.get_df())
            test.export_test()
        except ValueError as e:
            raise e
        
    def import_list(self):
        pass

class GroundListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        self.table = GroundList()
    
    def export_test(self):
        try:
            test = GroundListRo(self.cfg, self.table.get_df())
            test.export_test()
        except ValueError as e:
            raise e
         
    def import_list(self):
        pass

class AggregateModel:
    def __init__(self, 
                 wire_list: ListViewModel, 
                 unused_list_df: ListViewModel, 
                 ground_list_df: ListViewModel):
        self.wire_model = wire_list
        self.isolated_model = unused_list_df
        self.grd_model = ground_list_df
        self.cfg: Config
        self.error_str = "Empty tables"
        self.__set_config_default__()
        self.__name__ = "Aggregate"
    
    def get_name(self):
        return self.__name__

    def __set_config_default__(self):
        with open('config.yaml', 'r') as file:
            self.cfg = OmegaConf.load(file)
    
    def export_spreadsheets(self):
        try:
            if not self.wire_model.get_df().empty:
                self.cfg.results_path = "/".join(self.cfg.results_path.split("/")[:-1]) + f"/{self.wire_model.get_name()}" 
                self.wire_model.export_spreadsheet()
            if not self.isolated_model.get_df().empty:
                self.cfg.results_path = "/".join(self.cfg.results_path.split("/")[:-1]) + f"/{self.isolated_model.get_name()}"
                self.isolated_model.export_spreadsheet()
            if not self.grd_model.get_df().empty:
                self.cfg.results_path = "/".join(self.cfg.results_path.split("/")[:-1]) + f"/{self.grd_model.get_name()}"
                self.grd_model.export_spreadsheet()
        except ValueError as e:
            raise e

    def export_tests(self):
        try:
            AggregateRo(self.cfg,
                        self.wire_model.get_df(),
                        self.isolated_model.get_df(),
                        self.grd_model.get_df()).export_test()
        except ValueError as e:
            raise e

    def set_file_path(self, path):
        self.cfg.results_path = path