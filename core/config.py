from abc import ABC, abstractmethod


class ConfigComponent(ABC):

    def __init__(self, name):
        self.name = name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def add(self, component):
        pass

    def remove(self, component):
        pass

    def set_param(self, param_path, value):
        pass

    @abstractmethod
    def get_param(self, param_path):
        pass

    @abstractmethod
    def get_dict(self):
        pass


def parse_path(param_path):
    path = param_path.split('.', 1)
    param = path[0]
    path = path[1] if len(path) == 2 else None
    return param, path


def _create_config_part(name, data):
    if not isinstance(data, dict):
        return ConfigParam(name, data)
    cfg = Config(name)
    for key, value in data.items():
        cfg.add(_create_config_part(key, value))
    return cfg


def create_config(data):
    if not data:
        return Config('root')
    return _create_config_part('root', data)


class Config(ConfigComponent):

    def __init__(self, name):
        super().__init__(name)
        self._children = {}

    def add(self, component: ConfigComponent):
        self._children[component.name] = component
        component.parent = self

    def remove(self, component: ConfigComponent):
        self._children.pop(component.name)
        component.parent = None

    def get_children(self):
        return self._children

    def __getitem__(self, item):
        return self._children[item] \
            if item in self._children.keys() else None

    def set_param(self, param_path, value):
        param, part_path = parse_path(param_path)
        if part_path is None:
            cfg_p = ConfigParam(param, value)
            self._children[param] = cfg_p
            return
        if param in self._children.keys():
            self._children[param].set_param(part_path, value)
        else:
            cfg = Config(param)
            cfg.set_param(part_path, value)
            self._children[param] = cfg

    def get_param(self, param_path):
        if param_path is None:
            return self
        param, path = parse_path(param_path)
        return self._children[param].get_param(path) \
            if param in self._children else None

    def get_dict(self):
        return {n: p.get_dict() for n, p in self._children.items()}


class ConfigParam(ConfigComponent):

    def __init__(self, name, value):
        super().__init__(name)
        self._value = value

    def set_param(self, param_path, value):
        self._value = value

    def get_param(self, param_path=None):
        return self._value

    def get_dict(self):
        return self._value
