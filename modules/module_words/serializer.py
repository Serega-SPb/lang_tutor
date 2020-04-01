from core.abstractions import AbstractScenarioSerializer
from core.decorators import try_except_wrapper
from .word import Word


class WordsScenarioSerilizer(AbstractScenarioSerializer):

    @try_except_wrapper
    def serialize(self, m_data):
        result = []
        for d in m_data:
            if not isinstance(d, Word):
                raise ValueError('Incorrect data type')
            sc_part = {attr: getattr(d, attr) for attr in d.__slots__}
            result.append(sc_part)
        return result

    @try_except_wrapper
    def deserialize(self, sc_data):
        result = []
        for d in sc_data:
            word = Word(*[d[attr] for attr in Word.__slots__])
            result.append(word)
        return result
