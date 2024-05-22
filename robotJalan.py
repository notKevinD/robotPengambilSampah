import numpy as np
import cv2
import Function
import deteksiSampah


Function.Setup()
Function.dekatiMeja()
Function.belokMeja()
while True:
    nilaiy,jenis = deteksiSampah.cariObjek()
    print(nilaiy)
    print(jenis)
    Function.time.sleep(1)
    Function.motorStepper(nilaiy, nomorStepper=1)
    ###################################################################### masih perlu perbandingan nilai y dan jarak sesungguhnya
    Function.motorStepper(titikGerak=50, nomorStepper=0)
    ######################################################################perlu titik stepper 1 mengenai meja
    Function.Suction(1) #menghidupkan Suction
    Function.motorStepper(titikGerak=100, nomorStepper=0)
    ###################################################################### kembali ke titik awal stepper

    ###################################################################### perlu function buat cari kotak sampah yang benar
    Function.motorStepper(titikGerak=50, nomorStepper=1)
    ######################################################################gerak Stepper 1 ke tong sampah
    Function.Suction(1) #mematikan Suction
    Function.motorStepper(titikGerak=50, nomorStepper=1) #mengembalikan stepper 1 ke daerah tengah





# kevin, nilai = cariObjek()
    if cv2.waitKey(1) & 0xFF == ord('q'): 
            break