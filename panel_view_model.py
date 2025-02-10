from omegaconf import OmegaConf
from list_view_model import *

class RightPanelViewModel:
    def __init__(self):
        self.__wire_model__: WireListViewModel
        self.__isolated_model__: UnusedListViewModel
        self.__grd_model__: GroundListViewModel
        self.__cfg__: Config
        self.error_str = "Empty tables"
        self.__name__ = "Tables"
        self.__set_config_default__()
        self.__set_submodels__()

    def __set_config_default__(self):
        try:
            self.__cfg__ = open_config("config.yaml")
        except ValueError as e:
            raise e
    
    def __set_submodels__(self):
        self.__wire_model__ = WireListViewModel(self)
        self.__isolated_model__ = UnusedListViewModel()
        self.__grd_model__ = GroundListViewModel()

    def get_name(self):
        return self.__name__
    
    def export_spreadsheets(self, folder_path: str):
        try:
            if not self.__wire_model__.get_df().empty:
                self.__wire_model__.export_spreadsheet(folder_path + f"/{self.__wire_model__.get_name()}.csv" )
            if not self.__isolated_model__.get_df().empty:
                self.__isolated_model__.export_spreadsheet(folder_path + f"/{self.__isolated_model__.get_name()}.csv")
            if not self.__grd_model__.get_df().empty:
                self.__grd_model__.export_spreadsheet(folder_path + f"/{self.__grd_model__.get_name()}.csv")
        except ValueError as e:
            raise e

    # TODO: figure out what to do with config
    def export_tests(self, file_path: str):
        try:
            cfg = self.__wire_model__.set_file_path(file_path)
            AggregateRo(self.__cfg__,
                        self.__wire_model__.get_df(),
                        self.__isolated_model__.get_df(),
                        self.__grd_model__.get_df()).export_test()
        except ValueError as e:
            raise e
    
    def get_wire_model(self):
        return self.__wire_model__

    def get_isolated_model(self):
        return self.__isolated_model__
    
    def get_grd_model(self):
        return self.__grd_model__