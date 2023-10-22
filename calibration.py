import os
from time import sleep
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT) #informar o pino
servo= GPIO.PWM(18, 50) #pino 03 inicializado a 50Hz
servo.start(0)

GPIO.setup(13,GPIO.OUT )
GPIO.setup(12,GPIO.OUT )


ESC1= GPIO.PWM(12,50)#informa o pino que a ESC1 ta conectada
ESC1.ChangeDutyCycle(0)

ESC2= GPIO.PWM(13,50)#informa o pino que a ESC2 ta conectada
ESC2.ChangeDutyCycle(0)

print("funcionando ok ")

max_value = 100 #valores max e min de largura de pulso da ESC
min_value = 0
#sem o comando manual
print(" OBRIGATÓRIO: insira calibrate para calibrar a ESC em primeiro lançamento")
print("Se a ESC ja estiver calibrada, digite control, arm OU stop ")
#arm para armar a esc se ela já estiver calibrada
#control para inicializar e controlar a velocidade


def calibrate():   #calibrar a ESC
    print("vamos calibrar as ESCs")
    ESC1.ChangeDutyCycle(0)
    ESC2.ChangeDutyCycle(0)
    print("verifique se a bateria está desconectada e aperte ENTER")
    inp=input()
    if inp=='':
      ESC1.ChangeDutyCycle(max_value)
      ESC2.ChangeDutyCycle(max_value)
      print("se n escutar um bip bip e um tom gradual é pq deu ruim")
      inp=input()
      if inp == '':
          ESC1.ChangeDutyCycle(min_value)
          ESC2.ChangeDutyCycle(min_value)
          print('bip')
          sleep(10)
          print('quase lá...')
          ESC1.ChangeDutyCycle(0)
          ESC2.ChangeDutyCycle(0)
          sleep(5)
          ESC1.ChangeDutyCycle(min_value)
          ESC2.ChangeDutyCycle(min_value)
          sleep(2)
          print('ESC armada! batmovel pronto pra ação')
          control()
          SetAngle()

def control():
    print("iniciando o motor...ESC calibrada e armada. se n, ctrl 'x'")
    print("iniciando o motor...ESC calibrada e armada. se n, ctrl 'x'")
    sleep(1)
    speed = 1000
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        ESC1.ChangeDutyCycle(speed)
        ESC2.ChangeDutyCycle(speed)
        inp = input()

        if inp == "q": #diminui em 100
            speed -= 100
            print("speed =", speed)
        elif inp == "e": #aumenta em 100
            speed += 100
            print("speed =", speed)
        elif inp == "d": #aumenta em 10
            speed += 10
            print("speed =", speed)
        elif inp == "a": #diminui em 10
            speed -= 10
            print("speed =", speed)
        elif inp == "stop": #PARA
            stop()
            break
        elif inp == "arm": #armar nov a esc 
            arm()
            break
        else:
            print("WHAT DID I SAY!! Press a, q, d, or e")

def SetAngle(angle):
    duty= angle/18 + 2 #2 é o menor possível
    GPIO.output(18,True)
    servo.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(18, False)
    servo.ChangeDutyCycle(0)
    print('iniciando o servo motor...')
    servo.SetAngle(90) 
    sleep(0.5)
    servo.SetAngle(0)
    sleep(0.5)
    servo.Setangle(180)
    sleep(0.5)
    servo.stop()


def arm(): #arma a ESC depois que ela ja está calibrada
    print("caso a ESC já esteja calibrada mas não armada,conecte a bateria e aperte ENTER")
    inp = input()
    if inp == '':
        ESC1.ChangeDutyCycle(0)
        ESC2.ChangeDutyCycle(0)
        sleep(1)
        ESC1.ChangeDutyCycle(max_value)
        ESC2.ChangeDutyCycle(max_value)
        sleep(1)
        ESC1.ChangeDutyCycle(min_value)
        ESC2.ChangeDutyCycle(min_value)
        sleep(1)
        control()
        SetAngle()

def stop():
    ESC1.ChangeDutyCycle(0)
    ESC2.ChangeDutyCycle(0)
    servo.stop()
    GPIO.cleanup()

    inp = input()
if inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
