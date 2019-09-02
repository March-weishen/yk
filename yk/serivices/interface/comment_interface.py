from lib import comment
from core import models
from conf import settings
import time

alive_user = settings.alive_user


def register(dic, conn):
    name = dic.get("name")
    pwd = dic.get("pwd")
    if not comment.check_name(name):
        dic_back = {"flag": 1, "msg": "注册成功！"}
        comment.service_send(conn, dic_back)
        a = models.User(name=name, password=pwd, is_vip=0, is_locked=0, user_type=dic.get("user_type"),
                        register_time=time.strftime("%Y-%m-%d %H:%M:%S"))
        a.save()
    else:
        dic_back = {"flag": 0, "msg": "用户已经存在！"}
        comment.service_send(conn, dic_back)


def login(dic, conn):
    name = dic.get("name")
    pwd = dic.get("pwd")
    object_user = comment.check_login(name, pwd)
    if object_user:
        notice = comment.check_notice(flag=1)
        dic_back = {"flag": 1, "msg": "登陆成功！", "user_id": object_user.id, "is_vip": object_user.is_vip,"notice":notice}
        session_obj = comment.get_md5(name)
        dic_back["session"] = session_obj
        dic_back["is_vip"] = object_user.is_vip

        settings.mutex.acquire()
        alive_user[dic["addr"]] = [session_obj, object_user.id]
        settings.mutex.release()

        comment.service_send(conn, dic_back)

    else:
        dic_back = {"flag": 0, "msg": "账号或密码错误！"}
        comment.service_send(conn, dic_back)
