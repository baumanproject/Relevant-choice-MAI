import argparse
from pdf_reader_module.main import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'PDF GD saver')
    parser.add_argument('--path', help='path to config file')
    args = parser.parse_args()
    #print(args.path)
    main_app(args.path)
    # google Api setting

