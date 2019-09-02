import socket
from lib import comment
from conf import settings
from concurrent.futures import ThreadPoolExecutor
from interface import admin_interface,user_interface,comment_interface

pool = ThreadPoolExecutor(50)
mutex = settings.mutex
alive_user = settings.alive_user
func_dic={
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
    "check_notice":user_interface.check_notice,
}


s = socket.socket()
s.bind(("127.0.0.1",8888))
s.listen(5)


def w(conn,addr):
    try:
        while True:
            dic = comment.service_recv(conn)
            dic["addr"] = addr
            func_name = dic.get("type")
            func_dic.get(func_name)(conn,dic)
    except ConnectionResetError as e:
        print(addr,e)
        mutex.acquire()
        alive_user.pop(addr)
        mutex.release()
        conn.close()


def service():
    while True:
        conn, addr = s.accept()
        pool.submit(w,conn,addr)

