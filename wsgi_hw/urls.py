class Url:

    def __init__(self, path, handler, name):
        self.path = path
        self.handler = handler
        self.name = name

    def __call__(self, *args, **kwargs):
        self.handler(*args, **kwargs)

    def __eq__(self, other):
        return other == (self.name if self.name is not None else self.path)

    def __repr__(self):
        return f'Url(name={self.name}, path={self.path})'
