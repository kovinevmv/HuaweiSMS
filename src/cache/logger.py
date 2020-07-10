import os
from time import gmtime, strftime

from src.config import otherConfig


if not os.path.exists(otherConfig.CACHE_PATH) and otherConfig.ENABLE_LOGGING:
    os.makedirs(otherConfig.CACHE_PATH)

LOG_PATH = os.path.join(otherConfig.CACHE_PATH, 'log.txt')


class Logger:
    @staticmethod
    def log(msg, type=None):
        if otherConfig.ENABLE_LOGGING:
            Logger.log_in_file(f'[{Logger.now()}] ')
            if type:
                Logger.log_in_file(type.upper() + ' ')
            Logger.log_in_file(msg + '\n')

    @staticmethod
    def now():
        return strftime("%d-%m-%Y %H:%M:%S", gmtime())

    @staticmethod
    def log_in_file(string):
        with open(LOG_PATH, 'a+', encoding='utf-8', errors='ignore') as f:
            f.write(string)
