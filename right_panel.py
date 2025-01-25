from PyQt6.QtWidgets import ( 
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtGui import QAction
from wrman.converter.ditmco_test import *
from wrman.pin_management.list_manager import *
from wrman.config_classes.config import Config
from table_views import *
import yaml
from list_view_model import AggregateModel

class RightPanel(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.wire_list_view = WireListView(parent)
        self.unused_list_view = UnusedListView(parent)
        self.ground_list_view = GroundListView(parent)
        self.agg_model = AggregateModel(self.wire_list_view.list_model.table,
                                        self.unused_list_view.list_model.table,
                                        self.ground_list_view.list_model.table)

        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(self.wire_list_view)
        right_panel_layout.addWidget(self.unused_list_view)
        right_panel_layout.addWidget(self.ground_list_view)
        right_panel_layout.addStretch()

        self.setLayout(right_panel_layout)

        import_action = QAction(QIcon("open.png"), "&Import All", self)
        import_action.setStatusTip(f"Import all lists")
        import_action.triggered.connect(self.agg_model.import_lists)
        import_action.setCheckable(True)

        export_action = QAction(QIcon("open.png"), "&Export All", self)
        export_action.setStatusTip(f"Export all lists")
        export_action.triggered.connect(self.agg_model.export_lists)
        export_action.setCheckable(True)

        parent.import_menu.addAction(import_action)
        parent.export_menu.addAction(export_action)
    
    