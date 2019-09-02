import struct
import json
from hashlib import md5
import os
from conf import settings
from functools import wraps

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR


def client_send(c, dic):
    bytes_json = json.dumps(dic).encode("utf-8")
    c.send(struct.pack("i", len(bytes_json)))
    c.send(bytes_json)


def client_recv(c):
    dict_len = struct.unpack("i", c.recv(4))[0]
    dic = json.loads(c.recv(dict_len).decode("utf-8"))
    return dic


def get_md5(con):
    md = md5()
    md.update(con.encode("utf-8"))
    return md.hexdigest()


def get_movies_list():
    movies_list = os.listdir(BASE_UPLOAD_DIR)
    if movies_list:
        return movies_list
    return False


def show_list(lis):
    for i, j in enumerate(lis, 1):
        print(i, j, sep="    ")


def get_movie_md5(path):
    md1 = md5()
    with open(path, "rb") as f:
        for i in f:
            md1.update(i)
    return md1.hexdigest()


def send_movie(c, dic, path):
    file_size = os.path.getsize(path)
    dic["file_size"] = file_size
    b = file_size
    client_send(c, dic)
    a = 0
    with open(path, "rb") as f:
        while file_size > 0:
            con = f.read(1024 * 10)
            c.send(con)
            file_size -= 1024 * 10
            a += 1024 * 10
            if file_size < 1024 * 10:
                con = f.read(file_size)
                c.send(con)
                a += file_size
                file_size = 0
            progress(a, b)


def check_login(func):
    @wraps(func)
    def inner(*args, **kwargs):
        from core import admin
        if not admin.user_dict["session"]:
            print("请先登陆！")
            admin.login(*args, **kwargs)
        res = func(*args, **kwargs)
        return res

    return inner


def check_login1(func):
    @wraps(func)
    def inner(*args, **kwargs):
        from core import user
        if not user.user_dict["session"]:
            print("请先登陆！")
            user.login(*args, **kwargs)
        res = func(*args, **kwargs)
        return res

    return inner


def progress(size, file_size):
    percent = size * 100 / file_size
    if percent >= 100:  # 如果百分比大于1的话则取1
        percent_r = 100
        print('\r%s%%%s' % (percent_r, "*" * 100))
        return
    percent_r = "%.3f" % percent
    print('\r%s%%%s' % (percent_r, "*" * int(percent)), end='', flush=True)
    # \r 代表调到行首的意思，\n为换行的意思，fiel代表输出到哪，flush=True代表无延迟，立马刷新。第二个%s是百分比
