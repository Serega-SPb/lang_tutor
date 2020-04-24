import os
import sys
import zipfile
import pkgutil
from importlib import util, import_module

from core.abstractions import AbstractModuleInit
from core.decorators import try_except_wrapper
from core.log_config import logger


__module_dir = '../modules'


def get_full_module_dir():
    return os.path.abspath(get_module_dir())


def get_module_dir():
    return __module_dir


def set_module_dir(path):
    if not os.path.isdir(path):
        return
    global __module_dir
    __module_dir = path


@try_except_wrapper
def _get_local_module(name):
    spec = util.find_spec(name)
    if spec:
        return import_module(name)


@try_except_wrapper
def _get_zip_module(name):
    if name.endswith('.zip'):
        name = name[:-4]
    zip_file = os.path.join(get_full_module_dir(), f'{name}.zip')
    if not zipfile.is_zipfile(zip_file):
        return
    sys.path.insert(0, zip_file)
    return import_module('.', package=name)


@try_except_wrapper
def _get_folder_module(name):
    mod_path = os.path.join(get_full_module_dir(), name)
    init_file = os.path.join(mod_path, '__init__.py')
    if not os.path.isdir(mod_path) or not os.path.isfile(init_file):
        return
    spec = util.spec_from_file_location(name, init_file)
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@try_except_wrapper
def _get_init(module):
    sys.modules[module.__name__] = module
    init_mod = import_module('.init', package=module.__name__)
    if not hasattr(init_mod, 'Init'):
        return None
    i = init_mod.Init()
    return i if isinstance(i, AbstractModuleInit) else None


@try_except_wrapper
def get_module_init(name):
    import_funcs = [_get_folder_module, _get_zip_module]
    module, _init = None, None
    while import_funcs and _init is None:
        func = import_funcs.pop(0)
        module = func(name)
        if module:
            _init = _get_init(module)
    if module is None:
        logger.warning(f'Module {name} has not been imported')
    elif _init is None:
        logger.warning(f'{name.capitalize()} module does not implement interface')
    return _init
