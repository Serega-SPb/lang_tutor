from PyQt5.QtWidgets import QWidget

from core.decorators import try_except_wrapper
from ui.additional_widgets import load_data_in_list
from .additional_widgets_kan import KanjiWidget, KeyComboBox
from .editor_block_view_ui import Ui_Form


class EditorBlockView(QWidget):

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
        self.ui.kanjiList.currentItemChanged.connect(self.select_kanji)
        self.ui.kanjiContainer.setEnabled(False)
        self.ui.keyCmbBx = KeyComboBox.morph_from(self.ui.keyCmbBx)
        self.ui.horizontalLayout_4.addWidget(self.ui.keyCmbBx)

    def connect_widgets(self):
        self.ui.addBtn.clicked.connect(lambda x: self.controller.add_kanji())
        self.ui.removeBtn.clicked.connect(self.remove_kanji)
        self.ui.questTypeCmbBx.currentTextChanged.connect(self.controller.set_quest_type)
        self.ui.keyCmbBx.currentIndexChanged.connect(self.select_key)

        self.ui.kanjiLnEd.textEdited.connect(self.controller.set_kanji_value)
        self.ui.dashCountSpBx.valueChanged.connect(self.controller.set_kanji_dash_count)
        self.ui.onReadingPte.textChanged.connect(
            lambda: self.controller.set_kanji_on_reading(self.ui.onReadingPte.toPlainText()))
        self.ui.kunReadingPte.textChanged.connect(
            lambda: self.controller.set_kanji_kun_reading(self.ui.kunReadingPte.toPlainText()))
        self.ui.translatePte.textChanged.connect(
            lambda: self.controller.set_kanji_translate(self.ui.translatePte.toPlainText()))

    def connect_model_signals(self):
        self.model.quest_type_changed += self.ui.questTypeCmbBx.setCurrentText
        self.model.quest_types_changed += self.load_quest_types
        self.model.keys_changed += self.load_keys
        self.model.kanjis_changed += self.load_kanjis
        self.model.current_kanji_changed += self.load_current_kanji
        self.model.current_kanji_index_changed += self.ui.kanjiList.setCurrentRow
        self.model.update_label_event += self.update_lbl

    def load_quest_types(self, values):
        self.ui.questTypeCmbBx.clear()
        self.ui.questTypeCmbBx.addItems(values)

    def load_keys(self, values):
        self.ui.keyCmbBx.load_data(values)

    def select_kanji(self, item):
        self.controller.set_kanji_index(self.ui.kanjiList.currentRow())
        self.controller.select_kanji(item.data if item else None)

    def load_kanjis(self, values):
        self.ui.kanjiList.clear()
        for val in values:
            load_data_in_list(self.ui.kanjiList, KanjiWidget, val)

    def load_current_kanji(self, kanji):
        self.ui.kanjiContainer.setEnabled(True if kanji else False)
        if not kanji:
            return
        self.ui.kanjiLnEd.setText(kanji.value)
        self.ui.keyCmbBx.select_by_value(kanji.key)
        self.ui.dashCountSpBx.setValue(kanji.dash_count)
        self.ui.onReadingPte.setPlainText(', '.join(kanji.on))
        self.ui.kunReadingPte.setPlainText(', '.join(kanji.kun))
        self.ui.translatePte.setPlainText(', '.join(kanji.translate))

    @try_except_wrapper
    def select_key(self, *args):
        curr_key = self.ui.keyCmbBx.get_currect_data()
        if not curr_key:
            self.reset_kanji_container()
            return
        self.controller.set_kanji_key(curr_key)

    @try_except_wrapper
    def remove_kanji(self, *args):
        kanji = self.ui.kanjiList.currentItem().data
        self.reset_kanji_container()
        self.controller.remove_kanji(kanji)

    def update_lbl(self):
        i = self.ui.kanjiList.currentItem()
        if i:
            i.wid.update_title()

    def reset_kanji_container(self):
        self.ui.kanjiLnEd.clear()
        self.ui.keyCmbBx.setCurrentIndex(-1)
        self.ui.dashCountSpBx.clear()
        self.ui.onReadingPte.clear()
        self.ui.kunReadingPte.clear()
        self.ui.translatePte.clear()
