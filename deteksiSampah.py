import numpy as np
import cv2
import Function
# import utama
JenisBenda=["daun", "plastik", "ferro","kertas","nonFerro"]


# Fungsi untuk mendapatkan titik tengah kontur
def the_color(hsv_values):
    hue = hsv_values[0]
    saturation = hsv_values[1]
    value = hsv_values[2]

    if hue > 45-10 and saturation>80-10 and value > 130-10 and hue<45+10 and saturation<80+10 and value < 130+10:
        print("nonferro")
        return "non ferro" #NONFERRO
    elif (hue > 88 and saturation>30 and value > 168 and hue < 88+8 and saturation<30+8 and value < 168+8) or ( hue > 36-4 and saturation>91-4 and value >172-4 and hue < 36+4 and saturation<91+4 and value <172+4 ):
        print("kertas")
        return "kertas" #kertas
    elif hue > 55-8 and saturation>25-5 and value > 156-5 and hue < 55+6 and saturation<25+6 and value < 156+6:
        print("ferro")
        return "ferro" #FERRO
    elif (hue > 37-3 and saturation>113-3 and value> 132-3 and hue < 37+3 and saturation<113+3 and value< 132+3) or ( hue >53-3 and saturation>216-3 and value > 104-3 and hue <53+3 and saturation<216+3 and value < 104+3):
        print("daun")
        return "daun" #daun
    elif (hue >102-3 and saturation>63-3 and value> 131-3 and hue <102+3 and saturation<63+3 and value< 131+3) or ( hue > 63-3 and saturation>97-3 and value> 81-3 and hue < 63+3 and saturation<97+3 and value< 81+3):
        print("plastik")
        return "plastik" #:Plastik
    else:
        print("tidak tahu")
        return "tidak tahu"
    

def cariObjek():
    #butuh fungsi saat 1 pun objek blum ditemukan #01
    cap = cv2.VideoCapture(-1)
    nilaiY = 0 
    toggleKiriKanan = 0 # 0 robot gerak ke kiri, 1 ke kanan
    ijin=0
    fps = 0
    frame_count = 0
    jenis = "1"
    start_time = Function.time.time()

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        frame = cv2.flip(frame,1)
        frame = cv2.flip(frame,0)
        if not ret:
            break
        frame_count+=1
        if Function.time.time() - start_time >= 1:
            fps = frame_count / (Function.time.time() - start_time)
            print("FPS:", fps)
            frame_count = 0
            start_time = Function.time.time()
        #menemukan contour meja
        # frame = cv2.imread('foto.jpg')
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
                        jenis = the_color(warna_hsv)
                        print(warna_hsv)
                        
                        cv2.putText(frame, jenis,(int(x+w/2),int(y+h/2)),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,255,255),1)
                        #menjalankan roda ke contour ya ditentukan
                        if x+w/2 < 280 :
                            print("mundur")
                            Function.mundur()
                            toggleKiriKanan = 1
                            print(y+h/2)
                            ijin = 0
                        elif x+w/2 > 320 :
                            print("maju")
                            Function.maju()  
                            toggleKiriKanan = 0
                            print(y+h/2)
                            ijin = 0
                        else:
                            print("sudah tengah")
                            Function.stop()
                            ijin+=1
                            Function.time.sleep(0.5)
                            nilaiY = y +h/2
                            print(nilaiY)
            else:
                #saat ukuran meja masih begitu
                if cv2.contourArea(biggest_contour) > 83000:
                    if toggleKiriKanan == 0:
                        Function.maju()
                    elif toggleKiriKanan == 1:
                        Function.mundur()
                #saat dipinggir, ganti arah
                else :
                    Function.stop()
                    Function.time.sleep(2)
                    toggleKiriKanan +=1
                    toggleKiriKanan %= 2
                    #waktu sleep harus dibuat seminimalnya
                    if toggleKiriKanan == 0:
                        Function.maju()
                        Function.time.sleep(6)
                    elif toggleKiriKanan == 1:
                        Function.mundur()
                        Function.time.sleep(6)


        cv2.line(hanyaObjek,(280,0),(280,480),(255,255,255), 1, cv2.LINE_4)
        cv2.line(hanyaObjek,(360,0),(360,480),(255,255,255), 1, cv2.LINE_4)
        cv2.imshow('hanyaobjek', hanyaObjek)
        cv2.imshow('layarhitam', layarHitam)
        # cv2.imshow('Frame5', binary_roi)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        if ijin==2: 
            break
    #robot sudah ditengah, mengembalikan nilai dari y dan jenis sampah
    cap.release()
    cv2.destroyAllWindows()
    return nilaiY, jenis


def cekKamera():
   #butuh fungsi saat 1 pun objek blum ditemukan
    cap = cv2.VideoCapture(-1)


    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        frame = cv2.flip(frame,1)
        if not ret:
            break
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    #robot sudah ditengah, mengembalikan nilai dari y dan jenis sampah
    cap.release()
    cv2.destroyAllWindows()


def cekDeteksi():
    cap = cv2.VideoCapture(-1)
    nilaiY = 0 
    toggleKiriKanan = 0 # 0 robot gerak ke kiri, 1 ke kanan
    ijin=0
    fps = 0
    frame_count = 0
    jenis = "1"
    start_time = Function.time.time()

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        frame = cv2.flip(frame,1)
        frame = cv2.flip(frame,0)
        if not ret:
            break
        frame_count+=1
        if Function.time.time() - start_time >= 1:
            fps = frame_count / (Function.time.time() - start_time)
            print("FPS:", fps)
            frame_count = 0
            start_time = Function.time.time()
        #menemukan contour meja
        # frame = cv2.imread('foto.jpg')
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
            mask = cv2.rectangle(layarHitam,(x,y+20),(x+w,y+20+h),(255,255,255),-1)
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
                        jenis = the_color(warna_hsv)
                        print(warna_hsv)
                        
                        cv2.putText(frame, jenis,(int(x+w/2),int(y+h/2)),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,255,255),1)
                        


            
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

def cariTempatSampah(jenis_sampah):
    #butuh fungsi saat 1 pun objek blum ditemukan
    cap = cv2.VideoCapture(-1)
    nilaiy = 0
    toggleKiriKanan = 0 # 0 robot gerak ke kiri, 1 ke kanan
    ijin=0
    fps = 0
    frame_count = 0
    jenis = "1"
    start_time = Function.time.time()

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        frame = cv2.flip(frame,1)
        frame = cv2.flip(frame,0)
        if not ret:
            break
        frame_count+=1
        if Function.time.time() - start_time >= 1:
            fps = frame_count / (Function.time.time() - start_time)
            print("FPS:", fps)
            frame_count = 0
            start_time = Function.time.time()
        #menemukan contour meja
        # frame = cv2.imread('foto.jpg')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        layarHitam = np.zeros_like(gray)
        # gray = cv2.GaussianBlur(gray, (21, 21), 0)
        _, binary = cv2.threshold(gray,60,255, cv2.THRESH_BINARY)  
        binary = cv2.bitwise_not(binary)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        
        if contours:
            #menggambar masking meja
            biggest_contour = max(contours, key = cv2.contourArea)
            print(cv2.contourArea(biggest_contour))
            mask = cv2.drawContours(layarHitam, [biggest_contour], 0,(255,255,255),-1)
            mask = cv2.bitwise_not(mask)
            selainMeja = cv2.bitwise_and(frame,frame,mask=mask)
            hsv = cv2.cvtColor(selainMeja, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([0, 98, 89])
            upper_bound = np.array([14, 159, 189])
            if jenis_sampah == "ferrro" :
                lower_bound = np.array([0, 98, 89])
                upper_bound = np.array([14, 159, 189])
            elif jenis_sampah == "plastik" :
                lower_bound = np.array([22, 110, 180])
                upper_bound = np.array([32, 198, 255])
            elif jenis_sampah == "kertas" :
                lower_bound = np.array([99, 147, 111])
                upper_bound = np.array([111, 198, 247])
            elif jenis_sampah == "daun" :
                lower_bound = np.array([31, 35, 99])
                upper_bound = np.array([59, 109, 219])
            elif jenis_sampah == "non ferro":
                lower_bound = np.array([31, 35, 99])
                upper_bound = np.array([59, 109, 219])
            # Threshold the HSV image to get only colors in the specified range
            maskHsv = cv2.inRange(hsv, lower_bound, upper_bound)
            tempatSampah = cv2.bitwise_and(frame, frame, mask=maskHsv)
            #mencari contour sampah2
            hanyaObjekGray = cv2.cvtColor(tempatSampah, cv2.COLOR_BGR2GRAY)
            _, binary_roi = cv2.threshold(hanyaObjekGray, 60, 255, cv2.THRESH_BINARY)
            contours_roi, _ = cv2.findContours(binary_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            biggest_contour1 = contours_roi
            if biggest_contour1:
                contourTempatSampah=max(biggest_contour1,key= cv2.contourArea)

                if [contourTempatSampah]:
                        x, y, w, h = cv2.boundingRect(contourTempatSampah)
                        cv2.circle(frame,(int(x+w/2),int(y+h/2)),5,(0,0,255),-1)
                        if x+w/2 < 280 :
                            print("mundur")
                            Function.mundur()
                            toggleKiriKanan = 1
                            print(y+h/2)
                            ijin = 0
                        elif x+w/2 > 320 :
                            print("maju")
                            Function.maju()  
                            toggleKiriKanan = 0
                            print(y+h/2)
                            ijin = 0
                        else:
                            print("sudah tengah")
                            Function.stop()
                            # ijin+=1
                            Function.time.sleep(0.5)
                            nilaiy = y+h/2
                            print(nilaiy)


            else:
                #saat ukuran meja masih begitu
                if cv2.contourArea(biggest_contour) > 83000:
                    if toggleKiriKanan == 0:
                        Function.maju()
                    elif toggleKiriKanan == 1:
                        Function.mundur()
                #saat dipinggir, ganti arah
                else :
                    Function.stop()
                    Function.time.sleep(2)
                    toggleKiriKanan +=1
                    toggleKiriKanan %= 2
                    #waktu sleep harus dibuat seminimalnya
                    if toggleKiriKanan == 0:
                        Function.maju()
                        Function.time.sleep(6)
                    elif toggleKiriKanan == 1:
                        Function.mundur()
                        Function.time.sleep(6)

        cv2.imshow('hanyaobjek', frame)
        cv2.imshow('layarhitam', layarHitam)
        cv2.imshow('tempatSampah', layarHitam)
        # cv2.imshow('Frame5', binary_roi)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        if ijin==2: 
            break
    #robot sudah ditengah, mengembalikan nilai dari y dan jenis sampah
    cap.release()
    cv2.destroyAllWindows()
    return nilaiy, jenis
 

