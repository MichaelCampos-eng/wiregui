from wrman.pin_management.list_manager import *
from wrman.config_classes.config import *
from wrman.converter.ditmco_test import *
import yaml


class AggregateModel:
    def __init__(self, wire_list_df: pd.DataFrame, unused_list_df: pd.DataFrame, ground_list_df: pd.DataFrame):
        self.wire_list_df = wire_list_df
        self.unused_list_df = unused_list_df
        self.ground_list_df = ground_list_df
        self.cfg: Config
        self.__set_config_fault__()

    def __set_config_fault__(self):
        with open('config.yaml', 'r') as file:
            self.cfg = yaml.safe_load(file)

    def export_lists(self):
        txt = AggregateRo(self.cfg,
                           self.wire_list_df,
                           self.unused_list_df,
                           self.ground_list_df)
        if txt != "":
            raise ValueError(self.error_str)
        with open(self.cfg.results_path, 'w') as file:
            file.write(txt)
    
    def import_lists(self):
        pass

class ListViewModel():
    def __init__(self):
        self.table: DitmcoList = None
        self.cfg: Config = None
        self.__set_config_fault__()

    def __set_config_fault__(self):
        with open('config.yaml', 'r') as file:
            self.cfg = yaml.safe_load(file)

    def get_df(self):
        return self.table.get_df()
    
    def append(self, arg):
        self.table.step(arg)
    
    def get_name(self):
        return self.table.get_list_name()
    
    def get_placeholder(self):
        return self.table.fetch_curr_arg_name()

    def export_list(self):
        pass

    def import_list(self):
        pass

    

class WireListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        self.table = WireList()
    
    def export_list(self):
        test = WireListRo(self.cfg, self.table.get_df())
        test.export_test()

    def import_list(self):
        pass

class UnusedListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        self.table = IsolatedList()
    
    def export_list(self):
        test = UnusedListRo(self.cfg, self.table.get_df())
        test.export_test()

    def import_list(self):
        pass

class GroundListViewModel(ListViewModel):
    def __init__(self):
        super().__init__()
        self.table = GroundList()
    
    def export_list(self):
        test = GroundListRo(self.cfg, self.table.get_df())
        test.export_test()
    
    def import_list(self):
        pass