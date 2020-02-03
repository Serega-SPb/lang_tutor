import logging
from threading import Thread
from queue import Queue

from core.log_config import LOGGER_NAME
from core.metaclasses import Singleton


class Event:
    def __init__(self, *arg_types):
        self.__subscribers = []
        self.arg_types = arg_types

    def __iadd__(self, func):
        self.__subscribers.append(func)
        return self

    def __isub__(self, func):
        self.__subscribers.remove(func)
        return self

    def emit(self, *args):
        [sub(*args) for sub in self.__subscribers]
        # [MessageBus.put_in_queue(sub, args) for sub in self.__subscribers]


class MessageBus(metaclass=Singleton):

    __execute_queue = Queue()

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.__executor_thread = Thread(target=self.__loop, daemon=True)
        self.__executor_thread.start()

    def __call__(self, *args, **kwargs):
        print('CALL')

    def __loop(self):
        while True:
            func, *args = self.__execute_queue.get()
            self.logger.debug(f'{func} | {args}')
            try:
                func(*args)
            except Exception as e:
                self.logger.error(e)

    @staticmethod
    def put_in_queue(func, args):
        if MessageBus.instance is None:
            MessageBus()

        MessageBus.__execute_queue.put((func, *args))
