from hashlib import md5
from functools import wraps
from conf import settings
import logging.config


def get_md(pwd):
    md = md5()
    md.update(b"shop")
    md.update(pwd.encode("utf-8"))
    res = md.hexdigest()
    return res


def check_login(func):
    from core import src
    @wraps(func)
    def inner(*args, **kwargs):
        if src.user_info["user"]:
            res = func(*args, **kwargs)
            return res
        else:
            print("请登陆！")
            src.login()

    return inner


def check_admin_login(func):
    from core import src
    @wraps(func)
    def inner(*args, **kwargs):
        if src.admin_info["user"]:
            res = func(*args, **kwargs)
            return res
        else:
            print("请登陆！")
            src.admin_login()

    return inner


def get_logger(type_name):
    logging.config.dictConfig(settings.LOGGING_DIC)
    logger = logging.getLogger(type_name)
    return logger
