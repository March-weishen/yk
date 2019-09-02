from core import admin,user

func_dic = {
    "1":admin.admin_view,
    "2":user.user_view,
}


def run(c):
    while True:
        choose = input("""
            请输入你的选择：
            1.管理员
            2.普通用户
            3.退出
        """).strip()
        if choose == "3":
            break
        if choose in func_dic:
            func_dic.get(choose)(c)
