from core.abstractions import AbstractScenarioSerializer
from core.decorators import try_except_wrapper
from .kanji import Kanji
from .storage import KanjiStorage


class KanjiScenarioSerilizer(AbstractScenarioSerializer):

    KEY_ATTR = 'key'

    @try_except_wrapper
    def serialize(self, m_data):
        result = []
        for d in m_data:
            if not isinstance(d, Kanji):
                continue
            sc_part = {attr: getattr(d, attr) for attr in d.__slots__}
            sc_part[self.KEY_ATTR] = getattr(d, self.KEY_ATTR).number
            result.append(sc_part)
        return result

    @try_except_wrapper
    def deserialize(self, sc_data):
        result = []
        storage = KanjiStorage()

        for d in sc_data:
            key_num, value, dash_count = [d[i] for i in Kanji.INIT_ATTRS]
            key = storage.get_key_by_id(key_num)
            kanji = Kanji(key, value, dash_count)
            [setattr(kanji, attr, d[attr])
             for attr in Kanji.__slots__ if attr not in Kanji.INIT_ATTRS]
            result.append(kanji)
        return result
