import logging

from PyQt5.QtWidgets import QWidget, QButtonGroup

from core import log_config
from core.data_loader import DataLoader
from core.decorators import try_except_wrapper
from ui.additional_widgets import ModuleWidget, ScenarioWidget, load_data_in_list
from ui.cross_widget_events import EditorMode
from .main_view_ui import Ui_Form


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


class Menu:
    DEFAULT = 0
    SCENARIO = 1
    MODULES = 2
    DEBUG = 3
    EDITOR = 4


class MainView(QWidget):

    OPTIONS_ENABLED_PARAM = 'ui.options_enabled'

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.data_loader = DataLoader()
        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.logger.addHandler(UiLogHandler(self.ui.logPte))

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

        self.load_modules()
        self.load_scenarios()

    def init_ui(self):
        self.ui.starScenarioBtn.setEnabled(False)
        self.ui.optionsEnableChbx.setChecked(
            self.data_loader.get_config_param(self.OPTIONS_ENABLED_PARAM) or False)
        self.ui.scenarioList.currentItemChanged.connect(
            lambda x: self.ui.starScenarioBtn.setEnabled(True if x else False))
        self.ui.optionsEnableChbx.toggled['bool'].connect(
            lambda x: self.save_ui_config(self.OPTIONS_ENABLED_PARAM, x))

        self.init_menu()

        self.ui.loadList.setVisible(False)
        self.ui.createFromList.setVisible(False)
        self.ui.createNewRbn.setChecked(True)
        self.ui.createNewRbn.toggled.connect(
            lambda: self.controller.set_editor_mode(EditorMode.CREATE_NEW))
        self.ui.createFromRbn.toggled.connect(
            lambda: self.controller.set_editor_mode(EditorMode.CREATE_FROM))
        self.ui.loadRbn.toggled.connect(
            lambda: self.controller.set_editor_mode(EditorMode.LOAD))
        self.ui.startEditorBtn.clicked.connect(self.on_start_editor)

    def init_menu(self):
        self.menu_group = QButtonGroup()
        btns = [self.ui.scenarioMenuBtn, self.ui.editorMenuBtn, self.ui.modulesMenuBtn,
                self.ui.configMenuBtn, self.ui.debugMenuBtn]
        for btn in btns:
            btn.setCheckable(True)
            self.menu_group.addButton(btn)

        self.ui.scenarioMenuBtn.clicked.connect(lambda: self.select_screen(Menu.SCENARIO))
        self.ui.editorMenuBtn.clicked.connect(lambda: self.select_screen(Menu.EDITOR))
        # self.ui.editorMenuBtn.clicked.connect(lambda: CrossWidgetEvents.change_screen_event.emit(ScI.EDITOR))
        self.ui.modulesMenuBtn.clicked.connect(lambda: self.select_screen(Menu.MODULES))
        self.ui.configMenuBtn.clicked.connect(lambda: self.select_screen(Menu.DEFAULT))
        self.ui.debugMenuBtn.clicked.connect(lambda: self.select_screen(Menu.DEBUG))
        # TODO ? statisticMenu ?
        self.ui.scenarioMenuBtn.click()
        # self.ui.scenarioMenuBtn.setChecked(True)
        # self.select_screen(Menu.SCENARIO)

    def save_ui_config(self, path, value):
        self.data_loader.set_config_param(path, value)

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
            load_data_in_list(self.ui.createFromList, ScenarioWidget, sc)
            load_data_in_list(self.ui.loadList, ScenarioWidget, sc)

    @try_except_wrapper
    def on_start_click(self, *args):
        curr_item = self.ui.scenarioList.currentItem()
        options_enabled = self.ui.optionsEnableChbx.isChecked()
        self.controller.start_scenario(curr_item.data, options_enabled)

    @try_except_wrapper
    def on_start_editor(self, *args):
        args = None
        mode = self.model.editor_mode
        if mode == EditorMode.CREATE_FROM:
            items = self.ui.createFromList.selectedItems()
            args = [i.data for i in items]
            if len(args) == 0:
                raise ValueError('Inccorect args')
        elif mode == EditorMode.LOAD:
            args = self.ui.loadList.currentItem().data
        self.controller.start_editor(mode, args)
