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
from core import models
import time


def buy_vip(dic, conn):
    print(dic)
    res = comment.check_session(dic, conn)
    if res:
        return
    dic2 = {"flag": "1"}
    comment.service_send(conn, dic2)
    dic1 = comment.service_recv(conn)
    if dic1.get("flag") == 1:
        user_obj = comment.check_user_id(dic.get("user_id"))
        if user_obj.is_vip == 1:
            dic_back = {"msg": "您已经是会员！"}
        else:
            user_obj.is_vip = 1
            user_obj.mysql_update()
            dic_back = {"msg": "充值成功！"}
    else:
        dic_back = {"msg": "充值失败！"}
    comment.service_send(conn, dic_back)


def select_movie(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    dic1 = {"flag": 1}
    comment.service_send(conn, dic1)
    movies_list = comment.get_movies_list()
    if not movies_list:
        dic2 = {"flag": 0, "msg": "暂无可以查看的电影！"}
    else:
        dic2 = {"flag": 1, "msg": movies_list}
    comment.service_send(conn, dic2)


def download_free_movie(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    movies_list = comment.get_movies_list(1)
    if movies_list:
        dic_back = {"flag": 1, "movies_list": movies_list}
        comment.service_send(conn, dic_back)
    else:
        dic_back = {"flag": 0, "msg": "暂无可以下载的电影！"}
        comment.service_send(conn, dic_back)
        return
    dic1 = comment.service_recv(conn)
    movie_name = dic1.get("movie_name")
    movie_obj = models.Movie.select(name=movie_name)[0]
    movie_path = movie_obj.path
    movie_size = os.path.getsize(movie_path)
    dic2 = {"movie_size": movie_size}
    comment.service_send(conn, dic2)
    a = 0
    with open(movie_path, "rb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                conn.send(f.read(movie_size - a))
            else:
                conn.send(f.read(1024 * 10))
            a += 1024 * 10
    dic3 = {"msg": "下载完成！"}
    comment.service_send(conn, dic3)
    download_record = models.DownloadRecord(user_id=dic.get("user_id"), movie_id=movie_obj.id,
                                            download_time=time.strftime("%Y-%m-%d %H:%M:%S"))
    download_record.save()


def download_charge_movie(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    movies_list = comment.get_movies_list(2)
    if movies_list:
        dic_back = {"flag": 1, "movies_list": movies_list}
        comment.service_send(conn, dic_back)
    else:
        dic_back = {"flag": 0, "msg": "暂无可以下载的电影！"}
        comment.service_send(conn, dic_back)
        return
    dic1 = comment.service_recv(conn)
    movie_name = dic1.get("movie_name")
    movie_obj = models.Movie.select(name=movie_name)[0]
    movie_path = movie_obj.path
    movie_size = os.path.getsize(movie_path)
    dic2 = {"movie_size": movie_size}
    comment.service_send(conn, dic2)
    a = 0
    with open(movie_path, "rb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                conn.send(f.read(movie_size - a))
            else:
                conn.send(f.read(1024 * 10))
            a += 1024 * 10
    dic3 = {"msg": "下载完成！"}
    comment.service_send(conn, dic3)
    download_record = models.DownloadRecord(user_id=dic.get("user_id"), movie_id=movie_obj.id,
                                            download_time=time.strftime("%Y-%m-%d %H:%M:%S"))
    download_record.save()


def check_download_movie(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    dic1 = {"flag": 1}
    comment.service_send(conn, dic1)
    record = comment.check_download_record(dic.get("user_id"))
    if record:
        dic2 = {"flag": 1, "record": record}
    else:
        dic2 = {"flag": 0, "msg": "暂无下载记录!"}
    comment.service_send(conn, dic2)


def check_notice(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    dic1 = {"flag": 1}
    comment.service_send(conn, dic1)
    notice_list = comment.check_notice()
    if notice_list:
        dic2 = {"flag": 1, "notice_list": notice_list}
    else:
        dic2 = {"flag": 0, "msg": "暂无公告！"}
    comment.service_send(conn, dic2)
