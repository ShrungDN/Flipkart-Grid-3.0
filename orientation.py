import cv2
import math

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3, 1)
    cv2.putText(frame, 'Tracking', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)

def getOrientation(bbox, memo):
    prev_pos = memo.pop(0)
    current_pos = memo[-1]
    angle = math.atan2(current_pos[1]-prev_pos[1], current_pos[0]-prev_pos[0])
    return -180*angle/math.pi 



cap = cv2.VideoCapture('media/car.mp4')
# cap = cv2.VideoCapture('media/video1.mp4')
# cap = cv2.VideoCapture(0)


# tracker = cv2.TrackerMOSSE_create()
tracker = cv2.TrackerCSRT_create()

_, frame = cap.read()
frame_count = 1
bounding_box = cv2.selectROI('Tracking', frame, False)
tracker.init(frame, bounding_box)

memo = []
x, y, w, h = int(bounding_box[0]), int(bounding_box[1]), int(bounding_box[2]), int(bounding_box[3])
memo.append((x+w/2, y+h/2))

history = 2

while frame_count <= history + 1:
    _, frame = cap.read()
    success, bounding_box = tracker.update(frame)
    if success:
        x, y, w, h = int(bounding_box[0]), int(bounding_box[1]), int(bounding_box[2]), int(bounding_box[3])
        memo.append((x+w/2, y+h/2))
    else:
        cv2.putText(frame, 'Lost', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
    
    frame_count += 1

print(memo)

while cap.isOpened():
    timer = cv2.getTickCount()
    _, frame = cap.read()
    frame_count += 1
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)

    success, bounding_box = tracker.update(frame)

    if success:
        x, y, w, h = int(bounding_box[0]), int(bounding_box[1]), int(bounding_box[2]), int(bounding_box[3])
        memo.append((x+w/2, y+h/2))
        drawBox(frame, bounding_box)
        angle = getOrientation(bounding_box, memo)
        cv2.putText(frame, str(int(angle)), (20, 300), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)

    else:
        cv2.putText(frame, 'Lost', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
    
    # cv2.putText(frame, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
    cv2.putText(frame, str(int(frame_count)), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)

    cv2.imshow('Tracking', frame)
    
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break 