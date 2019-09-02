import os
from threading import Lock

mutex = Lock()

BASE_DIR = os.path.dirname(os.path.dirname((__file__)))

BASE_UPLOAD_DIR = os.path.join(BASE_DIR,"upload_movies")

alive_user = {}
