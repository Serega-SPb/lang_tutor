from PyQt5.QtWidgets import QWidget

from .scenario_view_ui import Ui_Form
from ui.ui_messaga_bus import Event
from ui.exercise_ui_manager import ExerciseManager


class ScenarioView(QWidget):

    returnToMenuEvent = Event()

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller
        self.exercise_manager = ExerciseManager()
        self.current_exercise_widget = None

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.init_ui()
        self.connect_widgets()
        self.connect_model_signals()

    def init_ui(self):
        self.ui.backMenuBtn.clicked.connect(lambda x: self.returnToMenuEvent.emit())
        self.ui.totalLbl.setText(str(self.model.total))

    def connect_widgets(self):
        self.ui.answerBtn.clicked.connect(
            lambda x: self.controller.accept_answer(self.current_exercise_widget.answer))

    def connect_model_signals(self):
        self.model.name_changed += lambda x: self.ui.scenarioLbl.setText(x)
        self.model.scenario_ended += self.returnToMenuEvent.emit
        self.model.scenario_loaded += self.set_counter
        self.model.current_exercise_changed += self.load_exercise

    def load_exercise(self, exercise):
        if exercise:
            self.ui.currentLbl.setText(str(self.model.index + 1))

            if self.current_exercise_widget:
                self.ui.exerciseLayout.removeWidget(self.current_exercise_widget)
                self.current_exercise_widget.setParent(None)

            self.current_exercise_widget = self.exercise_manager.get_widget(*exercise, self)
            self.ui.exerciseLayout.addWidget(self.current_exercise_widget)
        else:
            self.controller.end_scenario()

    def set_counter(self):
        self.ui.currentLbl.setText(str(self.model.index + 1))
        self.ui.totalLbl.setText(str(self.model.total))
