# Safety_Compliance_Detector - FINAL with Alarm Debugging
# A Computer Vision Project

import os
import cv2
import csv
import datetime
from ultralytics import YOLO
import numpy as np
from playsound import playsound
import time

# ========== CONFIG ==========
MODEL_PATH = 'runs/detect/train/weights/best.pt'
SAVE_DIR = 'output_images'
LOG_CSV = 'detection_log.csv'
ALARM_SOUND = 'alarm.wav'
USE_WEBCAM = True

# --- ALARM TIMING CONFIG ---
INITIAL_DELAY_SECONDS = 30
ALARM_DURATION_SECONDS = 10
REMINDER_INTERVAL_SECONDS = 20
REMINDER_WINDOW_SECONDS = 120
MAJOR_TIMEOUT_MINUTES = 30

os.makedirs(SAVE_DIR, exist_ok=True)
model = YOLO(MODEL_PATH)
danger_zone = np.array([[100, 200], [500, 200], [500, 480], [100, 480]], np.int32)
print("Setup complete. Starting detection...")

person_states = {}

with open(LOG_CSV, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Track_ID', 'Event'])

    cap = cv2.VideoCapture(0 if USE_WEBCAM else VIDEO_PATH)
    if not cap.isOpened():
        print("FATAL ERROR: Cannot open camera.")
    else:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            results = model.track(frame, persist=True, tracker="bytetrack.yaml")[0]
            detected_ids_in_frame = set()

            if results.boxes.id is not None:
                boxes = results.boxes.cpu().numpy()
                all_classes_in_frame = [model.names[int(c)] for c in results.boxes.cls]

                for box in boxes:
                    track_id = int(box.id[0])
                    detected_ids_in_frame.add(track_id)
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    
                    is_in_violation = False
                    if class_name == 'person':
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        is_inside = cv2.pointPolygonTest(danger_zone, (int((x1+x2)/2), y2), False) >= 0
                        has_gear = any(c in all_classes_in_frame for c in ['helmet', 'hardhat', 'vest'])
                        is_in_violation = is_inside and not has_gear

                    ### ALARM STATE MACHINE ###
                    current_time = time.time()
                    
                    if is_in_violation:
                        if track_id not in person_states:
                            person_states[track_id] = {'start_time': current_time, 'state': 'pending', 'last_alarm_time': 0}
                        
                        state_info = person_states[track_id]
                        violation_duration = current_time - state_info['start_time']
                        
                        # --- NEW: Print current state for debugging ---
                        print(f"[DEBUG] Person ID: {track_id}, State: {state_info['state']}, Violation Time: {violation_duration:.1f}s")
                        
                        # State: PENDING -> ALARMING
                        if state_info['state'] == 'pending' and violation_duration > INITIAL_DELAY_SECONDS:
                            state_info['state'] = 'alarming'
                            state_info['last_alarm_time'] = current_time
                            print(f"ALARM: Person {track_id} in violation for {INITIAL_DELAY_SECONDS}s.")
                            playsound(ALARM_SOUND, block=False)

                        # State: ALARMING -> REMINDING
                        elif state_info['state'] == 'alarming' and (current_time - state_info['last_alarm_time']) > ALARM_DURATION_SECONDS:
                            state_info['state'] = 'reminding'
                            print(f"INFO: Person {track_id} alarm period ended. Switching to reminders.")

                        # State: REMINDING -> TIMED_OUT
                        elif state_info['state'] == 'reminding' and violation_duration > (INITIAL_DELAY_SECONDS + REMINDER_WINDOW_SECONDS):
                            state_info['state'] = 'timed_out'
                            state_info['last_alarm_time'] = current_time
                            print(f"INFO: Person {track_id} reminder window expired. Alarm silenced.")
                        
                        # State: REMINDING (Trigger reminder)
                        elif state_info['state'] == 'reminding' and (current_time - state_info['last_alarm_time']) > REMINDER_INTERVAL_SECONDS:
                            state_info['last_alarm_time'] = current_time
                            print(f"REMINDER: Person {track_id} still in violation.")
                            playsound(ALARM_SOUND, block=False)

                        # State: TIMED_OUT (Trigger 30-min reminder)
                        elif state_info['state'] == 'timed_out' and (current_time - state_info['last_alarm_time']) > (MAJOR_TIMEOUT_MINUTES * 60):
                            state_info['last_alarm_time'] = current_time
                            print(f"LONG-TERM REMINDER: Person {track_id} still in violation after {MAJOR_TIMEOUT_MINUTES} mins.")
                            playsound(ALARM_SOUND, block=False)
                    else:
                        if track_id in person_states:
                            del person_states[track_id]

            for track_id in list(person_states.keys()):
                if track_id not in detected_ids_in_frame:
                    del person_states[track_id]

            cv2.imshow("Safety Compliance Detector", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()