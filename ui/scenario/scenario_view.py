from PyQt5.QtWidgets import QWidget

from core.decorators import try_except_wrapper
from .scenario_view_ui import Ui_Form
from ui.exercise_ui_manager import ExerciseManager
from ..additional_widgets import translate_widget


class ScenarioView(QWidget):

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller
        self.exercise_manager = ExerciseManager()
        self.current_exercise_widget = None

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.translate_ui()

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

    def translate_ui(self):
        ui = self.ui
        widgets = [ui.answerBtn, ui.backMenuBtn]
        [translate_widget(w) for w in widgets]

    def init_ui(self):
        self.ui.totalLbl.setText(str(self.model.total))

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
    def load_exercise(self, exercise):

        if self.current_exercise_widget:
            self.ui.exerciseLayout.removeWidget(self.current_exercise_widget)
            self.current_exercise_widget.setParent(None)
            self.current_exercise_widget.send_answer_event -= self.ui.answerBtn.click
            self.current_exercise_widget = None

        if exercise:
            self.ui.currentLbl.setText(str(self.model.index + 1))
            self.current_exercise_widget = self.exercise_manager.get_widget(*exercise, self)
            self.current_exercise_widget.send_answer_event += self.ui.answerBtn.click
            self.ui.exerciseLayout.addWidget(self.current_exercise_widget)
            self.current_exercise_widget.setFocus()
        else:
            self.controller.end_scenario()

    def set_counter(self):
        self.ui.currentLbl.setText(str(self.model.index + 1))
        self.ui.totalLbl.setText(str(self.model.total))
