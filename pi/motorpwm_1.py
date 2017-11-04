import RPi.GPIO as GPIO
from time import sleep
cycling= False
i=50

GPIO.setmode(GPIO.BOARD)


GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)



pwm1=GPIO.PWM(11,500)
pwm2=GPIO.PWM(12,500)
pwm3=GPIO.PWM(13,500)
pwm4=GPIO.PWM(15,500)

pwm1.start(25)
pwm2.start(25)
pwm3.start(25)
pwm4.start(25)
sleep(2)

a= raw_input("Enter s to start:")
if(a == 's'):
        cycling =True
        for j in range (35,50):
                pwm1.ChangeDutyCycle(j)
                pwm2.ChangeDutyCycle(j)
                pwm3.ChangeDutyCycle(j)
                pwm4.ChangeDutyCycle(j)
                sleep(0.5)
                print j

while (cycling == True):
        pwm1.ChangeDutyCycle(i)
        pwm2.ChangeDutyCycle(i)
        pwm3.ChangeDutyCycle(i)
        pwm4.ChangeDutyCycle(i)
        print i
        a= raw_input("Enter values to stop")
        if (a=='a'):
                i=i+1;
        elif (a=='q'):
                cycling = False

pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
GPIO.cleanup()

