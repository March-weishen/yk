import os
import sys
sys.path.append(os.path.dirname(__file__))

from TcpClient import tcpclient

if __name__ == '__main__':
    tcpclient.client()