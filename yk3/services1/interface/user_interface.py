import os
from core import models
from lib import comment
from conf import settings

UPLOAD_MOVIES = settings.UPLOAD_MOVIES


def r_movie(conn, movie_path, movie_size):
    a = 0
    with open(movie_path, "rb") as f:
        while a < movie_size:
            data = f.read(1024 * 10)
            conn.send(data)
            a += 1024 * 10


@comment.check_login
def buy_vip(conn, dic):
    dic1 = comment.service_recv(conn)
    if dic1.get("flag"):
        user_id = dic.get("user_id")
        user_obj = models.User.select(id=user_id)[0]
        if user_obj.is_vip == 1:
            dic_back = {"flag": 2, "msg": "已经是会员，无需充值！"}
        else:
            user_obj.is_vip = 1
            user_obj.my_update()
            dic_back = {"flag": 1, "msg": "充值成功！"}
    else:
        dic_back = {"flag": 0, "msg": "充值失败！"}
    comment.service_send(conn, dic_back)


@comment.check_login
def select_movie(conn, dic):
    movies_list = comment.get_movies_list()
    if movies_list:
        dic1 = {"flag": 1, "movies_list": movies_list}
        comment.service_send(conn, dic1)
    else:
        dic1 = {"flag": 0, "msg": "暂无可以查看的电影！"}
        comment.service_send(conn, dic1)
        return


@comment.check_login
def download_free_movie(conn, dic):
    movies_list = comment.get_movies_list(flag=1)
    if movies_list:
        dic1 = {"flag": 1, "movies_list": movies_list}
        comment.service_send(conn, dic1)
    else:
        dic1 = {"flag": 0, "msg": "暂无可以下载的电影！"}
        comment.service_send(conn, dic1)
        return
    dic_back = comment.service_recv(conn)
    movie_name = dic_back.get("movie_name")
    movie_path = os.path.join(UPLOAD_MOVIES, movie_name)
    movie_size = os.path.getsize(movie_path)
    dic3 = {"movie_size": movie_size}
    comment.service_send(conn, dic3)
    r_movie(conn, movie_path, movie_size)
    user_id = dic.get("user_id")
    movie_id = models.Movie.select(name=movie_name)[0].id
    record = models.DownloadRecord(user_id=user_id, movie_id=movie_id, download_time=comment.get_time())
    record.save()
    dic2 = {"msg": "下载成功！"}
    comment.service_send(conn, dic2)


@comment.check_login
def download_charge_movie(conn, dic):
    movies_list = comment.get_movies_list(flag=2)
    if movies_list:
        dic1 = {"flag": 1, "movies_list": movies_list}
        comment.service_send(conn, dic1)
    else:
        dic1 = {"flag": 0, "msg": "暂无可以下载的电影！"}
        comment.service_send(conn, dic1)
        return
    dic_back = comment.service_recv(conn)
    movie_name = dic_back.get("movie_name")
    movie_path = os.path.join(UPLOAD_MOVIES, movie_name)
    movie_size = os.path.getsize(movie_path)
    dic3 = {"movie_size": movie_size}
    comment.service_send(conn, dic3)
    r_movie(conn, movie_path, movie_size)
    user_id = dic.get("user_id")
    movie_id = models.Movie.select(name=movie_name)[0].id
    record = models.DownloadRecord(user_id=user_id, movie_id=movie_id, download_time=comment.get_time())
    record.save()
    dic2 = {"msg": "下载成功！"}
    comment.service_send(conn, dic2)


@comment.check_login
def check_download_movie(conn, dic):
    movie_list = []
    user_id = dic.get("user_id")
    records_obj = models.DownloadRecord.select(user_id=user_id)
    if records_obj:
        for i in records_obj:
            movie_id = i.movie_id
            movie_name = models.Movie.select(id=movie_id)[0].name
            time = i.download_time
            movie = "%s    %s" % (movie_name, time)
            movie_list.append(movie)
        dic1 = {"flag": 1, "movie_list": movie_list}
    else:
        dic1 = {"flag": 0, "msg": "暂无下载记录！"}
    comment.service_send(conn, dic1)


@comment.check_login
def check_notice(conn, dic):
    notice_list = []
    notices_obj = models.Notice.select()
    if notices_obj:
        for i in notices_obj:
            title = i.title
            content = i.content
            time = i.create_time
            notice = "%s    %s    %s" % (title, content, time)
            notice_list.append(notice)
        dic1 = {"flag": 1, "notice_list": notice_list}
    else:
        dic1 = {"flag": 0, "msg": "暂无公告！"}
    comment.service_send(conn, dic1)
