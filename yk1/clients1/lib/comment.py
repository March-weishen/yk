import json
import struct
import os
from conf import settings
from hashlib import md5

BASE_UPLOAD_DIR = settings.BASE_UPLOAD_DIR


def client_send(c,dic):
    json_dic = json.dumps(dic).encode("utf-8")
    str_dic = struct.pack("i",len(json_dic))
    c.send(str_dic)
    c.send(json_dic)

def client_recv(c):
    dic_len = struct.unpack("i",c.recv(4))[0]
    dic = json.loads(c.recv(dic_len).decode("utf-8"))
    return dic


def show_list(l):
    for i, j in enumerate(l,1):
        print(i,j,sep="    ")


def get_movies_list():
    movies_list = os.listdir(BASE_UPLOAD_DIR)
    if movies_list:
        return movies_list
    return False


def get_movie_md5(movie_path):
    md = md5()
    with open(movie_path,"rb") as f:
        md.update(f.read())
    return md.hexdigest()


def progress(size, file_size):
    percent = size * 100 / file_size
    if percent >= 100:  # 如果百分比大于1的话则取1
        percent_r = 100
        print('\r%s%%%s' % (percent_r, "*" * 100))
        return
    percent_r = "%.3f" % percent
    print('\r%s%%%s' % (percent_r, "*" * int(percent)), end='', flush=True)
    # \r 代表调到行首的意思，\n为换行的意思，fiel代表输出到哪，flush=True代表无延迟，立马刷新。第二个%s是百分比
