from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtGui import QAction, QIcon
from wrman.converter.ditmco_test import *
from wrman.conn_management.list_manager import *
from table_views import *
from panel_view_model import RightPanelViewModel

class RightPanelView(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.model = RightPanelViewModel()
        
        self.wire_list_view = WireListView(self, self.model.get_wire_model())
        self.unused_list_view = UnusedListView(self, self.model.get_isolated_model())
        self.ground_list_view = GroundListView(self, self.model.get_grd_model())

        self.csv_import_menu = parent.import_menu.addMenu("&Spreadsheet (.csv)")
        self.csv_export_menu = parent.export_menu.addMenu("&Spreadsheet (.csv)")
        self.test_export_menu = parent.export_menu.addMenu("&Test (.ro)")

        test_export_action = QAction(QIcon("open.png"), "&All", self)
        test_export_action.setStatusTip(f"Export test scrips all")
        test_export_action.triggered.connect(self.__export_tests_dialog__)
        
        table_export_action = QAction(QIcon("open.png"), "&All", self)
        table_export_action.setStatusTip(f"Export spreadsheets all")
        table_export_action.triggered.connect(self.__export_csvs_dialog__)

        self.csv_export_menu.addAction(table_export_action)
        self.test_export_menu.addAction(test_export_action)

        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(self.wire_list_view)
        right_panel_layout.addWidget(self.unused_list_view)
        right_panel_layout.addWidget(self.ground_list_view)
        right_panel_layout.addStretch()

        self.setLayout(right_panel_layout)

    def __export_csvs_dialog__(self):
        dialog = QFileDialog(self)
        folder_path = dialog.getExistingDirectory(self, "Select Folder")
        try:
            self.model.export_spreadsheets(folder_path)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def __export_tests_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self,
                                              "Save File",
                                              f"{self.model.get_name()}.ro",
                                              "RO Files (*.ro)")
        try:
            self.model.export_tests(file_path)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
