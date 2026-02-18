import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os
import time


MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model (~25MB), please wait...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )
    print("Download complete!")


HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),       
    (0,5),(5,6),(6,7),(7,8),      
    (5,9),(9,10),(10,11),(11,12),  
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)                          
]

def draw_landmarks_on_frame(frame, hand_landmarks_list):
    
    h, w, _ = frame.shape
    for hand_landmarks in hand_landmarks_list:
        # Get pixel coordinates for all 21 landmarks
        points = [
            (int(lm.x * w), int(lm.y * h))
            for lm in hand_landmarks
        ]
        # Draw skeleton connections (white lines)
        for start, end in HAND_CONNECTIONS:
            cv2.line(frame, points[start], points[end], (255, 255, 255), 2)
        # Draw landmark dots (green circles)
        for pt in points:
            cv2.circle(frame, pt, 5, (0, 255, 0), -1)


options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
detector = vision.HandLandmarker.create_from_options(options)


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not open webcam. Try VideoCapture(1) instead.")
    raise SystemExit(1)

print("Webcam opened! Press Q to quit.")
prev_time = 0


while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)

    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    
    result = detector.detect(mp_image)

    
    if result.hand_landmarks:
        draw_landmarks_on_frame(frame, result.hand_landmarks)

    
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
    prev_time = curr_time

    hand_count = len(result.hand_landmarks) if result.hand_landmarks else 0
    cv2.putText(frame, f"FPS: {int(fps)}",     (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    cv2.putText(frame, f"Hands: {hand_count}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.imshow("Hand Tracking  |  Press Q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
detector.close()
print("Done")