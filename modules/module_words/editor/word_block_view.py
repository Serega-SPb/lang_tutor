from PyQt5.QtWidgets import QWidget

from .word_block_view_ui import Ui_Form


class EditorBlockView(QWidget):

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.connect_widgets()
        self.connect_model_signals()

    def connect_widgets(self):
        self.ui.spellingLnEd.textEdited.connect(self.controller.set_word_spelling)
        self.ui.readingLnEd.textEdited.connect(self.controller.set_word_reading)
        self.ui.translatePte.textChanged.connect(
            lambda: self.controller.set_word_translate(self.ui.translatePte.toPlainText()))

    def connect_model_signals(self):
        self.model.word_changed += self.load_word

    def load_word(self, value):
        if not value or self.parent() is None:
            return
        self.ui.spellingLnEd.setText(value.spelling)
        self.ui.readingLnEd.setText(value.reading)
        self.ui.translatePte.setPlainText(', '.join(value.translate))
