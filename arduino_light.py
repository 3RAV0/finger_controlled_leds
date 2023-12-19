import cv2
import mediapipe as mp
import time
import serial

cap  = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingerCoordinates = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumCoordinate = (4, 2)
arduino_port = '/dev/cu.usbserial-1120'  
port = serial.Serial(arduino_port, 9600)
time.sleep(1)



while True:
    
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandMarks = results.multi_hand_landmarks 
    #print(multiLandMarks)

    if multiLandMarks:
        handPoints = []
        for handlms in multiLandMarks:
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

            for idx, lm in enumerate(handlms.landmark):
                #print(idx, lm) 
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handPoints.append((cx, cy))

        for point in handPoints:
            cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)

        upCount = 0
        for coordinate in fingerCoordinates:
            if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                upCount += 1
        
        if handPoints[thumCoordinate[0]][0] < handPoints[thumCoordinate[1]][0]:
            upCount += 1
        if upCount == 5:
            print("dcşklsmcşkdmcksc")
        if upCount == 1:
            veri = "a"
            port.write(b'a')
        elif upCount == 2:
            veri = "b"
            port.write(b'b')
        elif upCount == 3:
            veri = "c"
            port.write(b'c')
        elif upCount == 4:
            veri = "d"
            port.write(b'd')
        elif upCount == 5:
            veri = "e"
            port.write(b'e')
        elif upCount == 0:
            veri = "q"
            port.write(b'q')
        
        cv2.putText(img, str(upCount), (150, 150), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255), 5)

    cv2.imshow("FINGERS", img)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break
