from lib import comment
from core import models
from conf import settings

alive_user = settings.alive_user
mutex = settings.mutex

def register(conn, dic):
    name = dic.get("name")
    pwd = dic.get("pwd")
    pwd_md = comment.get_md5(pwd)
    flag = comment.check_user_name(name)
    if flag:
        dic_back = {"flag": 0, "msg": "用户已经存在！"}
    else:
        user_obj = models.User(name=name, password=pwd_md, is_vip=0, is_locked=0, user_type=dic.get("user_type"),
                               register_time=comment.get_time())
        user_obj.save()
        dic_back = {"flag": 1, "msg": "注册成功！"}
    comment.service_send(conn, dic_back)


def login(conn, dic):
    name = dic.get("name")
    pwd = dic.get("pwd")
    pwd_md = comment.get_md5(pwd)
    user_obj = comment.check_user_name(name)
    if not user_obj:
        dic_back = {"flag": 0, "msg": "用户不存在"}
    else:
        if pwd_md == user_obj.password:
            id = user_obj.id
            session = comment.get_md5(name)
            addr = dic.get("addr")
            mutex.acquire()
            alive_user[addr] = [session,id]
            mutex.release()
            dic_back = {"flag": 1, "msg": "登陆成功！", "session": session,"notice":comment.select_first_notice()}
        else:
            dic_back = {"flag": 0, "msg": "密码错误！"}
    comment.service_send(conn, dic_back)
