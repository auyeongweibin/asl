import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import time

def detect(model):
    words = ['SMUBIA', 'SCIS']
    current_word = 0
    current_letter = 0
    pTime = 0
    cTime = 0

    while True:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 60)
        segmentor = SelfiSegmentation()

        if not (cap.isOpened()):
            print("Could not open video device")
            break
            
        else:

            _, frame1 = cap.read()
            frame = segmentor.removeBG(frame1, (255,255,255), threshold=0.2)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(frame, f'FPS: {int(fps)}', (frame.shape[1] - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            result = model(frame)
            prediction = result[0]
            
            boxes = prediction.boxes
            characters = prediction.names
            
            if len(boxes) > 0:
                box = boxes[0]
                label = characters[int(box.cls[0].numpy())]
                if current_word != len(words) and label == words[current_word][current_letter]:
                    current_letter += 1
                    if current_letter == len(words[current_word]):
                        current_word += 1
                        current_letter = 0

                x,y,w,h = box.xyxy[0].numpy()
                frame = cv2.rectangle(frame, (int(x), int(y)), (int(w), int(h)), (36,255,12), 1)
                cv2.putText(frame, f'Label: {label}', (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            if current_word != len(words):
                cv2.putText(frame, f'Score: {current_word}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                cv2.putText(frame, f'Current Word: {words[current_word]}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                cv2.putText(frame, f'Current Letter: {words[current_word][current_letter]}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            else:
                cv2.putText(frame, f'Score: All Completed!', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')