"""
1 注册
2 登录
3 冲会员
4 查看视频
5 下载免费视频
6 下载收费视频
7 查看观影记录
8 查看公告
"""
import os
from lib import comment
from conf import settings

BASE_DOWNLOAD_DIR = settings.BASE_DOWNLOAD_DIR

user_dic = {
    "session": None
}


def w_movie(c, movie_path, movie_size):
    a = 0
    with open(movie_path, "wb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                data = c.recv(movie_size - a)
                f.write(data)
                return
            data = c.recv(1024 * 10)
            a += 1024 * 10
            f.write(data)


def register(c):
    name = input("请输入用户名：")
    pwd = input("请输入密码：")
    re_pwd = input("请输入密码：")
    if pwd == re_pwd:
        dic = {"type": "register", "name": name, "pwd": pwd, "user_type": "user"}
        comment.client_send(c, dic)
        dic_back = comment.client_recv(c)
        if not dic_back:
            print(dic_back.get("msg"))
            return
        print(dic_back.get("msg"))


def login(c):
    name = input("请输入用户名：")
    pwd = input("请输入密码：")
    dic = {"type": "login", "name": name, "pwd": pwd}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    flag = dic_back.get("flag")
    if flag == 2:
        print(dic_back.get("msg"))
        print(dic_back.get("notice"))
        user_dic["session"] = dic_back.get("session")
        return
    print(dic_back.get("msg"))


def buy_vip(c):
    dic = {"type": "buy_vip", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    choose = input("是否购买会员(y/n)：").strip().lower()
    if choose == "y":
        dic1 = {"flag": 1}
    else:
        dic1 = {"flag": 0}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    print(dic_back1.get("msg"))


def select_movie(c):
    dic = {"type": "select_movie", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    movies_list = dic_back1.get("movies_list")
    comment.show_list(movies_list)


def download_free_movie(c):
    dic = {"type": "download_free_movie", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    movies_list = dic_back1.get("movies_list")
    comment.show_list(movies_list)
    choose = input("请选择要下载的电影的序号：")
    movie = movies_list[int(choose) - 1]
    movie_name = movie.split("    ")[0]
    dic1 = {"movie_name": movie_name}
    comment.client_send(c, dic1)
    dic_back2 = comment.client_recv(c)
    movie_size = dic_back2.get("movie_size")
    movie_path = os.path.join(BASE_DOWNLOAD_DIR, movie_name)
    w_movie(c, movie_path, movie_size)
    dic_back3 = comment.client_recv(c)
    print(dic_back3.get("msg"))


def download_charge_movie(c):
    dic = {"type": "download_charge_movie", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    movies_list = dic_back1.get("movies_list")
    comment.show_list(movies_list)
    choose = input("请选择要下载的电影的序号：")
    movie = movies_list[int(choose) - 1]
    movie_name = movie.split("    ")[0]
    dic1 = {"movie_name": movie_name}
    comment.client_send(c, dic1)
    dic_back2 = comment.client_recv(c)
    movie_size = dic_back2.get("movie_size")
    movie_path = os.path.join(BASE_DOWNLOAD_DIR, movie_name)
    w_movie(c, movie_path, movie_size)
    dic_back3 = comment.client_recv(c)
    print(dic_back3.get("msg"))


def check_download_movie(c):
    dic = {"type": "check_download_movie", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    record_list = dic_back1.get("record")
    comment.show_list(record_list)


def check_notice(c):
    dic = {"type": "check_notice", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    notice_list = dic_back1.get("notices")
    comment.show_list(notice_list)


def logout():
    user_dic["session"] = None


func_dict = {
    "1": register,
    "2": login,
    "3": buy_vip,
    "4": select_movie,
    "5": download_free_movie,
    "6": download_charge_movie,
    "7": check_download_movie,
    "8": check_notice,
    "10": logout,
}


def user_view(c):
    while True:
        choose = input("""
            1 注册
            2 登录
            3 冲会员
            4 查看视频
            5 下载免费视频
            6 下载收费视频
            7 查看观影记录
            8 查看公告
            9 退出
            10 注销
        """)
        if choose == "9":
            break
        if choose in func_dict:
            func_dict.get(choose)(c)
        else:
            print("请输入合理的数字！")
