import logging

from PyQt5.QtWidgets import QMainWindow, QListWidgetItem

from core import log_config
from core.decorators import try_except_wrapper
from .additional_widgets import ModuleWidget, ScenarioWidget
from .main_view_ui import Ui_MainWindow


def load_data_in_list(list_wid, data_wid, data):
    item = QListWidgetItem()
    item.data = data
    widget = data_wid(data, list_wid)

    item.setSizeHint(widget.sizeHint())
    list_wid.addItem(item)
    list_wid.setItemWidget(item, widget)


class UiLogHandler(logging.Handler):
    def __init__(self, log_widget):
        super().__init__()
        self.widget = log_widget
        self.widget.setReadOnly(True)
        self.setFormatter(log_config.formatter)
        self.setLevel(log_config.STREAM_LOG_LVL)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MainView(QMainWindow):

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.logger.addHandler(UiLogHandler(self.ui.logPte))

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

        self.loads()

    def loads(self):
        self.controller.reload_modules()
        self.controller.reload_scenarios()

    def init_ui(self):
        self.ui.starScenarioBtn.setEnabled(False)
        self.ui.scenarioList.currentItemChanged.connect(
            lambda x: self.ui.starScenarioBtn.setEnabled(True if x else False))

        self.ui.scenarioMenuBtn.clicked.connect(lambda: self.select_screen(1))
        self.ui.editorMenuBtn.clicked.connect(lambda: self.select_screen(0))
        self.ui.modulesMenuBtn.clicked.connect(lambda: self.select_screen(2))
        self.ui.configMenuBtn.clicked.connect(lambda: self.select_screen(0))
        self.ui.debugMenuBtn.clicked.connect(lambda: self.select_screen(3))
        # TODO ? statisticMenu ?

    def select_screen(self, i):
        if self.ui.stackedWidget.currentIndex() == i:
            return
        self.ui.stackedWidget.setCurrentIndex(i)

    def connect_widgets(self):
        self.ui.modulesListRefreshBtn.clicked.connect(self.controller.reload_modules)
        self.ui.scenarioListRefreshBtn.clicked.connect(self.controller.reload_scenarios)
        self.ui.starScenarioBtn.clicked.connect(self.on_start_click)

    def connect_model_signals(self):
        self.model.modules_changed += self.load_modules
        self.model.scenarios_changed += self.load_scenarios

    @try_except_wrapper
    def load_modules(self):
        self.ui.modulesList.clear()
        mods = self.model.modules
        for mod in mods:
            load_data_in_list(self.ui.modulesList, ModuleWidget, mod)

    @try_except_wrapper
    def load_scenarios(self):
        self.ui.scenarioList.clear()
        scens = self.model.scenarios
        for sc in scens:
            load_data_in_list(self.ui.scenarioList, ScenarioWidget, sc)

    @try_except_wrapper
    def on_start_click(self, *args):
        curr_item = self.ui.scenarioList.currentItem()
        if not hasattr(curr_item, 'data'):
            return
        self.controller.start_scenario(curr_item.data)