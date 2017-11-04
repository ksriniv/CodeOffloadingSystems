import socket
import sensor

def Connect():
    global conn    
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 55555              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr

def Send():
    sensor.I2C_Initialise()
    while True:
        sensorvalues = sensor.Main_Sensor()
        conn.sendall(sensorvalues)

if __name__ == '__main__':
    Connect()
    while True: 
        Send()
    conn.close()
