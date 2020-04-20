from ui.translator import Translator


class ModuleTranslator:

    __name = ''

    @staticmethod
    def register(name, directory):
        Translator.register_translator(name, directory)
        ModuleTranslator.__name = name

    @staticmethod
    def get_value():
        return Translator.get_translator(ModuleTranslator.__name)
