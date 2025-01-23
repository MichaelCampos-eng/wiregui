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
from PyQt6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem

import sys
from wrman.converter.ditmco_test import *
from wrman.pin_management.list_manager import *

class PandasModel(QAbstractTableModel):

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        if parent == QModelIndex():
            return len(self._dataframe)
        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._dataframe.index[section])
        return None

class TableView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.component_list: DitmcoList
        self.__setup_comp_list__()

        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        table_name = QLabel(self.component_list.get_list_name())
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
        self.model = PandasModel(self.component_list.get_table_df())
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        input_layout = QVBoxLayout()
        self.user_input_box = QLineEdit()
        self.user_input_box.setPlaceholderText(self.component_list.fetch_curr_arg_name())
        self.user_input_box.returnPressed.connect(self.__user_input__)
        input_layout.addWidget(self.user_input_box)
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

    def __user_input__(self):
        try:
            self.component_list.step(self.user_input_box.text())
            self.model = PandasModel(self.component_list.get_table_df())
            self.table_view.setModel(self.model)
        except ValueError as e:
            QMessageBox.critical(self, "Input List Error", str(e))             
            pass
        self.__input_placeholder__()
    
    def __input_placeholder__(self):
        self.user_input_box.clear()
        self.user_input_box.setPlaceholderText(self.component_list.fetch_curr_arg_name())

    def __toggle_table__(self):
        self.table_view.show() if self.check_box.isChecked() else self.table_view.hide()

    def __setup_comp_list__(self):
        pass
    
class WireListView(TableView):
    def __init__(self):
        super().__init__()
        
    def __setup_comp_list__(self):
        self.component_list = WireList()
        
class UnusedListView(TableView):
    def __init__(self):
        super().__init__()
    
    def __setup_comp_list__(self):
        self.component_list = IsolatedList()
    
    def __input_placeholder__(self):
        self.user_input_box.setPlaceholderText(self.component_list.fetch_curr_arg_name())

class GroundListView(TableView):
    def __init__(self):
        super().__init__()

    def __setup_comp_list__(self):
        self.component_list = GroundList()
