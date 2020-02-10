from core.exercise import Exercise
from ui.ui_messaga_bus import Event


class ScenarioModel:

    name_changed = Event(str)
    current_exercise_changed = Event(Exercise)
    scenario_loaded = Event()
    scenario_ended = Event()

    def __init__(self):
        self._name = 'NONE'
        self.exercises = []
        self._index = 0
        self.correct_count = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)

    @property
    def current_exercise(self):
        return self.exercises[self.index] if self.index < self.total else None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        self.current_exercise_changed.emit(self.current_exercise)

    @property
    def total(self):
        return len(self.exercises)

    def set_exercises(self, exercises):
        self.reset()
        self.exercises = exercises
        self.scenario_loaded.emit()
        self.current_exercise_changed.emit(self.current_exercise)

    def check_answer(self, answer):
        self.correct_count += 1 if self.current_exercise[1].check_answer(answer) else 0
        self.index += 1

    def reset(self):
        self._index = 0
        self.correct_count = 0
