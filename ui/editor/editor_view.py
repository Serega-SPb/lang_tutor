from PyQt5.QtWidgets import QWidget

from core.decorators import try_except_wrapper
from ui.additional_widgets import ScenarioDataWidget, load_data_in_list
from .editor_view_ui import Ui_Form


class EditorView(QWidget):

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

    def init_ui(self):
        self.ui.undoBtn.setEnabled(False)
        self.ui.redoBtn.setEnabled(False)

        self.ui.addBlockBtn.setEnabled(False)
        self.ui.blocksCmbBx.currentIndexChanged.connect(
            lambda x: self.ui.addBlockBtn.setEnabled(True if x > -1 else False))

        self.ui.scenarioBlocksList.itemDoubleClicked.connect(self.open_block)

        # TEMP -- not implemented --
        self.ui.testRunBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)

    def connect_widgets(self):
        self.ui.backMenuBtn.clicked.connect(self.close_block)
        self.ui.backMenuBtn.clicked.connect(self.controller.back_to_menu)
        self.ui.addBlockBtn.clicked.connect(self.add_block)

        self.ui.undoBtn.clicked.connect(self.controller.undo)
        self.ui.redoBtn.clicked.connect(self.controller.redo)

        self.ui.testRunBtn.clicked.connect(self.controller.test_run)  # ?
        self.ui.saveBtn.clicked.connect(self.controller.save_scenario)

    def connect_model_signals(self):
        self.model.scenario_changed += self.load_scenario
        self.model.blocks_changed += self.load_blocks
        self.model.can_undo_changed += self.ui.undoBtn.setEnabled
        self.model.can_redo_changed += self.ui.redoBtn.setEnabled
        self.model.block_widget_changed += self.load_block_widget

    def load_scenario(self, scenario):
        self.ui.scenarioNameLed.setText(scenario.name)
        self.ui.scenarioBlocksList.clear()
        for data in scenario.scenario_data:
            load_data_in_list(self.ui.scenarioBlocksList, ScenarioDataWidget, data, self.remove_block)

    @property
    def current_add_block(self):
        return self.ui.blocksCmbBx.currentText()

    def load_blocks(self, blocks):
        self.ui.blocksCmbBx.clear()
        [self.ui.blocksCmbBx.addItem(bl) for bl in blocks]

    @try_except_wrapper
    def add_block(self, *args):
        self.controller.add_block(self.current_add_block)

    @try_except_wrapper
    def remove_block(self, *args):
        self.controller.remove_block(*args)

    def open_block(self, item):
        self.controller.set_block_widget(item.data)

    def close_block(self):
        layout = self.ui.scenarioBlockWidget.layout()
        item = layout.itemAt(0)
        if item:
            item.widget().setParent(None)

    @try_except_wrapper
    def load_block_widget(self, widget):
        self.close_block()
        layout = self.ui.scenarioBlockWidget.layout()
        layout.addWidget(widget)
