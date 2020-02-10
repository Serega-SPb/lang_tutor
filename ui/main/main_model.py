from core.data_loader import DataLoader

from ui.ui_messaga_bus import Event


class MainModel:

    modules_changed = Event()
    scenarios_changed = Event()

    def __init__(self):
        self.data_loader = DataLoader()

    @property
    def modules(self):
        return self.data_loader.modules.values()

    @property
    def scenarios(self):
        return self.data_loader.scenarios.values()

    # TODO ? propertiess: current_scenario | exercises | current exercise
