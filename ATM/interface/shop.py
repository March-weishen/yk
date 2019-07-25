from .user import check_bal_inter
from .atm import pay_inter
from db import db_handler


def check_cost(username, cost):
    balance = check_bal_inter(username)
    if cost > balance:
        return False
    return True

def shop_pay(username,cost):
    pay_inter(username,cost)
    user_dict = db_handler.check_usernam(username)
    user_dict["shop_car"] = {}
    db_handler.save(user_dict)


def get_shop_car(username):
    user_dict = db_handler.check_usernam(username)
    shop_car = user_dict["shop_car"]
    return shop_car


def save_shop_car(username,shop_car):
    user_dict = db_handler.check_usernam(username)
    old_shop_car = user_dict["shop_car"]

    for i,j in shop_car.items():
        if old_shop_car.get(i):
            old_shop_car[i] += j
        else:
            old_shop_car[i] = j
    user_dict["shop_car"].update(old_shop_car)

    db_handler.save(user_dict)