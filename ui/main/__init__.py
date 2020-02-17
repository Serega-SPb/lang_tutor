from .main_model import MainModel as Model
from .main_view import MainView as View
from .main_controller import MainController as Controller


def init():
    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    return view
