import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import pandas as pd
from datetime import datetime, timedelta
import pyodbc
import time
from speech_engine import SpeechEngine
from speech_engine_google import GTTSWrapper

# Konuşma kısmı
# speaker = SpeechEngine()
speaker = GTTSWrapper()

# Giriş ve çıkış için
entry_times = {}
exit_times = {}
durations = {}
last_seen_times = {}  # Öğrenci son görüldüğü zamanı takip etmek için

# Database
start_time = time.time()
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=CAPKAN\SQLEXPRESS;"
    "Database=StudentsFace;"
    "Trusted_Connection=yes;"
)
end_time = time.time()
print(f"[TIMER] Database connection established in {end_time - start_time:.4f} seconds")

# Webcam setup
start_time = time.time()
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 0)
end_time = time.time()
print(f"[TIMER] Webcam setup completed in {end_time - start_time:.4f} seconds")

start_time = time.time()
imgBackground = cv2.imread('Resources/background.jpg')
end_time = time.time()
print(f"[TIMER] Background image loaded in {end_time - start_time:.4f} seconds")

# Encoding
start_time = time.time()
try:
    with open('EncodeFile.p', 'rb') as file:
        encodeListKnownWithIDs = pickle.load(file)
    encodeListKnown, studentIds, names, majors ,photo_paths = encodeListKnownWithIDs
except Exception as e:
    print(f"[ERROR] Failed to load encoding file: {str(e)}")
    exit()

if len(encodeListKnown) == 0:
    print("[ERROR] No known encodings found in EncodeFile.p")
    exit()
#Varaible for face
detected_students = []
face_tracking = {}
distance_threshold = 0.40

frame_counter = 0
frame_time_total = 0
min_frame_time = float('inf')
max_frame_time = 0

while True:
    frame_start_time = time.time()

    capture_start = time.time()
    success, img = cap.read()
    if not success:
        print("[WARNING] Failed to capture frame from webcam")
        continue
    capture_time = time.time() - capture_start

    prep_start = time.time()
    imgSmall = cv2.resize(img, (0, 0), None, 0.5,+ 0.5)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
    prep_time = time.time() - prep_start

    # Yüz tanıma
    face_detect_start = time.time()
    faceCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurrentFrame)
    face_detect_time = time.time() - face_detect_start

    # Skip if no faces found
    if len(faceCurrentFrame) == 0:
        frame_time = time.time() - frame_start_time
        frame_time_total += frame_time
        frame_counter += 1
        min_frame_time = min(min_frame_time, frame_time)
        max_frame_time = max(max_frame_time, frame_time)

        cv2.imshow("Face Recognition Attendance", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    imgBackground[162:162 + 480, 55:55 + 640] = img

    current_time = datetime.now()
    detected_ids_in_frame = set()

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        match_start = time.time()
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        distance = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(distance)

        if distance[matchIndex] < distance_threshold:
            student_id = studentIds[matchIndex]
            detected_ids_in_frame.add(student_id)

            now = datetime.now()
            photo_path = photo_paths[matchIndex]
            photo_path = photo_paths[matchIndex]


            # İlk kez tanındıysa
            if student_id not in entry_times:
                entry_times[student_id] = now
                speaker.speak(f"Hoş geldin {names[matchIndex].split()[0]}")
            else:
                # Daha önce tanındı ve çıkış sayılacak
                last_seen = last_seen_times.get(student_id)
                if last_seen and (now - last_seen).total_seconds() > 10:  # 10 saniyeden fazla olduysa çıkış say
                    exit_times[student_id] = now
                    durations[student_id] = (exit_times[student_id] - entry_times[student_id]).total_seconds() / 3600
                    speaker.speak(f"Güle güle {names[matchIndex]}")

            last_seen_times[student_id] = now  # Her tanındığında güncelle

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = [coord * 2 for coord in (y1, x2, y2, x1)]
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0, colorR=(49, 14, 123), colorC=(49, 14, 123))

            cv2.putText(imgBackground, f"Name: {names[matchIndex]}", (bbox[0], bbox[1] - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (49, 14, 123), 2)
            cv2.putText(imgBackground, f"ID: {studentIds[matchIndex]}", (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (49, 14, 123), 2)

    for student_id in list(face_tracking.keys()):
        if student_id not in detected_ids_in_frame:
            del face_tracking[student_id]

    cv2.imshow("Face Recognition Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#   Yoklama
cap.release()
cv2.destroyAllWindows()
attendance_save_start = time.time()
attendance_data = []
for student_id, name in zip(studentIds, names):
    if student_id in entry_times and student_id in exit_times:
        duration = durations.get(student_id, 0)
        attendance_data.append({
            "Student ID": student_id,
            "Name": name,
            "Entry Time": entry_times[student_id].strftime("%H:%M:%S"),
            "Exit Time": exit_times[student_id].strftime("%H:%M:%S"),
            "Duration (hours)": round(duration, 2),
            "Attendance": "Tamamlandı"
        })
    elif student_id in entry_times:
        attendance_data.append({
            "Student ID": student_id,
            "Name": name,
            "Entry Time": entry_times[student_id].strftime("%H:%M:%S"),
            "Exit Time": "Yok",
            "Duration (hours)": 0,
            "Attendance": "Sadece Giriş"
        })
    else:
        attendance_data.append({
            "Student ID": student_id,
            "Name": name,
            "Entry Time": "Yok",
            "Exit Time": "Yok",
            "Duration (hours)": 0,  
            "Attendance": "Girmedi"
        })

attendance_df = pd.DataFrame(attendance_data)
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_file = f"Attendance_{current_datetime}.xlsx"

try:
    with pd.ExcelWriter(output_file) as writer:
        attendance_df.to_excel(writer, sheet_name="Attendance", index=False)
    print(f"[TIMER] Attendance saved to Excel in {time.time() - attendance_save_start:.4f} seconds")
except Exception as e:
    print(f"[ERROR] Failed to save attendance: {str(e)}")

print(f"Program completed. Attendance saved to {output_file}")