import smbus
import math
from time import sleep
import sys
sys.path.append('/home/pi/raspi/i2c-sensors/')
import bitify.python.sensors.oldimu as imu
import RPi.GPIO as GPIO

def I2C_Initialise():
    global bus
    global imu_controller
    bus = smbus.SMBus(1)
    imu_controller = imu.OLDIMU(bus, 0x68, 0x1e,"OLD IMU")
    imu_controller.set_compass_offsets(0, 0, 0)
    print "intialising..."

# Main Loop Function 
def Main_Sensor():
    (pitch, roll, yaw) = imu_controller.read_pitch_roll_yaw()
    result = "%.2f %.2f %.2f" % (pitch, roll, yaw)
    return str(result)

if __name__ == '__main__':
        I2C_Initialise()
        while True:
            Main_Sensor()
