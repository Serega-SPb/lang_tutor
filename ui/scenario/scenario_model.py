from ui.ui_messaga_bus import Event


class ScenarioModel:

    name_changed = Event(str)
    current_exercise_changed = Event(int, object)
    scenario_loaded = Event(int, int)
    scenario_ended = Event()

    def __init__(self):
        self._name = 'NONE'
        self.exercises = []
        self.widgets = []
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
    def current_widget(self):
        return self.widgets[self.index] if self.index < self.total else None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        self.current_exercise_changed.emit(value, self.current_widget)

    @property
    def total(self):
        return len(self.exercises)

    def set_exercises(self, exercises_wids_tuple):
        self.reset()
        self.widgets, self.exercises = zip(*exercises_wids_tuple)
        self.scenario_loaded.emit(self.index, self.total)
        self.current_exercise_changed.emit(self.index, self.current_widget)

    def check_answer(self, answer):
        self.correct_count += 1 if self.current_exercise.check_answer(answer) else 0
        self.index += 1

    def reset(self):
        self._index = 0
        self.correct_count = 0
