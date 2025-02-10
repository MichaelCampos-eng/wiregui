from list_view_model import *
import pandas as pd
import io
import zipfile


class LeftPanelViewModel:
    def __init__(self):
        pass

    def save_as(self, zf: zipfile.ZipFile):
        pass

class RightPanelViewModel:
    def __init__(self):
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
        
        
    def get_name(self):
        return self.__name__
    

    def save_as(self, zf: zipfile.ZipFile):
        try:
            wire_buff = io.BytesIO()
            wire_list: pd.DataFrame = self.__wire_model__.get_df()
            wire_list.to_parquet(wire_buff, engine="pyarrow")
            zf.writestr(self.__wire_model__.get_name(), wire_buff.getvalue())

            iso_buff = io.BytesIO()
            iso_list: pd.DataFrame = self.__isolated_model__.get_df()
            iso_list.to_parquet(iso_buff, engine="pyarrow")
            zf.writestr(self.__isolated_model__.get_name(), iso_buff.getvalue())

            grd_buff = io.BytesIO()
            grd_list: pd.DataFrame = self.__grd_model__.get_df()
            grd_list.to_parquet(grd_buff, engine="pyarrow")
            zf.writestr(self.__grd_model__.get_name(), grd_buff.getvalue())
        except ValueError as e:
            raise e

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
    