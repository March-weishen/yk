import os,sys
BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

from TcpClient import tcpclient
if __name__ == '__main__':
    tcpclient.client()