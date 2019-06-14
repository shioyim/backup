
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



def check(courier,infomation=""):

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
                    result = func(*args, **kw) 
                    
            except Exception as e: 
                if infomation:
                    loggers[courier](infomation) 
                else:
                    loggers[courier](e)                    
                result = None
            return result
        return wrapper 
    return decorator




async def run(func,courier="error",infomation="",**kw):       
     try:
        assert courier in loggers,"%s Not an available courier!"%courier
        is_error = False
     except AssertionError as e:
        loggers["error"](e)
        is_error = True

     try:
         if is_error:
             return None
         result = func(**kw) 
     except Exception as e: 
        if infomation:
            loggers[courier](infomation) 
        else:
            loggers[courier](e)
        result = None 
     return result 
 
 



#infomation 自定义消息 courier传信类型，就是所谓的debug、info、error 等等
#除非你忽略了错误消息，否则一般不建议自定义消息，自定义消息意味着无论发生什么样的错误类型，消息都是自定义的。
#exmple:
#def f(x,y):
#    return x/y
#result = await run(f,x=1,y=0,courier="info") 
#out#2019-06-13 21:23:22,756-INFO-division by zero
#result = await run(f,x=1,y=0,courier="error",infomation="y can not use zore.") 
#out# 2019-06-13 21:25:35,479-ERROR-y can not use zore.



#@check("info") 
#    def test(): 
#        assert False,"Raise a AssertionError!"  

#test()
#out#2019-06-13 21:49:47,712-INFO-Raise a AssertionError!


#test()
#@check("info","custom infomation!") 
#    def test(): 
#        assert False,"Raise a AssertionError!" 
#out#2019-06-13 21:50:56,175-INFO-custom infomation!



