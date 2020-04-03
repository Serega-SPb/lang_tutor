from core.memento import MementoManager


SEPARATORS = [',', '\n', ';']


def split(txt, seps):
    default_sep = seps[0]
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep) if i]


class EditorBlockController:
    def __init__(self, model):
        self.model = model
        self.memnto_manager = MementoManager()

    def load_block_data(self, data, prop_path):
        self.model.prop_path = prop_path
        self.model.set_word(data)

    def set_word_spelling(self, value):
        self.model.set_word_prop('spelling', value)
        self.model.update_label_event.emit()

    def set_word_reading(self, value):
        self.model.set_word_prop('reading', value)
        self.model.update_label_event.emit()

    def set_word_translate(self, value):
        self.model.set_word_prop('translate', split(value, SEPARATORS))
