class NotifyProperty:
    __slots__ = ('name', 'value', 'subscribers')

    def __init__(self, name, default_value=None):
        self.name = name
        self.subscribers = []
        self.value = default_value

    def get(self):
        return self.value

    def set(self, value):
        if self.value == value:
            return
        self.value = value
        [s(value) for s in self.subscribers if callable(s)]

    def __iadd__(self, other):
        self.subscribers.append(other)
        return self

    def __isub__(self, other):
        self.subscribers.remove(other)
        return self

    def __eq__(self, other):
        return self.value == other

    def __str__(self):
        return str(self.value)
