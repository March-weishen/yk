import os
from threading import Lock


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

UPLOAD_MOVIES = os.path.join(BASE_DIR,"upload_movies")

mutex = Lock()

alive_user = {}