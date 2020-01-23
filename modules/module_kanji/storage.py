from core.metaclasses import Singleton


class KanjiStorage(metaclass=Singleton):

    __kanji_keys_file = 'keys.json'
    kanji_keys = []
    scenario_kanji = []

    def __init__(self):
        self.load_keys()

    def load_keys(self):
        pass

    def load_scenario_kanji(self, scenario_data):
        # TODO parse sc_data
        pass
