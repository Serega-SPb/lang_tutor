import logging
from logging import handlers as hnds
import os
import sys

LOGGER_NAME = 'main'
ROOT = os.getcwd()
DIR_LOG = 'logs'

LOGGING_LVL = logging.DEBUG
FILE_LOG_LVL = logging.DEBUG
STREAM_LOG_LVL = logging.DEBUG

LOG_DIRECTORY = os.path.join(ROOT, DIR_LOG)
LOG_FILENAME = f'{LOGGER_NAME}.log'
ENCODING = 'utf-8'

if not os.path.exists(LOG_DIRECTORY):
    os.mkdir(LOG_DIRECTORY)

BACKUP_COUNT = 10
INTERVAL = 7
WHEN_INTERVAL = 'D'

formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

stream_hnd = logging.StreamHandler(sys.stdout)
stream_hnd.setFormatter(formatter)
stream_hnd.setLevel(STREAM_LOG_LVL)

file_hnd = hnds.TimedRotatingFileHandler(os.path.join(LOG_DIRECTORY, LOG_FILENAME), encoding=ENCODING,
                                         backupCount=BACKUP_COUNT, interval=INTERVAL, when=WHEN_INTERVAL)
file_hnd.setFormatter(formatter)
file_hnd.setLevel(FILE_LOG_LVL)

logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(stream_hnd)
logger.addHandler(file_hnd)
logger.setLevel(LOGGING_LVL)

if __name__ == '__main__':
    logger.critical('Test critical event')
    logger.error('Test error event')
    logger.warning('Test warning event')
    logger.debug('Test debug event')
    logger.info('Test info event')
