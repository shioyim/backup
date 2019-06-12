
import logging
import logging.handlers




logger = logging.getLogger(__name__)

LOG_LEVEL = "INFO"
logger_level= dict(
    DEBUG = logging.DEBUG,
    INFO  = logging.INFO,
    WARNING = logging.WARNING,
    ERROR = logging.ERROR,
    CRITICAL = logging.CRITICAL
    )






stream_handler = logging.StreamHandler()
#file_hander = logging.FileHandler(filename="test.log")

# formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
#file_hander.setFormatter(formatter)


stream_handler.setFormatter(formatter)
#file_hander.setFormatter(formatter)


logger.setLevel(level=logger_level[LOG_LEVEL])
#file_hander.setLevel(logger_level[LOG_LEVEL])


logger.addHandler(stream_handler)
#logger.addHandler(file_hander)

debug = logger.debug
info  = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical


loggers = dict(
    debug = debug,
    info  = info,
    warning = warning,
    error = error,
    critical = critical
    )


# def check(courier):

#     try:
#         assert courier in loggers,"%s Not an available courier!"%courier
#         error = False
#     except AssertionError as e:
#         loggers["error"](e)
#         error = True

#     def decorator(func):    
#         def wrapper(*args, **kw):
#             try: 
#                 if error:
#                     return None
#                 else:
#                     func(*args, **kw) 
#             except Exception as e: 
#                 loggers[courier](e)
#         return wrapper 
#     return decorator



def check(courier):

    try:
        assert courier in loggers,"%s Not an available courier!"%courier
        is_error = False
    except AssertionError as e:
        loggers["error"](e)
        is_error = True

    def decorator(func):    
        def wrapper(*args, **kw):
            try: 
                if is_error:
                    return None
                else:
                    f = func(*args, **kw) 
                    return f
            except Exception as e: 
                loggers[courier](e)
        return wrapper 
    return decorator










# from utils import logger    
# @logger.check("info")
# def test():
#     logger.warning("print debug info")
#     assert False,"Raise a AssertionError!"
#     print("Test pass!")


# if __name__ == '__main__':
#     test()
