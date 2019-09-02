from lib import comment
from core import models
import time
from conf import settings

alive_user = settings.alive_user
mutex = settings.mutex

def register(conn, dic):
    name = dic.get("name")
    pwd = dic.get("pwd")
    user_type = dic.get("user_type")
    flag = comment.check_user(name)
    if flag:
        dic1 = {"flag":0,"msg":"用户已存在！"}
        comment.service_send(conn,dic1)
        return
    password = comment.get_md5(pwd)
    register_time = time.strftime("%Y-%m-%d %H:%M:%S")
    user_obj = models.User(name=name,password=password,is_vip=0,is_locked=0,user_type=user_type,register_time=register_time)
    user_obj.save()
    dic1 = {"flag":1,"msg":"注册成功！"}
    comment.service_send(conn,dic1)


def login(conn, dic):
    name = dic.get("name")
    pwd = dic.get("pwd")
    password = comment.get_md5(pwd)
    user_obj = comment.check_user(name)
    if user_obj:
        if user_obj.password == password:
            user_id = user_obj.id
            session = comment.get_md5(name)
            addr = dic.get("addr")
            notice = comment.new_notice()
            mutex.acquire()
            alive_user[addr] = [session,user_id]
            mutex.release()
            dic = {"flag":2,"msg":"登陆成功！","session":session,"notice":notice}
        else:
            dic = {"flag":1,"msg":"密码错误！"}
    else:
        dic = {"flag":0,"msg":"用户不存在！"}
    comment.service_send(conn,dic)
