import socket
from core import src


def client():
    c = socket.socket()
    c.connect(("127.0.0.1",8888))
    src.run(c)