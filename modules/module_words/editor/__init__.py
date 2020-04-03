from .word_block_model import EditorBlockModel as Model
from .word_block_view import EditorBlockView as View
from .word_block_controller import EditorBlockController as Controller


def init():
    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    return view
