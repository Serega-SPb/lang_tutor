from core.metaclasses import Singleton
from core.data_loader import DataLoader
from core.exercise import ExerciseWithOptions
from .base_exercise_widgets import ExerciseWidget, ExerciseOptWidget


class ExerciseManager(metaclass=Singleton):

    def __init__(self):
        self.data_loader = DataLoader()
        self.logger = self.data_loader.logger

    def get_widget(self, mod_name, exercise, parent=None):
        if mod_name not in self.data_loader.modules:
            self.logger.warning(f'Module {mod_name} not found')
            return
        mod_init = self.data_loader.modules[mod_name].init

        if isinstance(exercise, ExerciseWithOptions):
            widget = mod_init.get_exercise_opt_widget() or ExerciseOptWidget
        else:
            widget = mod_init.get_exercise_widget() or ExerciseWidget
        return widget(exercise, parent)
