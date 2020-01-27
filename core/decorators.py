import logging
from core import log_config


main_logger = logging.getLogger(log_config.LOGGER_NAME)


def __get_logger(*args):
    if len(args) > 0 and hasattr(args[0], 'logger'):
        return args[0].logger
    else:
        return main_logger


def try_except_wrapper(func):
    def wrapper(*args, **kwargs):
        logger = __get_logger(args)
        func_mod = func.__module__
        func_name = func.__name__
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(f'{func_mod}.{func_name} | {ex}')
        return None
    return wrapper
