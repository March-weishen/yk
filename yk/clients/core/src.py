from core import admin, user

func_dict = {
    "1": admin.admin_view,
    "2": user.user_view
}


def run(c):
    while True:
        choose = input(
            """
            选择相应功能的序号：
            1.管理员
            2.普通用户
            3.退出
            """
        ).strip()
        if choose == "3":
            break
        if choose in func_dict:
            func_dict.get(choose)(c)
        else:
            print("请输入合理的序号！")
