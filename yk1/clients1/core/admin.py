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

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR
user_dic = {
    "session": None
}


def r_movie(c, movie_path, movie_size):
    a = 0
    with open(movie_path, "rb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                c.send(f.read(movie_size - a))
            c.send(f.read(1024 * 10))
            a += 1024 * 10
            comment.progress(a, movie_size)


def register(c):
    name = input("请输入用户名：")
    pwd = input("请输入密码：")
    re_pwd = input("请输入密码：")
    if pwd == re_pwd:
        dic = {"type": "register", "name": name, "pwd": pwd, "user_type": "admin"}
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
        user_dic["session"] = dic_back.get("session")
        return
    print(dic_back.get("msg"))


def upload_movie(c):
    session = user_dic.get("session")
    dic = {"type": "upload_movie", "session": session}
    comment.client_send(c, dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    movies_list = comment.get_movies_list()
    if not movies_list:
        dic1 = {"flag": 0}
        comment.client_send(c, dic1)
        print("暂无可以上传的电影！")
        return
    comment.show_list(movies_list)
    choose = input("请选择上传电影的序号：")
    movie_name = movies_list[int(choose) - 1]
    movie_path = os.path.join(BASE_UPLOAD_DIR, movie_name)
    movie_md5 = comment.get_movie_md5(movie_path)
    movie_size = os.path.getsize(movie_path)
    choose1 = input("是否收费(y/n):").strip().lower()
    is_free = 1 if choose1 == "y" else 0
    dic1 = {"movie_name": movie_name, "movie_md5": movie_md5, "movie_size": movie_size, "is_free": is_free}
    comment.client_send(c, dic1)
    dic_back1 = comment.client_recv(c)
    if not dic_back1.get("flag"):
        print(dic_back1.get("msg"))
        return
    print(dic_back1.get("msg"))
    r_movie(c, movie_path, movie_size)
    dic_back2 = comment.client_recv(c)
    print(dic_back2.get("msg"))


def delete_movie(c):
    session = user_dic.get("session")
    dic = {"type":"delete_movie","session":session}
    comment.client_send(c,dic)
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
    choose = input("请选择要删除的电影的序号：")
    movie = movies_list[int(choose)-1]
    movie_name = movie.split("    ")[0]
    dic1 = {"movie_name":movie_name}
    comment.client_send(c,dic1)
    dic_back2 = comment.client_recv(c)
    print(dic_back2.get("msg"))


def release_notice(c):
    session = user_dic.get("session")
    dic = {"type":"release_notice","session":session}
    comment.client_send(c,dic)
    dic_back = comment.client_recv(c)
    if not dic_back.get("flag"):
        print(dic_back.get("msg"))
        return
    notice_title = input("请输入公告的标题：")
    notice_content = input("请输入公告的内容：")
    dic1 = {"notice_title":notice_title,"notice_content":notice_content}
    comment.client_send(c,dic1)
    dic_back1 = comment.client_recv(c)
    print(dic_back1.get("msg"))


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
