import struct
import json
from hashlib import md5
from core import models
from conf import settings
import os

BASE_DOWNLOAD_DIR = settings.BASE_DOWNLOAD_DIR
s = settings.alive_user


def service_send(conn, dic):
    bytes_json = json.dumps(dic).encode("utf-8")
    conn.send(struct.pack("i", len(bytes_json)))
    conn.send(bytes_json)


def service_recv(conn):
    dict_len = struct.unpack("i", conn.recv(4))[0]
    dic = json.loads(conn.recv(dict_len).decode("utf-8"))
    return dic


def get_md5(con):
    md = md5()
    md.update(con.encode("utf-8"))
    return md.hexdigest()


def check_name(name):
    object_user = models.User.select(name=name)
    if object_user:
        return True


def check_login(name, pwd):
    object_user = models.User.select(name=name)
    if object_user:
        if object_user[0].password == pwd:
            return object_user[0]
    return False


def check_movie(movie_md5):
    object_movie = models.Movie.select(file_md5=movie_md5)
    if object_movie:
        if object_movie[0].is_delete:
            return 2
        return True


def check_session(dic, conn):
    addr = dic.get("addr")
    session = s.get(addr)[0]
    user_id = s.get(addr)[1]
    if dic.get("session") != session or dic.get("user_id") != user_id:
        dic_back1 = {"flag": 2, "msg": "请先登陆！"}
        service_send(conn, dic_back1)
        return True


def get_movies_list(flag=None):
    movies_list = []
    movies_obj = models.Movie.select()
    if movies_obj:
        for i in movies_obj:
            if i.is_delete:
                continue

            if not flag:
                free = "免费" if i.is_free else "收费"
                movie_obj = "%s    %s" % (i.name, free)
                movies_list.append(movie_obj)

            if flag == 1:
                if i.is_free:
                    movie_obj = "%s    %s" % (i.name, "免费")
                    movies_list.append(movie_obj)

            if flag == 2:
                if not i.is_free:
                    movie_obj = "%s    %s" % (i.name, "收费")
                    movies_list.append(movie_obj)
        return movies_list
    return False


def check_user_id(user_id):
    user_obj = models.User.select(id=user_id)
    if user_obj:
        return user_obj[0]
    return False


def check_download_record(user_id):
    record_list = []
    record_obj = models.DownloadRecord.select(user_id=user_id)
    if record_obj:
        for i in record_obj:
            movie_id = i.movie_id
            download_time = i.download_time
            movie_obj = models.Movie.select(id=movie_id)[0]
            movie_name = movie_obj.name
            record = "%s    %s" % (movie_name, download_time)
            record_list.append(record)
        return record_list
    return False


def check_notice(flag=None):
    notice_list = []
    notice_obj = models.Notice.select()
    if notice_obj:
        if not flag:
            for i in notice_obj:
                title = i.title
                content = i.content
                time = i.create_time
                notice = "%s    %s    %s" % (title, content, time)
                notice_list.append(notice)
        if flag == 1:
            notice_obj = sorted(notice_obj, key=lambda object: object.get("create_time"), reverse=True)
            i = notice_obj[0]
            title = i.title
            content = i.content
            time = i.create_time
            notice = "%s    %s    %s" % (title, content, time)
            notice_list.append(notice)
        return notice_list
    return False
