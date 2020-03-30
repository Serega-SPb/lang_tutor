from PyQt5.QtWidgets import QWidget

from core.decorators import try_except_wrapper
from ui.additional_widgets import load_data_in_list
from .editor_block_view_ui import Ui_Form
from .additional_widgets_word import WordWidget


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
        self.ui.wordsList.currentItemChanged.connect(self.select_word)
        self.ui.wordContainer.setEnabled(False)

    def connect_widgets(self):
        self.ui.addBtn.clicked.connect(lambda x: self.controller.add_word())
        self.ui.removeBtn.clicked.connect(self.remove_word)
        self.ui.questTypeCmbBx.currentTextChanged.connect(self.controller.set_quest_type)

        self.ui.spellingLnEd.textEdited.connect(self.controller.set_word_spelling)
        self.ui.readingLnEd.textEdited.connect(self.controller.set_word_reading)
        self.ui.translatePte.textChanged.connect(
            lambda: self.controller.set_word_translate(self.ui.translatePte.toPlainText()))

    def connect_model_signals(self):
        self.model.quest_type_changed += self.ui.questTypeCmbBx.setCurrentText
        self.model.quest_types_changed += self.load_quest_types
        self.model.words_changed += self.load_words
        self.model.current_word_changed += self.load_current_word
        self.model.current_word_index_changed += self.ui.wordsList.setCurrentRow
        self.model.update_label_event += self.update_lbl

    def load_quest_types(self, values):
        self.ui.questTypeCmbBx.clear()
        self.ui.questTypeCmbBx.addItems(values)

    def select_word(self, item):
        self.controller.set_word_index(self.ui.wordsList.currentRow())
        self.controller.select_word(item.data if item else None)

    def load_words(self, values):
        self.ui.wordsList.clear()
        for val in values:
            load_data_in_list(self.ui.wordsList, WordWidget, val)

    def load_current_word(self, value):
        self.ui.wordContainer.setEnabled(True if value else False)
        if not value:
            return
        self.ui.spellingLnEd.setText(value.spelling)
        self.ui.readingLnEd.setText(value.reading)
        self.ui.translatePte.setPlainText(', '.join(value.translate))

    @try_except_wrapper
    def remove_word(self, *args):
        word = self.ui.wordsList.currentItem().data
        self.reset_word_container()
        self.controller.remove_word(word)

    def update_lbl(self):
        i = self.ui.wordsList.currentItem()
        if i:
            i.wid.update_title()

    def reset_word_container(self):
        self.ui.spellingLnEd.clear()
        self.ui.readingLnEd.clear()
        self.ui.translatePte.clear()
