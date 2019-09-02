import socket
from lib import comment
from conf import settings
from concurrent.futures import ThreadPoolExecutor
from interface import admin_interface,user_interface,comment_interface

mutex = settings.mutex

alive_user = settings.alive_user
pool = ThreadPoolExecutor(50)
func_dict = {
    "register":comment_interface.register,
    "login":comment_interface.login,
    "upload_movie":admin_interface.upload_movie,
    "delete_movie":admin_interface.delete_movie,
    "release_notice":admin_interface.release_notice,
    "buy_vip":user_interface.buy_vip,
    "select_movie":user_interface.select_movie,
    "download_free_movie":user_interface.download_free_movie,
    "download_charge_movie":user_interface.download_charge_movie,
    "check_download_movie":user_interface.check_download_movie,
    "check_notice":user_interface.check_notice
}

s = socket.socket()
s.bind(("127.0.0.1",8888))
s.listen(5)

def working(conn,addr):
    try:
        while True:
            dic = comment.service_recv(conn)
            dic["addr"] = addr
            func_type = dic.get("type")
            func_dict.get(func_type)(conn,dic)
    except ConnectionResetError as e:
        print(addr,e)
        mutex.acquire()
        alive_user.pop(addr)
        mutex.release()
        conn.close()


def service():
    while True:
        conn, addr = s.accept()
        pool.submit(working,conn,addr)
