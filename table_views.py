from PyQt6.QtWidgets import ( 
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
    QScrollArea
)
from PyQt6.QtCore import Qt

import sys
from wrman.converter.ditmco_test import *
from wrman.pin_management.list_manager import *

class TableView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.component_list: DitmcoList
        self.setup_comp_list()

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        table_name = QLabel(self.component_list.get_list_name())
        table_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check_box = QCheckBox()
        header_layout.addWidget(table_name), header_layout.addStretch(), header_layout.addWidget(check_box)

        scroll_area = QScrollArea()
        sheet_layout = QGridLayout()
        sheet_layout.setContentsMargins(0, 0, 0, 0), sheet_layout.setSpacing(0)
        for col_name in self.component_list.get_column_names:
            col = QLabel(col_name)
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.setStyleSheet("background-color: lightblue; padding: 10px")
            sheet_layout.addWidget(col)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(sheet_layout)

        input_layout = QVBoxLayout()
        self.user_input_box = QLineEdit()
        self.user_input_box.setPlaceholderText(self.component_list.fetch_curr_arg_name())
        self.user_input_box.returnPressed.connect(self.user_input)
        input_layout.addWidget(self.user_input_box)
        
        main_layout.addLayout(header_layout), main_layout.addWidget(scroll_area), main_layout.addLayout(input_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def user_input(self):
        try:
            self.component_list.step(self.user_input_box.text())
        except ValueError as e:
            # TODO: create an error window if ValueError               
            pass
        self.user_input_box.setPlaceholderText(self.component_list.fetch_curr_arg_name())

    def setup_comp_list(self):
        pass
        

class WireListView(TableView):
    def __init__(self):
        super().__init__()
        
    def setup_comp_list(self):
        self.component_list = WireList()
        
class UnusedListView(TableView):
    def __init__(self):
        super().__init__()
    
    def setup_comp_list(self):
        self.component_list = IsolatedList()

class GroundListView(TableView):
    def __init__(self):
        super().__init__()

    def setup_comp_list(self):
        self.component_list = GroundList()