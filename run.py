import argparse
from pdf_reader_module.main import *
from pdf_reader_module import logging

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description = 'PDF GD saver')
        parser.add_argument('--path', help='path to config file')
        args = parser.parse_args()
        print(args.path)
        main_app(args.path)
    except Exception as e:
        logging.error("Unexpected error", exc_info=True)


