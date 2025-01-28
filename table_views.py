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
    
    def __init__(self, parent):
        super().__init__()
        self.list_model: ListViewModel
        self.__setup_list_model__()

        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        table_name = QLabel(self.list_model.get_name())
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
        self.model = PandasModel(self.list_model.get_df())
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        input_layout = QVBoxLayout()
        self.user_input_box = QLineEdit()
        self.user_input_box.setPlaceholderText(self.list_model.get_placeholder())
        self.user_input_box.returnPressed.connect(self.__user_input__)
        input_layout.addWidget(self.user_input_box)
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        import_action = QAction(QIcon("open.png"), f"&Import {self.list_model.get_name()}", self)
        import_action.setStatusTip(f"Import {self.list_model.get_name()}")
        import_action.triggered.connect(self.__import_dialog__)
        import_action.setCheckable(True)

        export_action = QAction(QIcon("open.png"), f"&Export {self.list_model.get_name()}", self)
        export_action.setStatusTip(f"Export {self.list_model.get_name()}")
        export_action.triggered.connect(self.__export_dialog__)
        export_action.setCheckable(True)

    
        parent.import_menu.addAction(import_action)
        parent.export_menu.addAction(export_action)

    def __user_input__(self):
        try:
            self.list_model.append(self.user_input_box.text())
            self.model = PandasModel(self.list_model.get_df())
            self.table_view.setModel(self.model)
            self.table_view.scrollToBottom()
            self.__input_placeholder__()
        except ValueError as e:
            QMessageBox.critical(self, "Input List Error", str(e))
    
    def __input_placeholder__(self):
        self.user_input_box.clear()
        self.user_input_box.setPlaceholderText(self.list_model.get_placeholder())

    def __toggle_table__(self):
        self.table_view.show() if self.check_box.isChecked() else self.table_view.hide()

    def __setup_list_model__(self):
        pass

    def __import_dialog__(self):
        pass

    def __export_dialog__(self):
        dialog = QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(
            self,
            "Save File",
            f"{self.list_model.get_name()}.ro",
            "Text Files (*.ro);;All Files (*)"
        )
        self.list_model.set_file_path(file_path)
        try:
            self.list_model.export_list()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))             
        

class WireListView(ListView):
    def __init__(self, parent):
        super().__init__(parent)
        
    def __setup_list_model__(self):
        self.list_model = WireListViewModel()
        
class UnusedListView(ListView):
    def __init__(self, parent):
        super().__init__(parent)
    
    def __setup_list_model__(self):
        self.list_model = UnusedListViewModel()
    
    def __input_placeholder__(self):
        self.user_input_box.setPlaceholderText(self.list_model.get_placeholder())

class GroundListView(ListView):
    def __init__(self, parent):
        super().__init__(parent)

    def __setup_list_model__(self):
        self.list_model = GroundListViewModel()
