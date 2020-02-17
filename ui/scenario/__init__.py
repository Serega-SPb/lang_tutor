from .scenario_model import ScenarioModel as Model
from .scenario_view import ScenarioView as View
from .scenario_controller import ScenarioController as Controller


def init():
    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    return view
