"""
1.注册
2.登陆
3.上传视频
4.删除视频
5.发布公告
"""
from lib import comment
import os
from conf import settings

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR

user_dict = {
    "session": None,
    "user_id": None
}


def register(c):
    while True:
        name = input("请输入需要注册的用户名：")
        pwd = input("请输入密码：")
        re_pwd = input("请确认密码：")
        if pwd == re_pwd:
            md_pwd = comment.get_md5(pwd)
            dic = {"type": "register", "name": name, "pwd": md_pwd, "user_type": "admin"}
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
            break
        else:
            print(dic_back.get("msg"))


@comment.check_login
def upload_movie(c):
    while True:
        movies_list = comment.get_movies_list()
        comment.show_list(movies_list)
        choose = input("请输入需要上传的电影的序号：")
        movie_path = os.path.join(BASE_UPLOAD_DIR, movies_list[int(choose) - 1])
        movie_md5 = comment.get_movie_md5(movie_path)
        dic1 = {"type": "check_movie", "movie_md5": movie_md5, "session": user_dict.get("session"),
                "user_id": user_dict.get("user_id")}
        comment.client_send(c, dic1)
        dic_back1 = comment.client_recv(c)
        if dic_back1.get("flag") == 2:
            print(dic_back1.get("msg"))
            return
        if dic_back1.get("flag"):
            print(dic_back1.get("msg"))
            break
        else:
            print(dic_back1.get("msg"))
        choose1 = input("是否设置为收费电影(y/n)？").strip().lower()
        is_free = 0 if choose1 == "y" else 1
        dic = {"type": "upload_movie", "name": movies_list[int(choose) - 1],
               "is_free": is_free, "session": user_dict.get("session"),
               "user_id": user_dict.get("user_id"), "file_md5": movie_md5}
        comment.send_movie(c, dic, movie_path)
        dic_back2 = comment.client_recv(c)
        print(dic_back2.get("msg"))
        break


@comment.check_login
def delete_movie(c):
    dic = {"type": "delete_movie", "session": user_dict.get("session"),
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
    choose = input("请选择需要删除的电影的序号：")
    movie_str = movies_list[int(choose) - 1]
    movie_name = movie_str.split("    ")[0]
    dic1 = {"movie_name": movie_name}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    print(dic_back1.get("msg"))


@comment.check_login
def release_notice(c):
    dic = {"type": "release_notice", "session": user_dict.get("session"),
           "user_id": user_dict.get("user_id")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag") == 2:
        print(dic_back.get("msg"))
        return
    title = input("请输入公告的标题：")
    content = input("请输入公告的内容：")
    dic1 = {"title": title, "content": content}
    comment.client_send(c, dic1)
    dic_back = comment.client_recv(c)
    print(dic_back.get("msg"))


func_dict = {
    "1": register,
    "2": login,
    "3": upload_movie,
    "4": delete_movie,
    "5": release_notice,
}


def admin_view(c):
    while True:
        choose = input(
            """
            请输入相应功能的序号：
            1.注册
            2.登陆
            3.上传电影
            4.删除电影
            5.添加公告
            6.退出
            7.注销
            """).strip()
        if choose == "6":
            break
        if choose == "7":
            user_dict["session"] = None
            user_dict["user_id"] = None
            break
        if choose in func_dict:
            func_dict.get(choose)(c)
        else:
            print("请输入合理的数字！")
