from interface import user, atm, shop, admin
from lib import comment

user_info = {"user": ""}

admin_info = {"user": ""}


def register():
    logger = comment.get_logger("注册")
    while True:
        input_name = input("请输入你要注册的用户名：").strip()
        flag = user.check_username(input_name)
        if flag:
            print("用户名已存在，请重新输入！")
            continue
        input_pwd = input("请输入密码：").strip()
        re_input_pwd = input("请再次确认密码：").strip()
        if input_pwd == re_input_pwd:
            user.register_inter(input_name, input_pwd)
            print("注册成功！")
            logger.debug("{}注册成功！".format(input_name))
            return
        logger.debug("注册失败！")
        print("两次密码不一致！请重新注册！")


def login():
    logger = comment.get_logger("登陆")
    while True:
        input_name = input("请输入你的用户名：").strip()
        flag = user.check_username(input_name)
        if not flag:
            print("用户名不存在！请重新输入！")
            continue
        ret = user.check_lock(input_name)
        if ret:
            print("账户被锁定！")
            logger.debug("{}尝试登陆，账号被锁定，登陆失败！".format(input_name))
            return
        input_pwd = input("请输入密码：").strip()
        res = user.login(input_name, input_pwd)
        if not res:
            print("密码不正确，请重新输入！")
            logger.debug("{}尝试登陆，密码输入错误，登陆失败！".format(input_name))
            continue
        user_info["user"] = input_name
        logger.debug("{}登陆成功！".format(input_name))
        print("登陆成功！")
        return


# 查看余额
@comment.check_login
def check_bal():
    logger = comment.get_logger("查看余额")
    bal = user.check_bal_inter(user_info["user"])
    print("{}剩余{}元".format(user_info["user"], bal))
    logger.debug("{}剩余{}元".format(user_info["user"], bal))
    return


# 提现
@comment.check_login
def withdraw():
    logger = comment.get_logger("提现操作")
    while True:
        money = input("请输入你要提现的金额：").strip()
        if not money.isdigit():
            print("请输入数字！")
            continue
        flag = atm.withdraw_inter(user_info["user"], money)
        if not flag:
            print("余额不足！请充值！")
            logger.debug("{}尝试提现，余额不足，提现失败！".format(user_info["user"]))
            continue
        print(flag)
        logger.debug("{}提现成功，提取现金{}元".format(user_info["user"],money))
        return


# 还款
@comment.check_login
def repay():
    logger = comment.get_logger("还款")
    while True:
        money = input("请输入还款金额：").strip()
        if not money.isdigit():
            print("请输入数字！")
            continue
        atm.repay_inter(user_info["user"], money)
        print("还款成功！")
        logger.debug("{}成功还款{}元".format(user_info["user"],money))
        return


# 转账
@comment.check_login
def transfer():
    logger = comment.get_logger("转账")
    while True:
        to_username = input("请输入对方账户名：").strip()
        flag = user.check_username(to_username)
        if not flag:
            print("账户不存在！请重新输入！")
            continue
        money = input("请输入你要转账的金额：").strip()
        if not money.isdigit():
            print("请输入数字！")
            continue
        res = atm.transfer_inter(user_info["user"], to_username, money)
        if not res:
            print("余额不足，转账失败！")
            logger.debug("{}尝试给{}转账，余额不足，转账失败".format(user_info["user"],to_username))
            continue
        print("转账成功！")
        logger.debug("{}给{}转账{}元。".format(user_info["user"], to_username,money))
        return


# 查看流水
@comment.check_login
def check_flow():
    flow = user.check_flow_inter(user_info["user"])
    for i in flow:
        print(i)
    return


@comment.check_login
def shopping():
    goods_list = [
        ["坦克", 100],
        ["飞机", 200],
        ["火箭", 300],
        ["飞船", 400],
    ]

    cost = 0
    choose_shop_car = input("是否加载购物车车已存在的商品(y/n)?")
    if choose_shop_car.lower() == "y":
        shop_car = shop.get_shop_car(user_info["user"])
        for m, n in shop_car.items():
            for g in goods_list:
                if m in g:
                    spend = g[1] * n
                    cost += spend
    else:
        shop_car = {}

    while True:
        for i, j in enumerate(goods_list):
            detail = "{}单价{}元".format(j[0], j[1])
            print(i + 1, detail, sep="    ")
        choose_num = input("请输入对应商品的序号(q退出)：")
        if choose_num == "q":
            choose = input("结束购物并支付(y)/保存购物车并退出(n)")
            if choose.lower() == "y":
                shop.shop_pay(user_info["user"], cost)
                print("支付成功")
                return
            print(shop_car)
            shop.save_shop_car(user_info["user"], shop_car.cost)
            print("购物车保存成功！")
            return
        if not choose_num.isdigit():
            print("请输入数字！")
            continue
        if int(choose_num) > len(goods_list) and int(choose_num) < 0:
            print("输入的序号不存在")
            continue
        good_name, good_price = goods_list[int(choose_num) - 1]
        cost += good_price
        flag = shop.check_cost(user_info["user"], cost)
        if not flag:
            print("余额不足，请充值！")
            continue
        if shop_car.get(good_name):
            shop_car[good_name] += 1
        else:
            shop_car[good_name] = 1


# 查看购物车
@comment.check_login
def check_shop_car():
    shop_car = shop.get_shop_car(user_info["user"])
    if not shop_car:
        print("购物车为空！")
        return
    print(shop_car)


def logout():
    pass


def admin_login():
    while True:
        input_name = input("请输入管理员账户名：").strip()
        flag = admin.check(input_name)
        if not flag:
            print("管理员不存在！请重新输入！")
            continue
        input_pwd = input("请输入密码：").strip()
        res = admin.login(input_name, input_pwd)
        if not res:
            print("密码不正确，请重新输入！")
            continue
        admin_info["user"] = input_name
        print("登陆成功！")
        return


@comment.check_admin_login
def lock_user():
    while True:
        username = input("请输入要冻结的账户名：")
        flag = user.check_username(username)
        if not flag:
            print("用户不存在，请重新输入！")
            continue
        admin.lock_inter(username)
        print("冻结成功！")
        return


@comment.check_admin_login
def unlock_user():
    while True:
        username = input("请输入要解冻的账户名：")
        flag = user.check_username(username)
        if not flag:
            print("用户不存在，请重新输入！")
            continue
        admin.unlock_inter(username)
        print("解冻成功！")
        return


@comment.check_admin_login
def change_limit():
    while True:
        username = input("请输入要修改额度的账户名：")
        flag = user.check_username(username)
        if not flag:
            print("用户不存在，请重新输入！")
            continue
        balance = input("请输入你要修改的金额：")
        if not balance.isdigit():
            print("请输入数字！")
            continue
        admin.chang_inter(username, balance)
        print("修改成功！")
        return


admin_func_dict = {
    "1": lock_user,
    "2": unlock_user,
    "3": change_limit,
}


# 管理员功能
def admin_sys():
    admin_func_list = (
        """
        1.冻结账户
        2.解冻账户
        3.修改额度
        4.退出
        """
    )
    while True:
        print(admin_func_list)
        choose_num = input("请输入对应功能的序号：")
        if choose_num in admin_func_dict:
            admin_func_dict[choose_num]()
            continue
        if choose_num == "4":
            admin_info["user"] = ""
            break
        print("请输入有效序号！")


fun_dict = {
    "1": register,
    "2": login,
    "3": check_bal,
    "4": withdraw,
    "5": repay,
    "6": transfer,
    "7": check_flow,
    "8": shopping,
    "9": check_shop_car,
    "10": logout,
    "11": admin_sys,
}


def run():
    while True:
        print('''
                1.注册
                2.登陆
                3.查看余额
                4.提现
                5.还款
                6.转账
                7.查看流水
                8.购物车功能
                9.查看购物车
                10.注销
                11.管理员功能
                12.退出
                ''')
        choose = input("请输入对应功能的序号：")
        if choose in fun_dict:
            fun_dict[choose]()
            continue
        if choose == "12":
            break
        print("请输入有效序号！")
