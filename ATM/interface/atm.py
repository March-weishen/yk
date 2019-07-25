from db import db_handler


def withdraw_inter(username,money):
    user_dict = db_handler.check_usernam(username)
    if float(money) > user_dict["balance"]:
        return False
    user_dict["balance"] = user_dict["balance"] - float(money)
    a = 0.05*float(money)
    b = user_dict["balance"]
    db_handler.save(user_dict)
    c = "提现{}元，手续费{}元,还剩{}".format(money,a,b)
    user_dict["flow"].append(c)
    db_handler.save(user_dict)
    return c


def repay_inter(username,money):
    user_dict = db_handler.check_usernam(username)
    user_dict["balance"] = user_dict["balance"] + float(money)
    user_dict["flow"].append("还款{}元".format(money))
    db_handler.save(user_dict)


def transfer_inter(username,to_username,money):
    user_dict = db_handler.check_usernam(username)
    to_user_dict = db_handler.check_usernam(to_username)
    if float(money) > user_dict["balance"]:
        return False
    user_dict["balance"] = user_dict["balance"] - float(money)
    user_dict["flow"].append("给{}转账{}元".format(to_username,money))
    to_user_dict["balance"] = to_user_dict["balance"] + float(money)
    to_user_dict["flow"].append("{}给您转账{}元".format(username,money))
    db_handler.save(user_dict)
    db_handler.save(to_user_dict)
    return True


def pay_inter(username,cost):
    user_dict = db_handler.check_usernam(username)
    user_dict["balance"] = user_dict["balance"] - cost
    user_dict["flow"].append("购物支付{}元".format(cost))
    db_handler.save(user_dict)
