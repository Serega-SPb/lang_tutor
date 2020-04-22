from PyQt5.QtWidgets import QWidget

from core.decorators import try_except_wrapper
from ui.additional_widgets import translate_widget

from module_kanji.editor.additional_widgets_kan import KeyComboBox
from module_kanji.editor.kanji_block_view_ui import Ui_Form
from module_kanji.translator import ModuleTranslator


class EditorBlockView(QWidget):

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
        translator = ModuleTranslator.get_value()
        widgets = [ui.label, ui.label_3, ui.label_4,
                   ui.label_5, ui.label_6, ui.label_7]
        [translate_widget(w, translator) for w in widgets]

    def init_ui(self):
        self.ui.keyCmbBx = KeyComboBox.morph_from(self.ui.keyCmbBx)
        self.ui.horizontalLayout_4.addWidget(self.ui.keyCmbBx)

    def connect_widgets(self):
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
        self.model.keys_changed += self.load_keys
        self.model.kanji_changed += self.load_kanji

    def load_keys(self, values):
        self.ui.keyCmbBx.load_data(values)

    def load_kanji(self, kanji):
        if not kanji or self.parent() is None:
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
            return
        self.controller.set_kanji_key(curr_key)
