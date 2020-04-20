from PyQt5.QtWidgets import QWidget

from ui.additional_widgets import translate_widget

from module_numbers.editor.number_block_view_ui import Ui_Form
from module_numbers.translator import ModuleTranslator


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
        widgets = [ui.label, ui.label_2, ui.label_3,
                   ui.label_4, ui.label_5, ui.isRangeChbx]
        [translate_widget(w, translator) for w in widgets]

    def init_ui(self):
        self.ui.rangeValueWidget.setVisible(False)

    def connect_widgets(self):
        self.ui.isRangeChbx.toggled.connect(self.controller.set_is_range)
        self.ui.stepSpBx.valueChanged.connect(self.controller.set_step)

        self.ui.singleValueSpBx.valueChanged.connect(self.controller.set_number_value)
        self.ui.rangeFromSpBx.valueChanged.connect(self.controller.set_value_range_from)
        self.ui.rangeToSpBx.valueChanged.connect(self.controller.set_value_range_to)

    def connect_model_signals(self):
        self.model.number_changed += self.load_number

    def load_number(self, number):
        if not number or self.parent() is None:
            return

        self.ui.isRangeChbx.setChecked(number.is_range)
        self.ui.stepSpBx.setValue(number.step)
        self.ui.rangeFromSpBx.setValue(number.value_range[0])
        self.ui.rangeToSpBx.setValue(number.value_range[-1])
        self.ui.singleValueSpBx.setValue(number.value)
