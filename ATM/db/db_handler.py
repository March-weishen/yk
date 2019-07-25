from conf import settings
import json
import os

DB_BASE = settings.BASE_PATH

def check_usernam(input_name):
    user_path = os.path.join(DB_BASE, "db\{}.json".format(input_name))
    if os.path.exists(user_path):
        with open(user_path,"r",encoding="utf-8") as u:
            user_dict = json.load(u)
        return user_dict


def save(user_dict):
    user_path = os.path.join(DB_BASE, "db\{}.json".format(user_dict["user"]))
    with open(user_path, "w", encoding="utf-8") as u:
        json.dump(user_dict, u,ensure_ascii=False)


def check_admin(input_name):
    user_path = os.path.join(DB_BASE, r"db\admin\{}.json".format(input_name))
    if os.path.exists(user_path):
        with open(user_path,"r",encoding="utf-8") as u:
            admin_dict = json.load(u)
        return admin_dict
