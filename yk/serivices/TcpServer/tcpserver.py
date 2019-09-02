import socket
from lib import comment
from interface import admin_interface, user_interface, comment_interface
from concurrent.futures import ThreadPoolExecutor
from conf import settings
from threading import Lock

alive_user = settings.alive_user
settings.mutex = Lock()
mutex = settings.mutex

thread_pool = ThreadPoolExecutor(50)

func_dict = {
    "register": comment_interface.register,
    "login": comment_interface.login,
    "check_movie": admin_interface.check_movie,
    "upload_movie": admin_interface.upload_movie,
    "delete_movie": admin_interface.delete_movie,
    "release_notice": admin_interface.release_notice,
    "buy_vip": user_interface.buy_vip,
    "select_movie": user_interface.select_movie,
    "download_free_movie": user_interface.download_free_movie,
    "download_charge_movie": user_interface.download_charge_movie,
    "check_download_movie": user_interface.check_download_movie,
    "check_notice": user_interface.check_notice
}

s = socket.socket()
s.bind(("127.0.0.1", 8001))
s.listen(5)


def w(conn, addr):
    try:
        while True:
            dic = comment.service_recv(conn)
            dic["addr"] = addr
            func_name = dic.get("type")
            func_dict.get(func_name)(dic, conn)
    except ConnectionResetError as e:
        print(addr, e)
        mutex.acquire()
        alive_user.pop(addr)
        mutex.release()
        conn.close()


def service():
    while True:
        conn, addr = s.accept()
        thread_pool.submit(w, conn, addr)
        mutex.acquire()
        print(alive_user)
        mutex.release()
