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
from lib import comment
from conf import settings
import os

BASE_DOWNLOAD_DIR = settings.BASE_DOWNLOAD_DIR
user_dict = {
    "session": None,
    "user_id": None,
    "is_vip": None
}


def register(c):
    while True:
        name = input("请输入需要注册的用户名：")
        pwd = input("请输入密码：")
        re_pwd = input("请确认密码：")
        if pwd == re_pwd:
            md_pwd = comment.get_md5(pwd)
            dic = {"type": "register", "name": name, "pwd": md_pwd, "user_type": "user"}
            comment.client_send(c, dic)
            dic_back = comment.client_recv(c)
            if dic_back.get("flag"):
                print(dic_back.get("msg"))
                break
            else:
                print(dic_back.get("msg"))


def login(c):
    while True:
        name = input("请输入用户名：").strip()
        pwd = input("请输入密码：").strip()
        md_pwd = comment.get_md5(pwd)
        dic = {"type": "login", "name": name, "pwd": md_pwd}
        comment.client_send(c, dic)
        dic_back = comment.client_recv(c)
        if dic_back.get("flag"):
            print(dic_back.get("msg"))
            user_dict["session"] = dic_back.get("session")
            user_dict["user_id"] = dic_back.get("user_id")
            user_dict["is_vip"] = dic_back.get("is_vip")
            print(dic_back.get("notice")[0])
            break
        else:
            print(dic_back.get("msg"))


@comment.check_login1
def buy_vip(c):
    dic = {"type": "buy_vip", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    choose = input("请确认会员充值(y/n):").strip().lower()
    if choose == "y":
        dic1 = {"flag": 1}
    else:
        dic1 = {"flag": 0}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    print(dic_back1.get("msg"))


@comment.check_login1
def select_movie(c):
    dic = {"type": "select_movie", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if dic_back1.get("flag"):
        movies_list = dic_back1.get("msg")
        comment.show_list(movies_list)
    else:
        print(dic_back1.get("msg"))


@comment.check_login1
def download_free_movie(c):
    dic = {"type": "download_free_movie", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    if dic_back.get("flag"):
        movies_list = dic_back.get("movies_list")
        comment.show_list(movies_list)
    else:
        print(dic_back.get("msg"))
        return
    choose = input("请选择需要下载的免费电影的序号：")
    movie_str = movies_list[int(choose) - 1]
    movie_name = movie_str.split("    ")[0]
    dic1 = {"movie_name": movie_name}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    print(dic_back1)
    movie_size = dic_back1.get("movie_size")
    movie_path = os.path.join(BASE_DOWNLOAD_DIR, movie_name)
    a = 0
    with open(movie_path, "wb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                c.recv(movie_size - a)
            else:
                data = c.recv(1024 * 10)
            f.write(data)
            a += 1024 * 10
            comment.progress(a, movie_size)
    dic_back2 = comment.client_recv(c)
    print(dic_back2.get("msg"))


@comment.check_login1
def download_charge_movie(c):
    dic = {"type": "download_charge_movie", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    if dic_back.get("flag"):
        movies_list = dic_back.get("movies_list")
        comment.show_list(movies_list)
    else:
        print(dic_back.get("msg"))
        return
    choose = input("请选择需要下载的免费电影的序号：")
    movie_str = movies_list[int(choose) - 1]
    movie_name = movie_str.split("    ")[0]
    dic1 = {"movie_name": movie_name}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    print(dic_back1)
    movie_size = dic_back1.get("movie_size")
    movie_path = os.path.join(BASE_DOWNLOAD_DIR, movie_name)
    a = 0
    with open(movie_path, "wb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                c.recv(movie_size - a)
            else:
                data = c.recv(1024 * 10)
            f.write(data)
            a += 1024 * 10
            comment.progress(a, movie_size)
    dic_back2 = comment.client_recv(c)
    print(dic_back2.get("msg"))


@comment.check_login1
def check_download_movie(c):
    dic = {"type": "check_download_movie", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    dic_back1 = comment.client_recv(c)
    if dic_back1.get("flag"):
        record = dic_back1.get("record")
        comment.show_list(record)
    else:
        print(dic_back1.get("msg"))


@comment.check_login1
def check_notice(c):
    dic = {"type": "check_notice", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    dic_back = comment.client_recv(c)
    if dic_back.get("flag"):
        notice_list = dic_back.get("notice_list")
        comment.show_list(notice_list)
    else:
        print(dic_back.get("msg"))


func_dict = {
    "1": register,
    "2": login,
    "3": buy_vip,
    "4": select_movie,
    "5": download_free_movie,
    "6": download_charge_movie,
    "7": check_download_movie,
    "8": check_notice
}


def user_view(c):
    while True:
        choose = input("""
        请输入相应功能的序号:
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
        """).strip()
        if choose == "9":
            break
        if choose == "10":
            user_dict["session"] = None
            user_dict["user_id"] = None
            break
        if choose in func_dict:
            func_dict.get(choose)(c)
        else:
            print("请输入合理的数字！")
