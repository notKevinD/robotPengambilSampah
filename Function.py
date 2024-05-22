#!/usr/bin/env python3
import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial('/dev/ttyACM0',115200, timeout=1.0)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Ignore warning for now


pinStepStepper = [21,8]
pinDirStepper = [20,7]
pinInputStepper = [5,6] #sensor untuk mecari titik 0 stepper
revolution = 1600
delayStepper = 0.0001
titikStepper = [0,0]
titikAwal = [500,500]
centimeterperputaran = 0
jarakcm = 0
putaran = jarakcm * centimeterperputaran

pinSuction = 7 #suction relay

# 0 untuk depan
# 1,2 untuk samping
# TRIG_PIN = [10,13,12]
# ECHO_PIN = [9,19,16]



#kontrol motor stepper

def motorStepper(titikGerak,nomorStepper): #titikGerak sudah nilai int, jadi sebelumnya harus dihitung titik y menjadi titikGerak stepper
    global titikStepper
    gerakan = titikGerak - titikStepper[nomorStepper]
    if gerakan > 0:
        GPIO.output(pinDirStepper[nomorStepper], GPIO.HIGH)
    else:
        GPIO.output(pinDirStepper[nomorStepper], GPIO.LOW)
    titikStepper[nomorStepper] += gerakan
    for _ in range(abs(gerakan)):
        GPIO.output(pinStepStepper[nomorStepper], GPIO.HIGH)
        time.sleep(delayStepper)
        GPIO.output(pinStepStepper[nomorStepper], GPIO.LOW)
        time.sleep(delayStepper)
        if(GPIO.input(pinInputStepper[nomorStepper])) == False and gerakan > 0:
            titikStepper[nomorStepper]=0
            break

def Suction(nilai):
    if nilai == 1:
        GPIO.output(pinSuction, GPIO.HIGH)
    else:
        GPIO.output(pinSuction, GPIO.LOW)
        
def dekatiMeja():
    kirimSerial("dekatiMeja")
    while True:    
        terimaData = menerimaData()
        print(terimaData)
        if terimaData == "selesai":
            break
    
def maju():
    kirimSerial("maju")

def majuPelan():
    kirimSerial("majuPelan")

def mundur():
    kirimSerial("mundur")

def mundurPelan():
    kirimSerial("mundurPelan")

def stop():
    kirimSerial("berhenti")

#setupPin
def Setup():
    GPIO.setup(pinSuction, GPIO.OUT)

    #set pin stepper
    for pinstep in pinStepStepper:
        GPIO.setup(pinstep, GPIO.OUT)
    for pindir in pinDirStepper:
        GPIO.setup(pindir, GPIO.OUT)
    for pinInputSteppera in pinInputStepper:
        GPIO.setup(pinInputSteppera, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    #setStepper ke titik 0 
    motorStepper(-10000, 0)
    motorStepper(-20000, 1)
    # motorStepper(titikAwal[0], 0)
    # motorStepper(titikAwal[1], 1)

    time.sleep(1.5)
    ser.reset_input_buffer()
    print("Serial OK")

#initialize

def kirimSerial(data):
    ser.write(data.encode('utf-8'))
    # print("kirimData"+data)
    while ser.in_waiting <= 0:
        time.sleep(0.01)
    response = ser.readline().decode('utf-8').rstrip()
    print(response)
    
def menerimaData():
    while ser.in_waiting <=0:
        time.sleep(0.01)
    response = ser.readline().decode('utf-8').rstrip()
    return response

# def maju():
    