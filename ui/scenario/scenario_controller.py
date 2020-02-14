import random

from PyQt5.QtWidgets import QMessageBox

from core.data_loader import DataLoader


class ScenarioController:

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.data_loader = DataLoader()

    def load_scenario(self, scenario, q_type, opt_enb=True):  # ?
        self.model.name = scenario.name
        exercises = []
        for m, bl in scenario.get_data().items():
            mod = self.data_loader.modules[m].init
            tuple_lamb = lambda x: (m, x)
            exercises.extend(list(map(tuple_lamb, mod.get_exercises(bl, q_type, opt_enb))))
        random.shuffle(exercises)
        self.model.set_exercises(exercises)

    def accept_answer(self, answer):
        self.model.check_answer(answer)

    def end_scenario(self):
        QMessageBox.information(None, 'Results', f'Correct answers: {self.model.correct_count}/{self.model.total}')
        self.model.scenario_ended.emit()
