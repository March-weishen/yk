import os
import time
from lib import comment
from core import models
from conf import settings

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR


def r_movie(conn, movie_path, movie_size):
    a = 0
    with open(movie_path, "rb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                conn.send(f.read(movie_size - a))
            conn.send(f.read(1024 * 10))
            a += 1024 * 10


@comment.check_login
def buy_vip(conn, dic):
    dic_back = comment.service_recv(conn)
    if dic_back.get("flag"):
        user_id = dic.get("user_id")
        user_obj = models.User.select(id=user_id)[0]
        if user_obj.is_vip == 1:
            dic2 = {"msg": "您已经是会员了！"}
        else:
            user_obj.is_vip = 1
            user_obj.my_update()
            dic2 = {"msg": "充值成功！"}
    else:
        dic2 = {"msg": "充值失败！"}
    comment.service_send(conn, dic2)


@comment.check_login
def select_movie(conn, dic):
    movies_list = comment.get_movies_list()
    if not movies_list:
        dic2 = {"flag": 0, "msg": "暂无可以查看的电影"}
    else:
        dic2 = {"flag": 1, "movies_list": movies_list}
    comment.service_send(conn, dic2)


@comment.check_login
def download_free_movie(conn, dic):
    movies_list = comment.get_movies_list(flag=1)
    if not movies_list:
        dic2 = {"flag": 0, "msg": "暂无可以下载的电影"}
        comment.service_send(conn, dic2)
        return
    else:
        dic2 = {"flag": 1, "movies_list": movies_list}
    comment.service_send(conn, dic2)
    dic_back = comment.service_recv(conn)
    movie_name = dic_back.get("movie_name")
    movie_path = os.path.join(BASE_UPLOAD_DIR, movie_name)
    movie_size = os.path.getsize(movie_path)
    dic3 = {"movie_size": movie_size}
    comment.service_send(conn, dic3)
    r_movie(conn, movie_path, movie_size)
    user_id = dic.get("user_id")
    movie_id = models.Movie.select(name=movie_name)[0].id
    record = models.DownloadRecord(user_id=user_id, movie_id=movie_id, download_time=time.strftime("%Y-%m-%d %H:%M:%S"))
    record.save()
    dic4 = {"msg": "下载成功！"}
    comment.service_send(conn, dic4)


@comment.check_login
def download_charge_movie(conn, dic):
    movies_list = comment.get_movies_list(flag=2)
    if not movies_list:
        dic2 = {"flag": 0, "msg": "暂无可以下载的电影"}
        comment.service_send(conn, dic2)
        return
    else:
        dic2 = {"flag": 1, "movies_list": movies_list}
    comment.service_send(conn, dic2)
    dic_back = comment.service_recv(conn)
    movie_name = dic_back.get("movie_name")
    movie_path = os.path.join(BASE_UPLOAD_DIR, movie_name)
    movie_size = os.path.getsize(movie_path)
    dic3 = {"movie_size": movie_size}
    comment.service_send(conn, dic3)
    r_movie(conn, movie_path, movie_size)
    user_id = dic.get("user_id")
    movie_id = models.Movie.select(name=movie_name)[0].id
    record = models.DownloadRecord(user_id=user_id, movie_id=movie_id, download_time=time.strftime("%Y-%m-%d %H:%M:%S"))
    record.save()
    dic4 = {"msg": "下载成功！"}
    comment.service_send(conn, dic4)


@comment.check_login
def check_download_movie(conn, dic):
    record = comment.get_record(dic)
    if not record:
        dic1 = {"flag": 0, "msg": "暂无下载记录！"}
        comment.service_send(conn, dic1)
        return
    dic1 = {"flag": 1, "record": record}
    comment.service_send(conn, dic1)


@comment.check_login
def check_notice(conn, dic):
    notices = comment.get_notice()
    if not notices:
        dic1 = {"flag": 0, "msg": "暂无公告！"}
        comment.service_send(conn, dic1)
        return
    dic1 = {"flag": 1, "notices": notices}
    comment.service_send(conn, dic1)
