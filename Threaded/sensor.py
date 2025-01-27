import smbus
import math
import sys
sys.path.append('/home/pi/raspi/i2c-sensors/')
from time import sleep
import bitify.python.sensors.mpu6050 as mpu
bus = smbus.SMBus(1)
mpu_controller = mpu.MPU6050(bus, 0x68,"MPU")
address = 0x1e
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92
def Main_sensor():
    x_out = read_word_2c(3) * scale
    y_out = read_word_2c(7) * scale
    z_out = read_word_2c(5) * scale

    bearing  = math.atan2(y_out, x_out) 
    if (bearing < 0):
        bearing += 2 * math.pi
    yaw=math.degrees(bearing)
    

    (pitch, roll, gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = mpu_controller.read_all()
    sleep(0.01)
    result = " %.2f %.2f %.2f " % (math.degrees(pitch), math.degrees(roll), yaw)
    return result
    
    
