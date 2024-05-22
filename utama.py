import numpy as np
import cv2
import Function
import deteksiSampah

nilaiYSampah = 0
nilaiSampahBawah = 100
nilaiSampahAtas = 300
titikKotakSampah = 500
nilaiTinggiMeja = 200
nilaiTinggiBuatKamera = 500
# cap = cv2.VideoCapture(-1)
Function.Setup()
Function.dekatiMeja()
Function.belokMeja()

while True:
      nilaiy,jenis = deteksiSampah.cariObjek()
      print(nilaiy)
      print(jenis)
      Function.time.sleep(1)
      if nilaiy < 120:
            nilaiYSampah = nilaiSampahBawah
      else :
            nilaiYSampah = nilaiSampahAtas
      Function.motorStepper(nilaiYSampah, nomorStepper=1)
      # ###################################################################### masih perlu perbandingan nilai y dan jarak sesungguhnya
      Function.motorStepper(titikGerak=-45000, nomorStepper=0)
      # ######################################################################perlu titik stepper 1 mengenai meja
      Function.Suction(1) #menghidupkan Suction
      Function.motorStepper(titikGerak=nilaiTinggiBuatKamera, nomorStepper=0)
    # ###################################################################### kembali ke titik awal stepper
      
    # ###################################################################### perlu function buat cari kotak sampah yang benar
      Function.motorStepper(titikGerak=titikKotakSampah, nomorStepper=1)
    # ######################################################################gerak Stepper 1 ke tong sampah
    # Function.Suction(1) #mematikan Suction
    # Function.motorStepper(titikGerak=50, nomorStepper=1) #mengembalikan stepper 1 ke daerah tengah





# kevin, nilai = cariObjek()
      if cv2.waitKey(1) & 0xFF == ord('q'): 
                  break
# cap.release()
# cv2.destroyAllWindows()

