import os,sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from TcpServer import tcpsever
    tcpsever.service()
