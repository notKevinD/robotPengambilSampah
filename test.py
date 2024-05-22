import cv2
import numpy as np

cap = cv2.VideoCapture(0)
nilaiY = 0 
toggleKiriKanan = 0 # 0 robot gerak ke kiri, 1 ke kanan
ijin=0
fps = 0
frame_count = 0
jenis = "1"
# start_time = Function.time.time()

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    frame = cv2.flip(frame,1)
    frame = cv2.flip(frame,0)
    if not ret:
        break
    frame_count+=1
    # if Function.time.time() - start_time >= 1:
    #     fps = frame_count / (Function.time.time() - start_time)
    #     print("FPS:", fps)
    #     frame_count = 0
    #     start_time = Function.time.time()
    #menemukan contour meja
    frame = cv2.imread('foto.jpg')
    frame = cv2.resize(frame,(640,480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    layarHitam = np.zeros_like(gray)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)
    _, binary = cv2.threshold(gray,60,255, cv2.THRESH_BINARY)  
    binary = cv2.bitwise_not(binary)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    if contours:
        #menggambar masking meja
        biggest_contour = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(biggest_contour)
        print(cv2.contourArea(biggest_contour))
        # mask = cv2.drawContours(layarHitam, [biggest_contour], 0,(255,255,255),-1)
        mask = cv2.rectangle(layarHitam,(x,y+20),(x+w,y+h),(255,255,255),-1)
        hanyaObjek = cv2.bitwise_and(frame,frame,mask=mask)

        #mencari contour sampah2
        hanyaObjekGray = cv2.cvtColor(hanyaObjek, cv2.COLOR_BGR2GRAY)
        _, binary_roi = cv2.threshold(hanyaObjekGray, 60, 255, cv2.THRESH_BINARY)
        contours_roi, _ = cv2.findContours(binary_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        biggest_contour1 = contours_roi
        contour_sampah=[]
        if biggest_contour1:
            for biggest_contoura in biggest_contour1:
            #menggambar contour sampah dengan ukuran min dan max yang ditentukan
                if cv2.contourArea(biggest_contoura) > 4000:
                    contour_sampah.append(biggest_contoura)
            if contour_sampah:
                    contourYTerdekat = np.zeros_like(biggest_contour1[0])
                    nilaiUtama = 10000
                    for biggest_contoura in contour_sampah: 
                        x,y,w,h = cv2.boundingRect(biggest_contoura)
                        if abs(320-(x+w/2)) < nilaiUtama:
                            contourYTerdekat = biggest_contoura
                            nilaiUtama = abs(320-(y+w/2))
                    x, y, w, h = cv2.boundingRect(contourYTerdekat)
                    print("besar kontour sampah =" + str(cv2.contourArea(contourYTerdekat)))
                    cropped_image = hanyaObjek[y:y+h, x:x+w]
                    #menemukan warna rata2
                    cropped_image_hsv = cv2.cvtColor(hanyaObjek[y:y+h, x:x+w], cv2.COLOR_BGR2HSV)
                    mean_color = cv2.mean(cropped_image)
                    mean_color_hsv = cv2.mean(cropped_image_hsv)
                    # centerx = int((w)/2)
                    # centery = int((h)/2)
                    warna = tuple(map(int, mean_color[:3]))
                    warna_hsv = tuple(map(int, mean_color_hsv[:3]))
                    #menggambar contour dengan warna rata rata, titik tengah warna merah, dan jenis sampah
                    cv2.drawContours(frame, [contourYTerdekat], -1, warna, -1)
                    cv2.circle(frame,(int(x+w/2),int(y+h/2)),5,(0,0,255),-1)
                    # jenis = the_color(warna_hsv)
                    print(warna_hsv)
                    
                    # cv2.putText(frame, jenis,(int(x+w/2),int(y+h/2)),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,255,255),1)
                    


        
    cv2.line(hanyaObjek,(280,0),(280,480),(255,255,255), 1, cv2.LINE_4)
    cv2.line(hanyaObjek,(360,0),(360,480),(255,255,255), 1, cv2.LINE_4)
    cv2.imshow('hanyaobjek', hanyaObjek)
    cv2.imshow('layarhitam', layarHitam)
    cv2.imshow('Frame5', binary_roi)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    if ijin==2: 
        break
#robot sudah ditengah, mengembalikan nilai dari y dan jenis sampah
cap.release()
cv2.destroyAllWindows()
# return nilaiy, jenis