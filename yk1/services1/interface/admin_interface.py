import os
import time
from lib import comment
from conf import settings
from core import models

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR


def w_movie(conn, movie_path, movie_size):
    a = 0
    with open(movie_path, "wb") as f:
        while a < movie_size:
            if a + 1024 * 10 > movie_size:
                data = conn.recv(movie_size - a)
                f.write(data)
                return
            data = conn.recv(1024 * 10)
            a += 1024 * 10
            f.write(data)


@comment.check_login
def upload_movie(conn, dic):
    dic_back = comment.service_recv(conn)
    if not dic_back.get("flag", 1):
        return
    movie_name = dic_back.get("movie_name")
    movie_md5 = dic_back.get("movie_md5")
    flag = comment.check_movie_name(movie_name, movie_md5)
    if flag:
        dic2 = {"flag": 0, "msg": "电影已经存在！"}
        comment.service_send(conn, dic2)
        return
    dic2 = {"flag": 1, "msg": "开始上传！"}
    comment.service_send(conn, dic2)
    movie_size = dic_back.get("movie_size")
    movie_path = os.path.join(BASE_UPLOAD_DIR, movie_name)
    w_movie(conn, movie_path, movie_size)
    movie_obj = models.Movie(name=movie_name, path=movie_path, is_free=dic_back.get("is_free"),
                             is_delete=0, file_md5=movie_md5, upload_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                             user_id=dic.get("user_id"))
    movie_obj.save()
    dic3 = {"msg": "上传成功！"}
    comment.service_send(conn, dic3)


@comment.check_login
def delete_movie(conn, dic):
    movies_list = comment.get_movies_list()

    if not movies_list:
        dic2 = {"flag": 0, "msg": "暂无可以删除的电影！"}
        comment.service_send(conn, dic2)
        return
    dic2 = {"flag": 1, "movies_list": movies_list}
    comment.service_send(conn, dic2)
    dic_back = comment.service_recv(conn)
    movie_name = dic_back.get("movie_name")
    movie_obj = models.Movie.select(name=movie_name)[0]
    movie_obj.is_delete = 1
    movie_obj.my_update()
    dic3 = {"msg": "删除成功！"}
    comment.service_send(conn, dic3)


@comment.check_login
def release_notice(conn, dic):
    dic_back = comment.service_recv(conn)
    notice_title = dic_back.get("notice_title")
    notice_content = dic_back.get("notice_content")
    user_id = dic.get("user_id")
    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    notice_obj = models.Notice(title=notice_title, content=notice_content, user_id=user_id, create_time=create_time)
    notice_obj.save()
    dic2 = {"msg": "发布成功！"}
    comment.service_send(conn, dic2)
