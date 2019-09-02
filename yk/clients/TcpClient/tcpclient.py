import socket
from core import src


def client():
    c = socket.socket()
    c.connect(("127.0.0.1",8001))
    src.run(c)


