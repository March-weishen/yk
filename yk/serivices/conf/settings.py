import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_DOWNLOAD_DIR = os.path.join(BASE_DIR,"download_movies")
BASE_UPLOAD_DIR = os.path.join(BASE_DIR,"upload_movies")

alive_user = {}

mutex = None
