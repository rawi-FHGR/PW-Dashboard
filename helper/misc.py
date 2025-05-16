import logging
import inspect

logger = logging.getLogger(__name__)  # logger pro Modul

def log_current_function(level=logging.INFO, msg=""):
    func_name = inspect.currentframe().f_back.f_code.co_name
    logger.log(level, f"{func_name}(): {msg}")