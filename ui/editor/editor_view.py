from PyQt5.QtWidgets import QWidget

from core.data_loader import DataLoader
from core.decorators import try_except_wrapper
from ui.additional_widgets import ScenarioDataWidget, load_data_in_list, translate_widget
from .editor_view_ui import Ui_Form


class EditorView(QWidget):

    current_listitem_widget = None
    current_block_widget = None
    quest_types_loaded = False

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.translate_ui()

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

    def translate_ui(self):
        ui = self.ui
        widgets = [ui.label, ui.label_2, ui.label_3, ui.label_10,
                   ui.backMenuBtn, ui.saveBtn, ui.addBlockBtn,
                   ui.addBtn, ui.removeBtn]
        [translate_widget(w) for w in widgets]

    def init_ui(self):
        self.ui.saveBtn.setEnabled(False)
        self.ui.undoBtn.setEnabled(False)
        self.ui.redoBtn.setEnabled(False)
        self.ui.scenarioBlockWidget.setEnabled(False)
        self.ui.blockDataContainer.setEnabled(False)
        self.ui.addBlockBtn.setEnabled(False)
        self.ui.blocksCmbBx.currentIndexChanged.connect(
            lambda x: self.ui.addBlockBtn.setEnabled(True if x > -1 else False))

    def connect_widgets(self):
        self.ui.backMenuBtn.clicked.connect(self.controller.back_to_menu)
        self.ui.addBlockBtn.clicked.connect(self.add_block)

        self.ui.undoBtn.clicked.connect(self.controller.undo)
        self.ui.redoBtn.clicked.connect(self.controller.redo)
        self.ui.saveBtn.clicked.connect(self.controller.save_scenario)

        self.ui.scenarioBlocksList.currentRowChanged.connect(self.controller.set_sc_block_index)
        self.ui.blockDataList.currentRowChanged.connect(self.controller.set_data_index)
        self.ui.scenarioNameLed.textEdited.connect(self.controller.change_scenarion_name)
        self.ui.questTypeCmbBx.currentTextChanged.connect(self.set_quest_type)

        self.ui.addBtn.clicked.connect(self.controller.add_block_data)
        self.ui.removeBtn.clicked.connect(self.remove_block_data)

    def connect_model_signals(self):
        self.model.scenario_changed += self.load_scenario
        self.model.scenario_name_changed += self.ui.scenarioNameLed.setText
        self.model.blocks_changed += self.load_blocks
        self.model.can_undo_changed += self.ui.saveBtn.setEnabled
        self.model.can_undo_changed += self.ui.undoBtn.setEnabled
        self.model.can_redo_changed += self.ui.redoBtn.setEnabled

        self.model.quest_types_changed += self.load_quest_types
        self.model.current_quest_type_changed += self.ui.questTypeCmbBx.setCurrentText
        self.model.current_sc_block_index_changed += self.ui.scenarioBlocksList.setCurrentRow
        self.model.current_data_index_changed += self.ui.blockDataList.setCurrentRow
        self.model.current_sc_block_changed += self.load_sc_block
        self.model.current_data_changed += self.load_data

        self.model.listitem_widget_changed += self.set_listitem_widget
        self.model.block_widget_changed += self.set_block_widget

    def load_scenario(self, scenario):
        self.ui.scenarioNameLed.setText(scenario.name)
        self.ui.scenarioBlocksList.clear()
        for data in scenario.scenario_data:
            load_data_in_list(self.ui.scenarioBlocksList, ScenarioDataWidget, data, self.remove_block)

    def load_quest_types(self, types):
        self.quest_types_loaded = False
        self.ui.questTypeCmbBx.clear()
        if types:
            [self.ui.questTypeCmbBx.addItem(t.ui, t) for t in types]
        self.quest_types_loaded = True

    def set_quest_type(self, value):
        if self.quest_types_loaded:
            value = self.ui.questTypeCmbBx.currentData()
            self.controller.set_quest_type(value)

    def load_sc_block(self, sc_block):
        self.ui.blockDataList.clear()
        self.ui.scenarioBlockWidget.setEnabled(sc_block is not None)
        if not sc_block:
            return
        index = self.ui.questTypeCmbBx.findText(sc_block.quest_type.ui)
        self.ui.questTypeCmbBx.setCurrentIndex(index)

        for d in sc_block.data:
            load_data_in_list(self.ui.blockDataList, self.current_listitem_widget, d)

    def load_blocks(self, blocks):
        self.ui.blocksCmbBx.clear()
        [self.ui.blocksCmbBx.addItem(bl.ui_name, bl) for bl in blocks]

    def set_listitem_widget(self, value):
        self.current_listitem_widget = value

    def set_block_widget(self, value):
        self.current_block_widget = value

    @try_except_wrapper
    def add_block(self, *args):
        block = self.ui.blocksCmbBx.currentData()
        self.controller.add_block(block)

    @try_except_wrapper
    def remove_block(self, *args):
        self.controller.remove_block(*args)

    @try_except_wrapper
    def remove_block_data(self, *args):
        data = self.ui.blockDataList.currentItem().data
        self.controller.remove_block_data(data)

    def load_data(self, data, prop_path):
        self.close_block()
        self.ui.blockDataContainer.setEnabled(data is not None)
        if data is None:
            return

        self.load_block_widget()
        self.current_block_widget.model.update_label_event += self.update_lbl
        self.current_block_widget.controller.load_block_data(data, prop_path)

    def close_block(self):
        layout = self.ui.blockDataContainer.layout()
        item = layout.itemAt(0)
        if item:
            item.widget().setParent(None)

    @try_except_wrapper
    def load_block_widget(self):
        widget = self.current_block_widget
        if not widget:
            return

        layout = self.ui.blockDataContainer.layout()
        layout.addWidget(widget)

    def update_lbl(self):
        i = self.ui.blockDataList.currentItem()
        if i:
            i.wid.update_title()
