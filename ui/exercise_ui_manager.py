from core.exercise import ExerciseWithOptions
from .base_exercise_widgets import ExerciseWidget, ExerciseOptWidget


def get_widget(mod_init, exercise, parent=None):
    if isinstance(exercise, ExerciseWithOptions):
        widget = mod_init.get_exercise_opt_widget() or ExerciseOptWidget
    else:
        widget = mod_init.get_exercise_widget() or ExerciseWidget
    return widget(exercise, parent)
