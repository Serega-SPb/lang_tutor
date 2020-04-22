from abc import ABC, abstractmethod


class AbstractModuleInit(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_question_types(self):
        pass

    @staticmethod
    @abstractmethod
    def translate_local(var):
        pass

    @abstractmethod
    def get_exercises(self, scenario_block, question_type, ex_with_opt=True):
        pass

    @abstractmethod
    def serialize_block(self, data):
        pass

    @abstractmethod
    def deserialize_block(self, data):
        pass

    @abstractmethod
    def get_exercise_widget(self):
        pass

    @abstractmethod
    def get_exercise_opt_widget(self):
        pass

    @abstractmethod
    def get_editor_listitem_widget_cls(self):
        pass

    @abstractmethod
    def get_editor_block_widget(self):
        pass

    @abstractmethod
    def create_new_data_object(self):
        pass


class AbstractQuestionGenerator(ABC):

    @abstractmethod
    def get_questions(self, quest_type):
        pass


class AbstractScenarioSerializer(ABC):

    @abstractmethod
    def serialize(self, m_data):
        pass

    @abstractmethod
    def deserialize(self, sc_data):
        pass
