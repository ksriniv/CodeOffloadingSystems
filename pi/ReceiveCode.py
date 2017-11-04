import socket

def Connect():
    global s 
    HOST = '192.168.43.198'    # The remote host
    PORT = 33333              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

def Receive():
    while True:
        data = s.recv(20)
        print 'Received', repr(data)
if __name__ == '__main__':
    Connect()
    while True:
        Receive()
    s.close()
