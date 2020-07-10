import argparse

from src.api.API import API
from src.cache.logger import Logger
from src.formatter.formatter import Formatter


def main():
    description = 'Huawei e3372h API'

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', action="store_true", default=False, help='Get current status')
    parser.add_argument('-m', action="store_true", default=False, help='Send new SMS to email')

    args = parser.parse_args()

    if args.s:
        Formatter.format_status(API().get_total_status())



if __name__ == '__main__':
    main()