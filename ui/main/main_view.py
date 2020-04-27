import logging

from PyQt5.QtWidgets import QWidget, QButtonGroup, QFileDialog

from core import log_config
from core.decorators import try_except_wrapper
from ui.additional_widgets import ModuleWidget, ScenarioWidget, load_data_in_list
from ui.cross_widget_events import EditorMode, CrossWidgetEvents as CrossEvent
from ui.additional_widgets import translate_widget
from .main_view_ui import Ui_Form
from ..translator import Translator


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
    SETTINGS = 5


class MainView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.translate_ui()

        self.is_debug = self.model.is_debug

        if self.is_debug:
            self.logger = logging.getLogger(log_config.LOGGER_NAME)
            self.logger.addHandler(UiLogHandler(self.ui.logPte))

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

        CrossEvent.locale_changed_event += self.translate_ui
        self.controller.exec()

    def translate_ui(self):
        ui = self.ui
        translator = Translator.get_translator('main')
        widgets = [ui.label, ui.label_2, ui.label_3, ui.label_4, ui.label_5,
                   ui.scenarioMenuBtn, ui.editorMenuBtn, ui.modulesMenuBtn,
                   ui.configMenuBtn, ui.debugMenuBtn, ui.quitMenuBtn, ui.optionsEnableChbx,
                   ui.starScenarioBtn, ui.startEditorBtn, ui.deleteBtn,
                   ui.createNewRbn, ui.createFromRbn, ui.loadRbn, ui.deleteRbn,
                   ui.scenarioListRefreshBtn, ui.modulesListRefreshBtn,
                   ui.label_6, ui.label_7, ui.label_8, ui.label_9, ui.label_10,
                   ui.applySettingsBtn, ui.cancelSettingsBtn, ui.warningGrBx]
        [translate_widget(w, translator) for w in widgets]

    def init_ui(self):
        self.ui.debugMenuBtn.setVisible(self.is_debug)
        self.ui.starScenarioBtn.setEnabled(False)
        self.ui.scenarioList.currentItemChanged.connect(
            lambda x: self.ui.starScenarioBtn.setEnabled(True if x else False))
        self.init_menu()

        self.ui.loadList.setVisible(False)
        self.ui.createFromList.setVisible(False)
        self.ui.deleteList.setVisible(False)
        self.ui.deleteBtn.setVisible(False)
        self.ui.createNewRbn.setChecked(True)

        self.ui.warningGrBx.setVisible(False)
        self.ui.applySettingsBtn.setEnabled(False)

    def init_menu(self):
        self.menu_group = QButtonGroup()
        btns = [self.ui.scenarioMenuBtn, self.ui.editorMenuBtn, self.ui.modulesMenuBtn,
                self.ui.configMenuBtn, self.ui.debugMenuBtn]
        for btn in btns:
            btn.setCheckable(True)
            self.menu_group.addButton(btn)

        self.ui.scenarioMenuBtn.clicked.connect(lambda: self.select_screen(Menu.SCENARIO))
        self.ui.editorMenuBtn.clicked.connect(lambda: self.select_screen(Menu.EDITOR))
        self.ui.modulesMenuBtn.clicked.connect(lambda: self.select_screen(Menu.MODULES))
        self.ui.configMenuBtn.clicked.connect(lambda: self.select_screen(Menu.SETTINGS))
        self.ui.debugMenuBtn.clicked.connect(lambda: self.select_screen(Menu.DEBUG))
        self.ui.quitMenuBtn.clicked.connect(lambda x: CrossEvent.clsoe_main_window_event.emit())
        # TODO ? statisticMenu ?
        self.ui.scenarioMenuBtn.click()

    def select_screen(self, i):
        if self.ui.stackedWidget.currentIndex() == i:
            return
        self.ui.stackedWidget.setCurrentIndex(i)

    def connect_widgets(self):
        self.ui.optionsEnableChbx.toggled['bool'].connect(self.controller.set_is_options_enabled)
        self.ui.modulesListRefreshBtn.clicked.connect(self.controller.reload_modules)
        self.ui.scenarioListRefreshBtn.clicked.connect(self.controller.reload_scenarios)
        self.ui.starScenarioBtn.clicked.connect(self.on_start_click)
        self.ui.createNewRbn.toggled.connect(
            lambda: self.controller.set_editor_mode(EditorMode.CREATE_NEW))
        self.ui.createFromRbn.toggled.connect(
            lambda: self.controller.set_editor_mode(EditorMode.CREATE_FROM))
        self.ui.loadRbn.toggled.connect(
            lambda: self.controller.set_editor_mode(EditorMode.LOAD))
        self.ui.startEditorBtn.clicked.connect(self.on_start_editor)
        self.ui.deleteBtn.clicked.connect(self.on_delete_click)

        self.ui.localeCmbBx.currentTextChanged.connect(self.controller.select_locale)
        self.ui.modulesDirBtn.clicked.connect(self.select_modules_dir)
        self.ui.modulesDirLnEd.editingFinished.connect(
            lambda: self.controller.set_modules_dir(self.ui.modulesDirLnEd.text()))
        self.ui.scenarioDirBtn.clicked.connect(self.select_scenarios_dir)
        self.ui.scenarioDirLnEd.editingFinished.connect(
            lambda: self.controller.set_scenario_dir(self.ui.scenarioDirLnEd.text()))
        self.ui.applySettingsBtn.clicked.connect(self.controller.apply_settings)
        self.ui.cancelSettingsBtn.clicked.connect(self.controller.reload_setting)

    def connect_model_signals(self):
        self.model.is_options_enabled_changed += self.ui.optionsEnableChbx.setChecked
        self.model.modules_changed += self.load_modules
        self.model.scenarios_changed += self.load_scenarios

        self.model.locales_changed += self.load_locales
        self.model.is_applied_settings_changed += self.on_applied_flag_changed
        self.model.current_locale_changed += self.ui.localeCmbBx.setCurrentText
        self.model.modules_dir_changed += self.ui.modulesDirLnEd.setText
        self.model.scenarios_dir_changed += self.ui.scenarioDirLnEd.setText

    @try_except_wrapper
    def load_modules(self, mods):
        self.ui.modulesList.clear()
        for mod in mods:
            load_data_in_list(self.ui.modulesList, ModuleWidget, mod)

    @try_except_wrapper
    def load_scenarios(self, scens):
        ui_lists = [self.ui.scenarioList, self.ui.createFromList,
                    self.ui.loadList, self.ui.deleteList]
        [wid.clear() for wid in ui_lists]
        for sc in scens:
            [load_data_in_list(wid, ScenarioWidget, sc) for wid in ui_lists]

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

    @try_except_wrapper
    def on_delete_click(self, *args):
        items = self.ui.deleteList.selectedItems()
        args = [i.data.name for i in items]
        self.controller.delete_scenarios(args)

    def load_locales(self, values):
        self.ui.localeCmbBx.clear()
        self.ui.localeCmbBx.addItems(values)

    def on_applied_flag_changed(self, value):
        self.ui.warningGrBx.setHidden(value)
        self.ui.applySettingsBtn.setDisabled(value)

    def select_modules_dir(self):
        self.select_dir('SELECT_MODULES_DIR', self.model.modules_dir,
                        self.controller.set_modules_dir)

    def select_scenarios_dir(self):
        self.select_dir('SELECT_SCENARIOS_DIR', self.model.scenarios_dir,
                        self.controller.set_scenario_dir)

    def select_dir(self, title, start_dir, set_action):
        directory = QFileDialog.getExistingDirectory(self, title, start_dir)
        if directory:
            set_action(directory)
