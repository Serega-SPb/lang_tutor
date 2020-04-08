from core.abstractions import AbstractScenarioSerializer
from core.decorators import try_except_wrapper
from .number_data import NumberData


class NumbersScenarioSerilizer(AbstractScenarioSerializer):

    @try_except_wrapper
    def serialize(self, m_data):
        result = []
        for d in m_data:
            if not isinstance(d, NumberData):
                raise ValueError('Incorrect data type')
            sc_part = {attr: getattr(d, attr) for attr in d.__slots__}
            result.append(sc_part)
        return result

    @try_except_wrapper
    def deserialize(self, sc_data):
        result = []
        for d in sc_data:
            num_data = NumberData(*[d[attr] for attr in NumberData.__slots__])
            result.append(num_data)
        return result
