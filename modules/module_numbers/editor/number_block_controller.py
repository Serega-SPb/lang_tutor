
class EditorBlockController:
    def __init__(self, model):
        self.model = model

    def load_block_data(self, data, prop_path):
        self.model.prop_path = prop_path
        self.model.set_number(data)

    def set_number_value(self, value):
        self.model.set_number_prop('value', value)
        self.model.update_label_event.emit()

    def set_value_range_from(self, value):
        self.model.set_number_prop('value_range.[0]', value)
        self.model.update_label_event.emit()

    def set_value_range_to(self, value):
        self.model.set_number_prop('value_range.[1]', value)
        self.model.update_label_event.emit()

    def set_is_range(self, value):
        self.model.set_number_prop('is_range', value)
        self.model.update_label_event.emit()

    def set_step(self, value):
        self.model.set_number_prop('step', value)
        self.model.update_label_event.emit()
