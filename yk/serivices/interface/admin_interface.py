"""
1.注册
2.登陆
3.上传视频
4.删除视频
5.发布公告
"""
from lib import comment
from conf import settings
import os
from core import models
import time

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR


def check_movie(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    flag = comment.check_movie(dic.get("movie_md5"))
    if flag == 2:
        dic_back = {"flag": 2, "msg": "电影已存在,上传成功！"}
        comment.service_send(conn, dic_back)
        return
    if flag:
        dic_back = {"flag": 1, "msg": "电影已存在！"}
    else:
        dic_back = {"flag": 0, "msg": "请上传！"}
    comment.service_send(conn, dic_back)


def upload_movie(dic, conn):
    file_size = dic.get("file_size")
    movie_name = dic.get("name")
    movie_path = os.path.join(BASE_UPLOAD_DIR, movie_name)
    with open(movie_path, "wb") as f:
        while file_size > 0:
            con = conn.recv(1024 * 10)
            f.write(con)
            file_size -= 1024 * 10
            if file_size < 1024 * 10:
                con = conn.recv(file_size)
                f.write(con)
                break
    m = models.Movie(name=movie_name, path=movie_path, is_free=dic.get("is_free"),
                     is_delete=0, file_md5=dic.get("file_md5"), upload_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                     user_id=dic.get("user_id"))
    m.save()
    dic2 = {"msg": "上传成功！"}
    comment.service_send(conn, dic2)


def delete_movie(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    movies_list = comment.get_movies_list()
    if movies_list:
        dic_back = {"flag": 1, "movies_list": movies_list}
        comment.service_send(conn, dic_back)
    else:
        dic_back = {"flag": 0, "msg": "暂无可以删除的电影"}
        comment.service_send(conn, dic_back)
        return
    dic1 = comment.service_recv(conn)
    movie_name = dic1.get("movie_name")
    movie_obj = models.Movie.select(name=movie_name)
    if movie_obj:
        movie_obj[0].is_delete = 1
        movie_obj[0].mysql_update()
        dic_back1 = {"msg": "删除成功!"}
    else:
        dic_back1 = {"msg": "删除失败！"}
    comment.service_send(conn, dic_back1)


def release_notice(dic, conn):
    res = comment.check_session(dic, conn)
    if res:
        return
    dic_back = {"msg": "请添加公告！"}
    comment.service_send(conn, dic_back)
    dic1 = comment.service_recv(conn)
    title = dic1.get("title")
    content = dic1.get("content")
    user_id = dic.get("user_id")
    notice_obj = models.Notice(title=title, content=content, create_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                               user_id=user_id)
    notice_obj.save()
    dic_back1 = {"msg": "添加成功！"}
    comment.service_send(conn, dic_back1)
