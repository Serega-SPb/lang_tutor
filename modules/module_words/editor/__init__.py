from .editor_block_model import EditorBlockModel as Model
from .editor_block_view import EditorBlockView as View
from .editor_block_controller import EditorBlockController as Controller


def init():
    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    return view
