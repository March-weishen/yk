"""
1.注册
2.登陆
3.上传视频
4.删除视频
5.发布公告
"""
import os
from lib import comment
from conf import settings

UPLOAD_MOVIES = settings.UPLOAD_MOVIES

user_dic = {
    "session": None
}


def r_movie(c, movie_path, movie_size):
    a = 0
    with open(movie_path, "rb") as f:
        while a < movie_size:
            data = f.read(1024 * 10)
            c.send(data)
            a += 1024 * 10


def register(c):
    name = input("请输入用户名：").strip()
    pwd = input("请输入密码：").strip()
    re_pwd = input("请确认密码：")
    if pwd == re_pwd:
        dic = {"type": "register", "name": name, "pwd": pwd, "user_type": "admin"}
        comment.client_send(c, dic)
        dic_back = comment.client_recv(c)
        print(dic_back.get("msg"))
    else:
        print("两次密码输入不一致！")


def login(c):
    name = input("请输入用户名：").strip()
    pwd = input("请输入密码：").strip()
    dic = {"type": "login", "name": name, "pwd": pwd, "user_type": "admin"}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if dic_back.get("flag"):
        print(dic_back.get("msg"))
        user_dic["session"] = dic_back.get("session")
    else:
        print(dic_back.get("msg"))


def upload_movie(c):
    dic = {"type": "upload_movie", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    movies_list = comment.get_movies_list()
    if not movies_list:
        print("暂无可以上传的电影！")
        return
    comment.show_list(movies_list)
    choose = input("请选择你要上传的电影的序号：")
    movie_name = movies_list[int(choose) - 1]
    movie_path = os.path.join(UPLOAD_MOVIES, movie_name)
    movie_size = os.path.getsize(movie_path)
    movie_md5 = comment.get_movie_md5(movie_path)
    choose1 = input("是否收费(y/n):").strip()
    is_free = 1 if choose1 == "n" else 0
    dic1 = {"movie_name": movie_name, "movie_size": movie_size, "movie_md5": movie_md5, "is_free":is_free}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    print(dic_back1.get("msg"))
    r_movie(c,movie_path,movie_size)
    dic_back2 = comment.client_recv(c)
    print(dic_back2.get("msg"))

def delete_movie(c):
    dic = {"type": "delete_movie", "session": user_dic.get("session")}
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
    choose = input("请选择你要删除的电影的序号：")
    movie_name = movies_list[int(choose)-1].split("    ")[0]
    dic1 = {"movie_name":movie_name}
    comment.client_send(c,dic1)
    dic_back2 = comment.client_recv(c)
    print(dic_back2.get("msg"))


def release_notice(c):
    dic = {"type": "release_notice", "session": user_dic.get("session")}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    title = input("请输入公告标题：")
    content = input("请输入公告内容：")
    dic1 = {"title":title,"content":content}
    comment.client_send(c,dic1)
    dic_back = comment.client_recv(c)
    print(dic_back.get("msg"))


def logout():
    user_dic["session"] = None


func_dict = {
    "1": register,
    "2": login,
    "3": upload_movie,
    "4": delete_movie,
    "5": release_notice,
    "7": logout,
}


def admin_view(c):
    while True:
        choose = input("""
            1.注册
            2.登陆
            3.上传视频
            4.删除视频
            5.发布公告
            6.退出
            7.注销
        """)
        if choose == "6":
            break
        if choose in func_dict:
            func_dict.get(choose)(c)
        else:
            print("请输入合理的数字！")
