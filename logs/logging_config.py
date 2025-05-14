import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,  # set log level (INFO, DEBUG, WARNING, ERROR, CRITICAL
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # console
        logging.FileHandler("./logs/app.log", mode='a', encoding='utf-8')  # file
    ]
)

