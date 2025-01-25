from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
    QTableView,
    QHeaderView,
    QMessageBox
)
from pandas_model import *
from list_view_model import *

class ListView(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.list_model = ListViewModel()

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
        self.model = PandasModel(self.list_model.get_table())
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
        import_action.triggered.connect(self.list_model.import_list)
        import_action.setCheckable(True)

        export_action = QAction(QIcon("open.png"), f"&Export {self.list_model.get_name()}", self)
        export_action.setStatusTip(f"Export {self.list_model.get_name()}")
        export_action.triggered.connect(self.list_model.export_list)
        export_action.setCheckable(True)

        parent.import_menu.addAction(import_action)
        parent.export_menu.addAction(export_action)

    def __user_input__(self):
        try:
            self.table.step(self.user_input_box.text())
            self.model = PandasModel(self.table.get_table_df())
            self.table_view.setModel(self.model)
            self.table_view.scrollToBottom()
        except ValueError as e:
            QMessageBox.critical(self, "Input List Error", str(e))             
            pass
        self.__input_placeholder__()
    
    def __input_placeholder__(self):
        self.user_input_box.clear()
        self.user_input_box.setPlaceholderText(self.table.fetch_curr_arg_name())

    def __toggle_table__(self):
        self.table_view.show() if self.check_box.isChecked() else self.table_view.hide()

class WireListView(ListView):
    def __init__(self, parent):
        super().__init__(parent)
        
    def __setup_comp_list__(self):
        self.table = WireListViewModel()
        
class UnusedListView(ListView):
    def __init__(self, parent):
        super().__init__(parent)
    
    def __setup_comp_list__(self):
        self.table = UnusedListViewModel()
    
    def __input_placeholder__(self):
        self.user_input_box.setPlaceholderText(self.table.get_placeholder())

class GroundListView(ListView):
    def __init__(self, parent):
        super().__init__(parent)

    def __setup_comp_list__(self):
        self.table = GroundListViewModel()

