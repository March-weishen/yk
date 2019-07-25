from db import db_handler
from hashlib import md5


def check_username(input_name):
    user_dict = db_handler.check_usernam(input_name)
    if user_dict:
        return True


def register_inter(input_name,input_pwd):
    md = md5()
    md.update(b"shop")
    md.update(input_pwd.encode("utf-8"))
    input_pwd = md.hexdigest()
    user_dict = {
        "user": input_name,
        "pwd": input_pwd,
        "balance": 15000,
        "flow": [],
        "shop_car": {},
        "lock": False
    }
    db_handler.save(user_dict)


def login(input_name,input_pwd):
    user_dict = db_handler.check_usernam(input_name)
    md = md5()
    md.update(b"shop")
    md.update(input_pwd.encode("utf-8"))
    input_pwd = md.hexdigest()

    if input_pwd == user_dict["pwd"]:
        return True


def check_bal_inter(input_name):
    bal = db_handler.check_usernam(input_name)["balance"]
    return bal


def check_flow_inter(username):
    user_dict = db_handler.check_usernam(username)
    flow = user_dict["flow"]
    return flow


def check_lock(username):
    user_dict = db_handler.check_usernam(username)

    if user_dict["lock"]:
        return True