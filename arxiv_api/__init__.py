import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename='./logs/info_api.log',
                filemode='w+',
                level=logging.INFO)