import os
import sys
sys.path.append(os.path.dirname(__file__))

from TcpServer import tcpsever

if __name__ == '__main__':
    tcpsever.service()