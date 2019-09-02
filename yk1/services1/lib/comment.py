import os
import json
import struct
from core import models
from hashlib import md5
from functools import wraps
from conf import settings

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR
alive_user = settings.alive_user

def service_send(conn,dic):
    json_dic = json.dumps(dic).encode("utf-8")
    str_dic = struct.pack("i",len(json_dic))
    conn.send(str_dic)
    conn.send(json_dic)


def service_recv(conn):
    len_dic = struct.unpack("i",conn.recv(4))[0]
    dic = json.loads(conn.recv(len_dic).decode("utf-8"))
    return dic


def check_user(name):
    user_obj = models.User.select(name=name)
    if user_obj:
        user = user_obj[0]
        return user
    return False


def get_md5(con):
    md = md5()
    md.update(con.encode("utf-8"))
    return md.hexdigest()


def check_login(func):
    @wraps(func)
    def inner(*args,**kwargs):
        dic = args[1]
        conn = args[0]
        if dic.get("session"):
            addr = dic.get("addr")
            session = alive_user.get(addr)[0]
            user_id = alive_user.get(addr)[1]
            if session == dic.get("session"):
                args[1]["user_id"] = user_id
                dic1 = {"flag": 1}
                service_send(conn, dic1)
                func(*args,**kwargs)
        else:
            dic1 = {"flag":0,"msg":"请先登陆！"}
            service_send(conn,dic1)
    return inner


def check_movie_name(movie_name,movie_md5):
    movie_obj = models.Movie.select(name=movie_name)
    if movie_obj:
        movie = movie_obj[0]
        if movie.file_md5 == movie_md5:
            return True
    return False


def get_movies_list(flag=None):
    movie_list = []
    movies_obj = models.Movie.select()
    if movies_obj:
        for movie_obj in movies_obj:
            if movie_obj.is_delete:
                continue
            movie_name = movie_obj.name
            is_free = movie_obj.is_free
            if not flag:
                free = "免费" if is_free else "收费"
                movie = "%s    %s"%(movie_name,free)
                movie_list.append(movie)
            if flag == 1:
                if is_free:
                    movie = "%s    %s" % (movie_name, "免费")
                    movie_list.append(movie)
            if flag == 2:
                if not is_free:
                    movie = "%s    %s" % (movie_name, "收费")
                    movie_list.append(movie)
        return movie_list
    return False


def get_record(dic):
    record_list = []
    user_id = dic.get("user_id")
    records_obj = models.DownloadRecord.select(user_id=user_id)
    if records_obj:
        for record_obj in records_obj:
            movie_id = record_obj.movie_id
            movie_obj = models.Movie.select(id=movie_id)[0]
            movie_name = movie_obj.name
            is_free = movie_obj.is_free
            free = "免费" if is_free else "收费"
            data = record_obj.download_time
            record = "%s    %s    %s"%(movie_name,free,data)
            record_list.append(record)
        return record_list
    return False

def get_notice():
    notice_list = []
    notices_obj = models.Notice.select()
    if notices_obj:
        for notice_obj in notices_obj:
            title = notice_obj.title
            content = notice_obj.content
            create_time = notice_obj.create_time
            notice = "%s    %s    %s"%(title,content,create_time)
            notice_list.append(notice)
        return notice_list
    return False

def new_notice():
    notices_obj = models.Notice.select()
    if notices_obj:
        new_notices_obj = sorted(notices_obj,key=lambda obj:obj.create_time,reverse=True)
        notice_obj = new_notices_obj[0]
        title = notice_obj.title
        content = notice_obj.content
        create_time = notice_obj.create_time
        notice = "%s    %s    %s"%(title,content,create_time)
        return notice
    return False

