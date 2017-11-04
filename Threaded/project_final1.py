
# Initialsing the variables and Importing features
import smbus
import math
from time import sleep
import sys
sys.path.append('/home/pi/raspi/i2c-sensors/')
import socket

import bitify.python.sensors.oldimu as imu
import RPi.GPIO as GPIO

bus = smbus.SMBus(1)

freq = 490

#GPIO definitions


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
pwm1=GPIO.PWM(11,freq)
pwm2=GPIO.PWM(12,freq)
pwm3=GPIO.PWM(13,freq)
pwm4=GPIO.PWM(15,freq)

sleep(1)

# Start GPIO pins with a PWM Duty cycle and Push till 49%
pwm1.start(25)
pwm2.start(25)
pwm3.start(25)
pwm4.start(25)

    
def motorpush(data1):        # Send value to Motor from the received String
    data1=data1.split()
    data1 = [float(x.strip(' []')) for x in data1]
    #print data1
    #sleep(0.01)
    print data1
    pwm1.ChangeDutyCycle(data1[0])
    pwm2.ChangeDutyCycle(data1[1])
    pwm3.ChangeDutyCycle(data1[2])
    pwm4.ChangeDutyCycle(data1[3])
    
# Program Starts here...

imu_controller = imu.OLDIMU(bus, 0x68, 0x1e,"OLD IMU")
imu_controller.set_compass_offsets(0, 0, 0)

HOST = '127.0.0.1'         # The remote host
PORT = 50007                    # The same port as used by the server

# Create the Socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print "intialising..."

# Main Loop Function 

while(1):
    (pitch, roll, yaw) = imu_controller.read_pitch_roll_yaw()
    sleep(0.001)
    result = "%.2f %.2f %.2f " % (pitch, roll, yaw)
    s.sendall(result)
    sleep(0.001)
    data = s.recv(32)
    if not data: break
	#motorpush(data)
s.close()
GPIO.cleanup()
