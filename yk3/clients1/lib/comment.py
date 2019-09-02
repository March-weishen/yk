import os
import json
import struct
from hashlib import md5
from conf import settings


UPLOAD_MOVIES = settings.UPLOAD_MOVIES


def client_send(c,dic):
    json_dic = json.dumps(dic).encode("utf-8")
    len_dic = struct.pack("i", len(json_dic))
    c.send(len_dic)
    c.send(json_dic)


def client_recv(c):
    len_dic = struct.unpack("i", c.recv(4))[0]
    dic = json.loads(c.recv(len_dic).decode("utf-8"))
    return dic


def show_list(lis):
    for i,j in enumerate(lis,1):
        print(i,j,sep="    ")


def get_movies_list():
    movies_list = os.listdir(UPLOAD_MOVIES)
    if movies_list:
        return movies_list
    return False


def get_movie_md5(movie_path):
    md = md5()
    with open(movie_path,"rb") as f:
        for i in f:
            md.update(i)
    return md.hexdigest()


