from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
    QTableView,
    QHeaderView,
    QMessageBox,
    QFileDialog
)
from PyQt6.QtGui import QAction, QIcon
from pandas_model import *
from list_view_model import *

class ListView(QWidget):
    
    def __init__(self, parent, model: ListViewModel):
        super().__init__()
        self.view_model: ListViewModel = model
        self.view_model.data_changed.connect(self.__new_table_view__)

        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        table_name = QLabel(self.view_model.get_name())
        table_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toggle_name = QLabel("Show")
        self.check_box = QCheckBox()
        self.check_box.setChecked(True)
        self.check_box.clicked.connect(self.__toggle_table__)
        header_layout.addWidget(table_name)
        header_layout.addStretch()
        header_layout.addWidget(toggle_name)
        header_layout.addWidget(self.check_box)

        self.table_view = QTableView()
        self.model = PandasModel(self.view_model.get_df())
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        input_layout = QVBoxLayout()
        self.user_input_box = QLineEdit()
        self.user_input_box.setPlaceholderText(self.view_model.get_placeholder())
        self.user_input_box.returnPressed.connect(self.__user_input__)
        input_layout.addWidget(self.user_input_box)
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        import_csv_action = QAction(QIcon("open.png"), f"&{self.view_model.get_name()}", self)
        import_csv_action.setStatusTip(f"Export {self.view_model.get_name()}")
        import_csv_action.triggered.connect(self.__import_csv_dialog__)    

        export_csv_action = QAction(QIcon("open.png"), f"&{self.view_model.get_name()}", self)
        export_csv_action.setStatusTip(f"Export test script {self.view_model.get_name()}")
        export_csv_action.triggered.connect(self.__export_csv_dialog__)

        export_test_action = QAction(QIcon("open.png"), f"&{self.view_model.get_name()}", self)
        export_test_action.setStatusTip(f"Export test script {self.view_model.get_name()}")
        export_test_action.triggered.connect(self.__export_ro_dialog__)

        parent.csv_import_menu.addAction(import_csv_action)
        parent.csv_export_menu.addAction(export_csv_action)
        parent.test_export_menu.addAction(export_test_action)

    def __user_input__(self):
        try:
            self.view_model.append(self.user_input_box.text())
            self.__new_table_view__()
            
        except ValueError as e:
            QMessageBox.critical(self, "Input List Error", str(e))

    def __new_table_view__(self):
        try:
            self.model = PandasModel(self.view_model.get_df())
            self.table_view.setModel(self.model)
            self.table_view.scrollToBottom()
            self.__input_placeholder__()
        except ValueError as e:
            raise e
    
    def __input_placeholder__(self):
        self.user_input_box.clear()
        self.user_input_box.setPlaceholderText(self.view_model.get_placeholder())

    def __toggle_table__(self):
        self.table_view.show() if self.check_box.isChecked() else self.table_view.hide()

    def __import_csv_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getOpenFileName(self,
                                              "Open spreadsheet",
                                              "",
                                              "CSV Files (*.csv)")
        if file_path:
            try:
                self.view_model.import_spreadsheet(file_path)
                self.model = PandasModel(self.view_model.get_df())
                self.table_view.setModel(self.model)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

    def __export_csv_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self,
                                              "Save spreadsheet",
                                              f"{self.view_model.get_name()}.csv",
                                              "csv Files (*.csv))")
        if file_path:
            try:
                self.view_model.export_spreadsheet(file_path)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

    def __export_ro_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self,
                                              "Save test script",
                                              f"{self.view_model.get_name()}.ro",
                                              "RO Files (*.ro)")
        if file_path:
            try:
                self.view_model.export_ro_file(file_path)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))             
        

class WireListView(ListView):
    def __init__(self, parent, model: WireListViewModel):
        super().__init__(parent, model)
        
class UnusedListView(ListView):
    def __init__(self, parent, model: UnusedListViewModel):
        super().__init__(parent, model)
    
    def __input_placeholder__(self):
        self.user_input_box.setPlaceholderText(self.view_model.get_placeholder())

class GroundListView(ListView):
    def __init__(self, parent, model: GroundListViewModel):
        super().__init__(parent, model)
