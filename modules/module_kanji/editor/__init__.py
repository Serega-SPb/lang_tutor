from .kanji_block_model import EditorBlockModel as Model
from .kanji_block_view import EditorBlockView as View
from .kanji_block_controller import EditorBlockController as Controller


def init():
    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    return view
