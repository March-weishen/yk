import os
from lib import comment
from conf import settings
from core import models

UPLOAD_MOVIES = settings.UPLOAD_MOVIES


def w_movie(conn, movie_path, movie_size):
    a = 0
    with open(movie_path, "wb") as f:
        while a < movie_size:
            data = conn.recv(1024 * 10)
            f.write(data)
            a += 1024 * 10


@comment.check_login
def upload_movie(conn, dic):
    dic1 = comment.service_recv(conn)
    movie_name = dic1.get("movie_name")
    movie_md5 = dic1.get("movie_md5")
    flag = comment.check_movie(movie_name, movie_md5)
    if flag:
        dic_back = {"flag": 0, "msg": "电影已经存在！"}
    else:
        dic_back = {"flag": 1, "msg": "上传准备就绪！"}
    comment.service_send(conn, dic_back)
    movie_size = dic1.get("movie_size")
    movie_path = os.path.join(UPLOAD_MOVIES, movie_name)
    w_movie(conn, movie_path, movie_size)
    dic2 = {"msg": "上传成功！"}
    user_id = dic.get("user_id")
    is_free = dic1.get("is_free")
    movie_obj = models.Movie(name=movie_name, path=movie_path, is_free=is_free, is_delete=0, file_md5=movie_md5,
                             upload_time=comment.get_time(), user_id=user_id)
    movie_obj.save()
    comment.service_send(conn, dic2)


@comment.check_login
def delete_movie(conn, dic):
    movies_list = comment.get_movies_list()
    if not movies_list:
        dic_back = {"flag":0,"msg":"暂无可以删除的电影！"}
        comment.service_send(conn,dic_back)
        return
    dic_back = {"flag": 1, "movies_list":movies_list}
    comment.service_send(conn,dic_back)
    dic1 = comment.service_recv(conn)
    movie_name = dic1.get("movie_name")
    movie_obj = models.Movie.select(name=movie_name)[0]
    movie_obj.is_delete = 1
    movie_obj.my_update()
    dic_back1 = {"msg":"删除成功！"}
    comment.service_send(conn,dic_back1)



@comment.check_login
def release_notice(conn, dic):
    dic_back = comment.service_recv(conn)
    title = dic_back.get("title")
    content = dic_back.get("content")
    user_id = dic.get("user_id")
    notice_obj = models.Notice(title=title,content=content,create_time=comment.get_time(),user_id=user_id)
    notice_obj.save()
    dic1 = {"msg":"发布成功！"}
    comment.service_send(conn,dic1)
