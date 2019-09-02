import os,sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)


from TcpServer import tcpserver

if __name__ == '__main__':
    tcpserver.service()
