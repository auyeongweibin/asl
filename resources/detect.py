import cv2

def detect(model):
    while True:
        cap = cv2.VideoCapture(0)

        if not (cap.isOpened()):
            print("Could not open video device")
            break
            
        else:
            _, frame = cap.read()
            result = model(frame)
            prediction = result[0]
            
            boxes = prediction.boxes
            characters = prediction.names
            
            if len(boxes) > 0:
                box = boxes[0]
                x,y,w,h = box.xyxy[0].numpy()
                frame = cv2.rectangle(frame, (int(x), int(y)), (int(w), int(h)), (36,255,12), 1)
                cv2.putText(frame, f'Label: {characters[int(box.cls[0].numpy())]}', (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')