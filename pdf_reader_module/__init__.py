#import pdf_reader_module

import logging
'''
logger = logging.getLogger('pdf_app')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('./logs/info.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
#ch = logging.FileHandler("./logs/error.log")
#ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
#ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
#logger.addHandler(ch)
'''
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='./logs/info_parsing.log',
                filemode='w+',
                level=logging.INFO)



