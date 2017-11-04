#!/usr/bin/python

import pygame
import sys
import time
import smbus
import math
import sys
sys.path.append('/home/pi/raspi/i2c-sensors/')
import bitify.python.sensors.oldimu as imu
import RPi.GPIO as GPIO
import PID
#initalizing variables (setting up the stage)

minimum = 50
maximum = 80
size=(1024,768)
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255, 0,0)

speed=25

motor1 = 0
motor2 = 0
motor3 = 0
motor4 = 0

motor_increase = 1

bus = smbus.SMBus(1)

freq = 490

#intialise Pygame

pygame.init()
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Drone Control")
myfont = pygame.font.SysFont("monospace", 20)

#Define the GPIO Pins

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
pwm1=GPIO.PWM(11,freq)
pwm2=GPIO.PWM(12,freq)
pwm3=GPIO.PWM(13,freq)
pwm4=GPIO.PWM(15,freq)

time.sleep(1)

#Define Originalstate of the motor and Background for the GUI
(P, I, D) = (1.2, 0.1, 0.002)
PitchPid = PID.PID(P, I, D)
RollPid = PID.PID(P, I, D)
PitchPid.SetPoint= -0.06
PitchPid.setSampleTime(0.001)

RollPid.SetPoint=-0.14
RollPid.setSampleTime(0.001)
END = 10
    
def original_state(speed):

    global motor1
    motor1 = speed
    global motor2
    motor2 = speed
    global motor3
    motor3 = speed
    global motor4
    motor4 = speed


def background():
    drone= pygame.image.load("gui.bmp")
    screen.blit(drone, (0,0))
    label_credit = myfont.render("Developed By:", 1, black)
    screen.blit(label_credit, (610, 650))
    label_names = myfont.render("Karthick Narayanan and Doraditya N", 1, black)
    screen.blit(label_names, (610, 680))
    
def PitchPID(pitch):
    for i in range(1, END):
        PitchPid.update(pitch)
        pcorr = PitchPid.output
        global motor4
        global motor2
        motor4 = motor4 + (pcorr/50)
        motor2 = motor2 - (pcorr/50)
        if motor2<minimum:
            motor2 = minimum
        elif motor4>maximum:
            motor4 = maximum
        if motor4<minimum:
            motor4 = minimum
        elif motor2>maximum:
            motor2 = maximum      
        result = [motor1,motor2, motor3,motor4]
        #print "PitchPID result:"+str(result)
        motorpush(result)
        
def RollPID(roll):
    for i in range(1, END):
        RollPid.update(roll)
        rcorr = RollPid.output
        #print "rcorr: "+str(rcorr)
        global motor3
        global motor1
        motor3 = motor3 + (rcorr/50)
        motor1 = motor1 - (rcorr/50)
        if motor3<minimum:
            motor3 = minimum
        elif motor3>maximum:
            motor3 = maximum
        if motor1<minimum:
            motor1 = minimum
        elif motor1>maximum:
            motor1 = maximum
        result =[motor1,motor2, motor3,motor4]
        motorpush(result)
        
background()
pygame.display.flip()

pwm1.start(25)
pwm2.start(25)
pwm3.start(25)
pwm4.start(25)

imu_controller = imu.OLDIMU(bus, 0x68, 0x1e,"OLD IMU")
imu_controller.set_compass_offsets(0, 0, 0)

def motorpush(motor):        # Send value to Motor from the received String
    pwm1.ChangeDutyCycle(round(motor[0],1))
    pwm2.ChangeDutyCycle(round(motor[1],1))
    pwm3.ChangeDutyCycle(round(motor[2],1))
    pwm4.ChangeDutyCycle(round(motor[3],1))
    #print "Motor result:"+str(motor)
PIDflag = False
RollPIDflag = False
PitchPIDflag = False
while True:
    Old_time = time.time()
    (pitch, roll, yaw) = imu_controller.read_pitch_roll_yaw()
    time.sleep(0.00001)
    if(pitch-PitchPid.SetPoint>0.2 or pitch-PitchPid.SetPoint<-0.2):
        PIDflag = True
        PitchPIDflag = True
    if(roll- RollPid.SetPoint>0.2 or roll-RollPid.SetPoint<-0.2):
        PIDflag = True
        RollPIDflag = True    
    if PIDflag:        
        if PitchPIDflag:
            PitchPID(pitch)
        if RollPIDflag:
            RollPID(roll)
        PIDflag = False
        RollPIDflag = False
        PitchPIDflag = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        background()
        
        if pygame.key.get_focused():
            press = pygame.key.get_pressed()
            for i in range(0,len(press)):

                if press[i] == 1:

                    if pygame.key.name(i) == 'w':
                        forward = pygame.image.load("forward.bmp")
                        screen.blit(forward, (461, 206))
                        motor3 = motor3+ motor_increase

                    elif pygame.key.name(i) == 's':
                        backward = pygame.image.load("backward.bmp")
                        screen.blit(backward, (461, 476))
                        motor1 = motor1+ motor_increase
                       	
                        
                    elif pygame.key.name(i) == 'a':
                        left = pygame.image.load("left.bmp")
                        screen.blit(left, (200, 340))
                        motor2 = motor2+ motor_increase
                       

                    elif pygame.key.name(i) == 'd':
                        right = pygame.image.load("left.bmp")
                        screen.blit(right, (710, 350))
                        motor4 = motor4+ motor_increase
			
                    if pygame.key.name(i) == 'z':
                        forward = pygame.image.load("forward.bmp")
                        screen.blit(forward, (461, 206))
                        motor1 = motor1- motor_increase
			
                        

                    elif pygame.key.name(i) == 'x':
                        backward = pygame.image.load("backward.bmp")
                        screen.blit(backward, (461, 476))
                        motor2 = motor2- motor_increase
                       	
                        
                    elif pygame.key.name(i) == 'c':
                        left = pygame.image.load("left.bmp")
                        screen.blit(left, (200, 340))
                        motor3 = motor3- motor_increase
                       

                    elif pygame.key.name(i) == 'v':
                        right = pygame.image.load("right.bmp")
                        screen.blit(right, (710, 350))
                        motor4 = motor4- motor_increase
    
                    elif pygame.key.name(i) == 'e':
                        clockwise = pygame.image.load("clockr.bmp")
                        screen.blit(clockwise, (710, 350))
			motor2 = motor2+ motor_increase
                        motor4 = motor4+ motor_increase
			motor1 = motor1- motor_increase
			motor3 = motor3- motor_increase			

                    elif pygame.key.name(i) == 'q':
                        anticlockwise = pygame.image.load("anticlock.bmp")
                        screen.blit(anticlockwise, (200, 340))
                        motor1 = motor1+ motor_increase
			motor3 = motor3+ motor_increase
			motor2 = motor2- motor_increase
                        motor4 = motor4- motor_increase

                    elif pygame.key.name(i) == 't':
                        up = pygame.image.load("down.bmp")
                        for i in range(35,51):
                            screen.blit(up, (200, 340))
                            pygame.display.update()
                            speed = i
                            original_state(speed)
                            time.sleep(0.5)
                        PIDflag = True                               
                    elif pygame.key.name(i) == 'l':
                        down = pygame.image.load("down.bmp")
                        screen.blit(down, (710, 350))
                        speed = 0
                        original_state(speed)
                        
                    elif pygame.key.name(i) == 'u':
                        down = pygame.image.load("up.bmp")
                        screen.blit(down, (710, 350))
                        speed = speed+1
                        original_state(speed)
                        
                    elif pygame.key.name(i) == 'j':
                        down = pygame.image.load("down.bmp")
                        screen.blit(down, (710, 350))
                        speed = speed-1
                        original_state(speed)
                    elif pygame.key.name(i) == 'm':
                        original_state(speed)
            
            pygame.display.update()
            
    motor = [motor1,motor2, motor3,motor4]
    motorpush(motor)
    New_time = time.time()
    total_time = New_time - Old_time
    print total_time
