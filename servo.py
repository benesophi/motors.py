import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT) #informar o pino
servo= GPIO.PWM(03, 50) #pino 03 inicializado a 50Hz
servo.start(0)
sleep(2)

def SetAngle(angle):
    duty= angle/18 + 2 #2 é o menor possível
    GPIO.output(03,True)
    servo.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(03, False)
    servo.ChangeDutyCycle(0)

SetAngle(90) #90/18= 5 +2 = 7
sleep(2)
SetAngle(0) #2 (min)
sleep (2)
SetAngle(180) #180/18 + 2 = 12 (max)
sleep(2)


servo.stop()
GPIO.cleanup()
