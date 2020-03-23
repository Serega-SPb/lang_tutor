import os
import logging
import json

from core.log_config import LOGGER_NAME
from core.metaclasses import Singleton
from core.decorators import try_except_wrapper

from .kanji import KanjiKey


class KanjiStorage(metaclass=Singleton):

    __kanji_keys_file = 'KanjiKeys.json'
    kanji_keys = {}

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.load_keys()

    @try_except_wrapper
    def load_keys(self):
        file = os.path.join(os.path.dirname(__file__), self.__kanji_keys_file)
        if not os.path.exists(file):
            raise FileNotFoundError('Kanji keys file not found')

        with open(file, 'r') as file:
            js_keys = json.load(file)

        for js in js_keys:
            init_args = [js[i] for i in KanjiKey.INIT_ATTRS]
            key = KanjiKey(*init_args)
            for attr in KanjiKey.__slots__:
                if attr not in KanjiKey.INIT_ATTRS and attr in js.keys():
                    setattr(key, attr, js[attr])
            self.kanji_keys[key.number] = key

    def get_key_by_id(self, num):
        if num not in self.kanji_keys.keys():
            self.logger.warning(f'KanjiKey with id = {num} not found')
            return
        return self.kanji_keys.get(num)
