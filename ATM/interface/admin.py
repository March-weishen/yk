from db import db_handler
from lib import comment

def lock_inter(username):
    user_dict = db_handler.check_usernam(username)
    user_dict["lock"] = True
    db_handler.save(user_dict)

def unlock_inter(username):
    user_dict = db_handler.check_usernam(username)
    user_dict["lock"] = False
    db_handler.save(user_dict)


def chang_inter(username,balance):
    user_dict = db_handler.check_usernam(username)
    user_dict["balance"] = float(balance)
    db_handler.save(user_dict)


def check(input_name):
    admin_dict = db_handler.check_admin(input_name)
    if admin_dict:
        return True

def login(input_name,input_pwd):
    user_dict = db_handler.check_usernam(input_name)

    pwd = comment.get_md(input_pwd)


    if pwd == user_dict["pwd"]:
        return True