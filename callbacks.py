# callbacks.py
import logging
#import inspect

# import component's callbacks
import components.ivs.callbacks as ivs
import components.stock.callbacks as stock

# initialize logger
from helper.misc import log_current_function
logger = logging.getLogger(__name__)

def register_callbacks(app):
    '''
    Calls the register_callback functions of the main components
    :param app: Dash app instance
    :return: None
    '''
    log_current_function(level=logging.INFO, msg=f"{__name__}")

    stock.register_callbacks(app)
    ivs.register_callbacks(app)