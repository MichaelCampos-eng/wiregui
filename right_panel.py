from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtGui import QAction, QIcon
from wrman.converter.ditmco_test import *
from wrman.conn_management.list_manager import *
from table_views import *
from list_view_model import AggregateModel

class RightPanel(QWidget):

    def __init__(self, parent):
        super().__init__()

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

        self.wire_list_view = WireListView(self)
        self.unused_list_view = UnusedListView(self)
        self.ground_list_view = GroundListView(self)
        self.agg_model = AggregateModel(self.wire_list_view.list_model,
                                        self.unused_list_view.list_model,
                                        self.ground_list_view.list_model)

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
            self.agg_model.set_file_path(folder_path)
            self.agg_model.export_spreadsheets()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def __export_tests_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self,
                                              "Save File",
                                              f"{self.agg_model.get_name()}.ro",
                                              "RO Files (*.ro)")
        try:
            self.agg_model.set_file_path(file_path)
            self.agg_model.export_tests()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
