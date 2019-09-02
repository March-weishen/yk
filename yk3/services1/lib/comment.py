import json
import struct
import time
import os
from hashlib import md5
from core import models
from conf import settings
from functools import wraps

alive_user = settings.alive_user
mutex = settings.mutex
UPLOAD_MOVIES = settings.UPLOAD_MOVIES


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def service_send(conn, dic):
    json_dic = json.dumps(dic).encode("utf-8")
    len_dic = struct.pack("i", len(json_dic))
    conn.send(len_dic)
    conn.send(json_dic)


def service_recv(conn):
    len_dic = struct.unpack("i", conn.recv(4))[0]
    dic = json.loads(conn.recv(len_dic).decode("utf-8"))
    return dic


def get_md5(con):
    md = md5()
    md.update(con.encode("utf-8"))
    return md.hexdigest()


def check_user_name(name):
    user_obj = models.User.select(name=name)
    if user_obj:
        return user_obj[0]
    return False


def check_login(func):
    @wraps(func)
    def inner(*args, **kwargs):
        conn = args[0]
        dic = args[1]
        if dic.get("session"):
            addr = dic.get("addr")
            session = alive_user.get(addr)[0]
            user_id = alive_user.get(addr)[1]
            if session == dic.get("session"):
                args[1]["user_id"] = user_id
                dic1 = {"flag": 1}
                service_send(conn, dic1)
                func(*args, **kwargs)
            else:
                dic1 = {"flag": 0, "msg": "请先登陆！"}
                service_send(conn, dic1)
        else:
            dic1 = {"flag": 0, "msg": "请先登陆！"}
            service_send(conn, dic1)

    return inner


def check_movie(movie_name, movie_md5):
    md = md5()
    movie_path = os.path.join(UPLOAD_MOVIES, movie_name)
    if not os.path.isfile(movie_path):
        return False
    with open(movie_path, "rb") as f:
        for i in f:
            md.update(i)
    if movie_md5 == md.hexdigest():
        return True
    return False


def get_movies_list(flag=None):
    movies_list = []
    movies_obj = models.Movie.select()
    if movies_obj:
        for i in movies_obj:
            if i.is_delete:
                continue
            movie_name = i.name
            if not flag:
                free = "免费" if i.is_free == 1 else "收费"
                movie = "%s    %s" % (movie_name, free)
                movies_list.append(movie)
            if flag == 1:
                free = "免费"
                movie = "%s    %s" % (movie_name, free)
                movies_list.append(movie)
            if flag == 2:
                free = "收费"
                movie = "%s    %s" % (movie_name, free)
                movies_list.append(movie)
        return movies_list
    return False


def select_first_notice():
    notices_obj = models.Notice.select()
    if notices_obj:
        notices_obj = sorted(notices_obj, key=lambda obj: obj.create_time, reverse=True)
        notice_obj = notices_obj[0]
        title = notice_obj.title
        content = notice_obj.content
        time = notice_obj.create_time
        notice = "%s    %s    %s" % (title, content, time)
        return notice
    return False
