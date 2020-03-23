from .editor_model import EditorModel as Model
from .editor_view import EditorView as View
from .editor_controller import EditorController as Controller


def init():
    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    return view
