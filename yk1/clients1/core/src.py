from core import admin, user

func_dic = {
    "1": admin.admin_view,
    "2": user.user_view
}


def run(c):
    while True:
        choose = input("""
            1.管理员
            2.普通用户
            3.退出
        """)
        if choose == "3":
            break
        if choose in func_dic:
            func_dic.get(choose)(c)
        else:
            print("请输入合理数字！")
