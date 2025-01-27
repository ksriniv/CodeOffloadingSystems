from threading import Thread
from time import sleep
import socket
import smbus
import math
import sys
sys.path.append('/home/pi/raspi/i2c-sensors/')
import bitify.python.sensors.oldimu as imu
import RPi.GPIO as GPIO

data = ''

def SendConnect():
    global conn
    HOSTA = ''                  # Symbolic name meaning all available interfaces
    PORTA = 55555              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOSTA, PORTA))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    print type(conn)

def Send():
    while True: 
        conn.sendall(data)
        sleep(0.000001)


def ReceiveConnect():
    global s
    HOSTB = '192.168.43.198'    # The remote host
    PORTB = 33333              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOSTB, PORTB))
    print "Its Receive Connect"

def Receive():
    while True:     
        data = s.recv(24)
        print 'Received : ', repr(data)

def I2C_Initialise():
    global bus
    global imu_controller
    bus = smbus.SMBus(1)
    imu_controller = imu.OLDIMU(bus, 0x68, 0x1e,"OLD IMU")
    imu_controller.set_compass_offsets(0, 0, 0)
    print "intialising..."

# Main Loop Function

def Main_Sensor():
    I2C_Initialise()
    global data
    while True:
        (pitch, roll, yaw) = imu_controller.read_pitch_roll_yaw()
        data = "%.2f %.2f %.2f" % (pitch, roll, yaw)
        sleep(0.000001)

def Main():
    t1 = Thread(target=Send, args=())
    t2 = Thread(target=Receive, args=())
    t3 = Thread(target=Main_Sensor, args=())
    t1.start()
    t2.start()
    t3.start()


if __name__ == '__main__':
    ReceiveConnect()
    SendConnect()
    Main()   

