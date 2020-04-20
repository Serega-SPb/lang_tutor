import os
import json

from core.decorators import try_except_wrapper
from .cross_widget_events import CrossWidgetEvents


class Locales:
    ENGLISH = 'en'
    RUSSIAN = 'ru'


class Translator:

    DEFAULT_LOCALE_FILE = f'{Locales.ENGLISH}.json'
    LOCALE_DIR = 'locales'
    __translators = {}
    __current_locale = Locales.ENGLISH

    def __init__(self, path_to_locale):
        self.__locale_dict = {}
        self.__path_to_locale = path_to_locale

    @staticmethod
    def register_translator(name, locale_dir):
        tr = Translator(locale_dir)
        tr.load_locale(Translator.__current_locale)
        Translator.__translators[name] = tr

    @staticmethod
    def get_translator(name):
        return Translator.__translators.get(name)

    @staticmethod
    def get_locale():
        return Translator.__current_locale

    @staticmethod
    def set_locale(locale):
        Translator.__current_locale = locale
        [tr.load_locale(locale) for tr in Translator.__translators.values()]
        CrossWidgetEvents.locale_changed_event.emit()

    @try_except_wrapper
    def load_locale(self, locale=Locales.ENGLISH):
        filename = f'{locale}.json'
        filepath = os.path.join(self.__path_to_locale, self.LOCALE_DIR, filename)

        with open(filepath, 'r', encoding='utf-8') as file:
            self.__locale_dict = json.load(file)

    def translate(self, text):
        return self.__locale_dict.get(text.upper(), text)
