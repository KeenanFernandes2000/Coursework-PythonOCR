import cv2
import pytesseract
import os
from gtts import gTTS
from playsound import playsound

cap = cv2.VideoCapture("http://192.168.3.192:8080/video")
cap.set(3, 640)
cap.set(4, 480)

def imgToSound():
    fileWrite = open("String.txt", "w")
    _, img = cap.read()
    boxes = pytesseract.image_to_data(img)
    for a, b in enumerate(boxes.splitlines()):
        if a != 0:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
                fileWrite.write(b[11] + " ")
    fileWrite.close()
    fileRead = open("String.txt", "r")
    language = 'en'
    line = fileRead.read()
    if(line != ""):
        fileRead.close()
        myobj = gTTS(text=line, lang=language, slow=False)
        myobj.save("welcome.mp3")
        os.system('mpg321 welcome.mp3 &')
        cv2.imshow("Result", img)
        while True:
            if cv2.waitKey(1) & 0xFF ==ord('q'):
                break
    else:
        print("NO IMAGE DETECTED\n")
    
def startVideoWord():
    while True:
        _, img = cap.read()
        boxes = pytesseract.image_to_data(img)
        for a, b in enumerate(boxes.splitlines()):
            if a != 0:
                b = b.split()
                if len(b) == 12:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
                    print(b[11])
        cv2.imshow("Result", img)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
        
def startVideoChar():
     while True:
         _, img = cap.read()
         hImg, wImg, _ = img.shape
         boxes = pytesseract.image_to_boxes(img)
         for b in boxes.splitlines():
             b = b.split(' ')
             x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
             cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
             cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
             print(b[0])
             cv2.imshow("Result", img)
             if cv2.waitKey(1) & 0xFF ==ord('q'):
                 break
        
while True:
    print("1: Image to Sound")
    print("2: Live OCR Words")
    print("3: Live OCR Characters")
    print("4: Break")
    userInput = input("Please Select an Option: ")
    if(userInput == "1"):
        print("The First frame from the camera will be converted to a sound\n")
        imgToSound()
    elif(userInput == "2"):
        print("The live stream from the camera will start\n")
        startVideoWord()
    elif(userInput == "3"):
        print("The live stream from the camera will start\n")
        startVideoChar()
    else:
        print("THANK YOU FOR USING THE OCR PROGRAM")
        break
        