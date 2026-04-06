import os
import urllib.request
import cv2
import numpy as np
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

MODEL_FILE_NAME = "hand_landmarker.task"
MODEL_DOWNLOAD_URL = "https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task"

try:
    import mediapipe as mp
except ImportError as exc:
    raise ImportError(
        "MediaPipe is not installed in the active environment. "
        "Install it with: python3 -m pip install mediapipe"
    ) from exc

use_mediapipe_solutions = hasattr(mp, "solutions")
landmarker = None
mp_image = None

if use_mediapipe_solutions:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
else:
    from mediapipe.tasks.python.vision import hand_landmarker as mp_hand_landmarker
    from mediapipe.tasks.python.vision.core import image as mp_image

    model_path = os.environ.get("HAND_LANDMARKER_MODEL_PATH", MODEL_FILE_NAME)
    if not os.path.exists(model_path):
        print(f"Downloading MediaPipe hand landmarker model to '{model_path}'...")
        urllib.request.urlretrieve(MODEL_DOWNLOAD_URL, model_path)

    landmarker = mp_hand_landmarker.HandLandmarker.create_from_model_path(model_path)

colors = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
]
color_names = ["RED", "GREEN", "BLUE", "YELLOW", "MAGENTA", "CYAN"]
colorIndex = 0

points = [[] for _ in range(len(colors))]

def create_ui(width, height):
    ui_height = height // 8
    ui = np.zeros((ui_height, width, 3), dtype=np.uint8)
    
    for y in range(ui_height):
        color = [int(240 * (1 - y / ui_height))] * 3
        cv2.line(ui, (0, y), (width, y), color, 1)
    
    button_width = min(50, width // (len(colors) + 2))
    for i, color in enumerate(colors):
        x = 10 + i * (button_width + 10)
        cv2.circle(ui, (x + button_width // 2, ui_height // 2), button_width // 2 - 5, color, -1)
        cv2.circle(ui, (x + button_width // 2, ui_height // 2), button_width // 2 - 5, (0, 0, 0), 2)
        cv2.putText(ui, color_names[i][:1], (x + button_width // 2 - 5, ui_height // 2 + 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    cv2.rectangle(ui, (width - 100, 10), (width - 10, ui_height - 10), (200, 200, 200), -1)
    cv2.rectangle(ui, (width - 100, 10), (width - 10, ui_height - 10), (0, 0, 0), 2)
    cv2.putText(ui, "CLEAR", (width - 90, ui_height // 2 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return ui

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

frame_width = 640  # Reduced resolution
frame_height = 480  # Reduced resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

ui = create_ui(frame_width, frame_height)
ui_height = ui.shape[0]
canvas = np.full((frame_height, frame_width, 3), 255, dtype=np.uint8)

def get_index_finger_tip(hand_landmarks):
    if use_mediapipe_solutions:
        return (
            int(hand_landmarks.landmark[8].x * frame_width),
            int(hand_landmarks.landmark[8].y * frame_height),
        )

    return (
        int(hand_landmarks[8].x * frame_width),
        int(hand_landmarks[8].y * frame_height),
    )


def is_index_finger_raised(hand_landmarks):
    if use_mediapipe_solutions:
        return hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y

    return hand_landmarks[8].y < hand_landmarks[6].y

prev_point = None
min_distance = 5
is_drawing = False
line_thickness = 2

running = True
prev_time = time.time()

while running:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if use_mediapipe_solutions:
        results = hands.process(rgb_frame)
        multi_hand_landmarks = results.multi_hand_landmarks
    else:
        mp_image_frame = mp_image.Image(mp_image.ImageFormat.SRGB, rgb_frame)
        detection_result = landmarker.detect(mp_image_frame)
        multi_hand_landmarks = detection_result.hand_landmarks

    if multi_hand_landmarks:
        for hand_landmarks in multi_hand_landmarks:
            index_finger_tip = get_index_finger_tip(hand_landmarks)
            
            if is_index_finger_raised(hand_landmarks):
                if index_finger_tip[1] <= ui_height:  # Toolbar area
                    if index_finger_tip[0] >= frame_width - 100:  # Clear button
                        for p in points:
                            p.clear()
                        canvas.fill(255)
                        prev_point = None
                        is_drawing = False
                    else:
                        for i, x in enumerate(range(10, 10 + len(colors) * 60, 60)):
                            if x <= index_finger_tip[0] <= x + 50:
                                colorIndex = i
                                break
                else:
                    if not is_drawing:
                        prev_point = index_finger_tip
                        is_drawing = True
                    
                    if prev_point and np.linalg.norm(np.array(index_finger_tip) - np.array(prev_point)) > min_distance:
                        cv2.line(canvas, prev_point, index_finger_tip, colors[colorIndex], line_thickness)
                        prev_point = index_finger_tip
            else:
                prev_point = None
                is_drawing = False

            cv2.circle(frame, index_finger_tip, 5, colors[colorIndex], -1)

    output = cv2.addWeighted(frame, 0.6, canvas, 0.4, 0)
    output[:ui_height, :] = ui

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(output, f"FPS: {int(fps)}", (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("air canvas", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        running = False
    elif key == ord('s'):
        cv2.imwrite("air_canvas_drawing.png", canvas)
        print("Drawing saved as 'air_canvas_drawing.png'")
    elif key == ord('+'):
        line_thickness = min(line_thickness + 1, 10)
    elif key == ord('-'):
        line_thickness = max(line_thickness - 1, 1)

cap.release()
if landmarker is not None:
    landmarker.close()
cv2.destroyAllWindows()