import os
from time import sleep
import pigpio


pi = pigpio.pi()

pi.setmode(pi.BCM)

pi.setup(13,pi.OUT )
pi.setup(12,pi.OUT )
pi.setup(18, pi.OUT)

servo= pi.PWM(18)
pi.set_PWM_frequency(18, 50)
servo.start(0)

ESC1_GPIO= pi.PWM(12)  #informa o pino que a ESC ta conectada
pi.set_servo_pulsewidth(ESC1_GPIO, 0)
pi.set_PWM_frequency(12, 50)

ESC2_GPIO= pi.PWM (13)  #informa o pino que a ESC ta conectada
pi.set_servo_pulsewidth(ESC2_GPIO, 0)
pi.set_PWM_frequency(13, 50)


max_value = 2000 #valores max e min de largura de pulso da ESC
min_value = 700
#sem o comando manual
print(" OBRIGATÓRIO: insira calibrate para calibrar a ESC em primeiro lançamento")
print("Se a ESC ja estiver calibrada, digite control, arm OU stop ")
#arm para armar a esc se ela já estiver calibrada
#control para inicializar e controlar a velocidade


def calibrate():   #calibrar a ESC
    print("vamos calibrar a ESC")
    pi.set_servo_pulsewidth(ESC1_GPIO,0)
    pi.set_servo_pulsewidth(ESC2_GPIO,0)
    print("verifique se a bateria está desconectada e aperte ENTER")
    inp=input()
    if inp=='':
      pi.set_servo_pulsewidth(ESC1_GPIO,max_value)
      pi.set_servo_pulsewidth(ESC2_GPIO,max_value)
      print("se n escutar um bip bip e um tom gradual é pq deu ruim")
      inp=input()
      if inp == '':
          pi.set_servo_pulsewidth(ESC1_GPIO, min_value)
          pi.set_servo_pulsewidth(ESC2_GPIO, min_value)
          print('bip')
          sleep(4)
          print('quase lá...')
          pi.set_servo_pulsewidth(ESC1_GPIO,0)
          pi.set_servo_pulsewidth(ESC2_GPIO,0)
          sleep(2)
          print("armar a ESC")
          pi.set_servo_pulsewidth(ESC1_GPIO,min_value)
          pi.set_servo_pulsewidth(ESC2_GPIO,min_value)
          sleep(2)
          print('ESC armada! batmovel pronto pra ação')
          control()
          SetAngle()


def control():
    print("iniciando o motor...contando com  ESC calibrada e armada. se n, ctrl 'x'")
    sleep(1)
    speed = 1000
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC1_GPIO, speed)
        pi.set_servo_pulsewidth(ESC2_GPIO, speed)
        inp = input()
        if inp == "q":
            speed -= 100
            print("speed =", speed)
        elif inp == "e":
            speed += 100
            print("speed =", speed)
        elif inp == "d":
            speed += 10
            print("speed =", speed)
        elif inp == "a":
            speed -= 10
            print("speed =", speed)
        elif inp == "stop":
            stop()
            break
        elif inp == "arm":
            arm()
            break
        else:
            print("Press a, q, d, or e")

def SetAngle(angle):
    duty= angle/18 + 2 #2 é o menor possível
    pi.output(18,True)
    servo.ChangeDutyCycle(duty)
    sleep(1)
    pi.output(18, False)
    servo.ChangeDutyCycle(0)

    SetAngle(90) #90/18= 5 +2 = 7
    sleep(2)
    SetAngle(0) #2 (min)
    sleep (2)
    SetAngle(180) #180/18 + 2 = 12 (max)
    sleep(2)

def arm(): #arma a ESC depois que ela ja está calibrada
    print("caso a ESC já esteja calibrada mas não armada,conecte a bateria e aperte ENTER")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC1_GPIO, 0)
        pi.set_servo_pulsewidth(ESC2_GPIO, 0)
        sleep(1)
        pi.set_servo_pulsewidth(ESC1_GPIO, max_value)
        pi.set_servo_pulsewidth(ESC2_GPIO, max_value)
        sleep(1)
        pi.set_servo_pulsewidth(ESC1_GPIO, min_value)
        pi.set_servo_pulsewidth(ESC2_GPIO, min_value)
        sleep(1)
        control()
        SetAngle()

def stop():
    pi.set_servo_pulsewidth(ESC1_GPIO,0)
    pi.set_servo_pulsewidth(ESC2_GPIO,0)
    servo.stop()
    pi.stop()