#!/usr/bin/python

import pygame
import sys
import socket
from time import sleep
sys.path.append('/home/karthicknarayanan/ivPID')
import PID
#initalizing variables (setting up the stage)

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

HOST = None               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = None

def original_state(speed):

    global motor1
    motor1 = speed
    global motor2
    motor2 = speed
    global motor3
    motor3 = speed
    global motor4
    motor4 = speed
#intialise Pygame
#Define Originalstate of the motor and Background for the GUI
maximum = 70
minimum = 55

    
pygame.init()
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Drone Control")
myfont = pygame.font.SysFont("monospace", 20)

(P, I, D) = (1.2, 0.1, 0.002)
PitchPid = PID.PID(P, I, D)
RollPid = PID.PID(P, I, D)

PitchPid.SetPoint= -10.85
PitchPid.setSampleTime(0.001)

RollPid.SetPoint=3.33
RollPid.setSampleTime(0.001)
END = 1000
def PitchPID(pitch):
    for i in range(1, END):
        PitchPid.update(pitch)
        pcorr = PitchPid.output
        global motor4
        global motor2
        motor4 = motor4 + (pcorr/5)
        motor2 = motor2 - (pcorr/5)
       # if motor2<minimum:
       #     motor2 = minimum
       # elif motor2>maximum:
       #     motor2 = maximum
       # if motor4<minimum:
        #    motor4 = minimum
       # elif motor4>maximum:
        #    motor4 = maximum
        
        result = " %0.1f %0.1f %0.1f %0.1f "%(motor1,motor2, motor3,motor4)
        print "PitchPID result:"+result
        conn.send(result)
        sleep(0.05)
        data = conn.recv(256)
        data = data.split()
        data = [float(x.strip(' []')) for x in data]
        print data
        if not data: break

def RollPID(roll):
    for i in range(1, END):
        RollPid.update(roll)
        rcorr = RollPid.output
        print "rcorr: "+str(rcorr)
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
        result = " %0.1f %0.1f %0.1f %0.1f "%(motor1,motor2, motor3,motor4)
        print "RollPID result:"+result
        conn.send(result)
        sleep(0.05)
        data = conn.recv(256)
        data = data.split()
        data = [float(x.strip(' []')) for x in data]
        print data
        if not data: break
  
def background():
    drone= pygame.image.load("gui.bmp")
    screen.blit(drone, (0,0))
    label_credit = myfont.render("Developed By:", 1, black)
    screen.blit(label_credit, (610, 650))
    label_names = myfont.render("Karthick Narayanan and Doraditya N", 1, black)
    screen.blit(label_names, (610, 680))
    

background()
pygame.display.flip()

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)

conn, addr = s.accept()
print 'Connected by', addr

PIDflag = False

while True:
    data = conn.recv(256)
    data = data.split()
    data = [float(x.strip(' []')) for x in data]
    sleep(0.01)
    if PIDflag:
        #PitchPID(data[0])
        RollPID(data[1])
    print 'PID Condition surpassed'
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
                        right = pygame.image.load("right.bmp")
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
                        up = pygame.image.load("up.bmp")
                        for i in range(35,53):
                            screen.blit(up, (200, 340))
                            pygame.display.update()
                            speed = i
                            original_state(speed)
                            result = "%d %d %d %d"%(motor1,motor2, motor3,motor4)
                            conn.send(result)
                            sleep(0.5)
                            data = conn.recv(256)
                            data = data.split()
                            data = [float(x.strip(' []')) for x in data]
                            print data
                            if not data: break
                        PIDflag = True
                            
                    elif pygame.key.name(i) == 'l':
                        down = pygame.image.load("down.bmp")
                        screen.blit(down, (710, 350))
                        speed = 0
                        original_state(speed)
                        PIDflag = False
                        
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
            
    print data
    if not data: break
    result = " %0.1f %0.1f %0.1f %0.1f "%(motor1,motor2, motor3,motor4)
    print "result:"+result
    conn.send(result)
    sleep(0.05)

