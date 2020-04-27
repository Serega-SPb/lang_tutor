from PyQt5.QtWidgets import QWidget

from core.decorators import try_except_wrapper
from .scenario_view_ui import Ui_Form
from ..additional_widgets import translate_widget
from ..translator import Translator


class ScenarioView(QWidget):

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller
        self.current_exercise_widget = None

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.translate_ui()

        self.connect_widgets()
        self.connect_model_signals()

    def translate_ui(self):
        ui = self.ui
        translator = Translator.get_translator('main')
        widgets = [ui.answerBtn, ui.backMenuBtn]
        [translate_widget(w, translator) for w in widgets]

    def connect_widgets(self):
        self.ui.backMenuBtn.clicked.connect(self.controller.back_to_menu)
        self.ui.answerBtn.clicked.connect(
            lambda x: self.controller.accept_answer(self.current_exercise_widget.answer))

    def connect_model_signals(self):
        self.model.name_changed += lambda x: self.ui.scenarioLbl.setText(x)
        self.model.scenario_ended += self.controller.back_to_menu
        self.model.scenario_loaded += self.set_counter
        self.model.current_exercise_changed += self.load_exercise

    @try_except_wrapper
    def load_exercise(self, index, exercise_wid):
        if self.current_exercise_widget:
            self.ui.exerciseLayout.removeWidget(self.current_exercise_widget)
            self.current_exercise_widget.setParent(None)
            self.current_exercise_widget.send_answer_event -= self.ui.answerBtn.click
            self.current_exercise_widget = None

        if exercise_wid:
            self.ui.currentLbl.setText(str(index + 1))
            exercise_wid.setParent(self)
            self.current_exercise_widget = exercise_wid
            self.current_exercise_widget.send_answer_event += self.ui.answerBtn.click
            self.ui.exerciseLayout.addWidget(self.current_exercise_widget)
            self.current_exercise_widget.setFocus()
        else:
            self.controller.end_scenario()

    def set_counter(self, index, total):
        self.ui.currentLbl.setText(str(index + 1))
        self.ui.totalLbl.setText(str(total))
