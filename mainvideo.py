import os
import pickle
import numpy as np
import cv2
import face_recognition
import pandas as pd
from datetime import datetime
import pyodbc

VIDEO_PATH = 'D:\\PycharmProjects\\facerecognition\\test3.mp4'
ENCODE_FILE = 'EncodeFile.p'
OUTPUT_DIR = '.'
FRAME_SKIP = 120 #burayı değiştirebiliriz
BACKGROUND_IMAGE = 'Resources/background2.jpg'

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=SILLYKITTY;"
    "Database=StudentsFace;"
    "Trusted_Connection=yes;"
)
print("[INFO] Database connection established.")

#Encode yüklenmesi
try:
    with open(ENCODE_FILE, 'rb') as file:
        encodeListKnownWithIDs = pickle.load(file)
    encodeListKnown, studentIds, names, majors = encodeListKnownWithIDs
except Exception as e:
    print(f"[ERROR] Failed to load encoding file: {str(e)}")
    exit()

if len(encodeListKnown) == 0:
    print("[ERROR] No known encodings found.")
    exit()

#Video ve arka plan
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"[ERROR] Cannot open video file: {VIDEO_PATH}")
    exit()

# Arkaplan yüklenmesi
imgBackground = cv2.imread(BACKGROUND_IMAGE)
if imgBackground is None:
    print(f"[ERROR] Cannot load background image: {BACKGROUND_IMAGE}")
    exit()

detected_students = []
face_tracking = {}
distance_threshold = 0.5

frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_count += 1
    if frame_count % FRAME_SKIP != 0:
        continue

    current_background = imgBackground.copy()

    # Resiz
    imgSmall = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    #Yüz tanıma
    face_locations = face_recognition.face_locations(imgSmall)
    face_encodings = face_recognition.face_encodings(imgSmall, face_locations)

    current_time = datetime.now()
    detected_ids_in_frame = set()

    for encodeFace, faceLoc in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        distance = face_recognition.face_distance(encodeListKnown, encodeFace)

        if len(distance) == 0:
            continue

        matchIndex = np.argmin(distance)

        if matches[matchIndex] and distance[matchIndex] < distance_threshold:
            student_id = studentIds[matchIndex]
            detected_ids_in_frame.add(student_id)

            if student_id in face_tracking:
                start_time, duration = face_tracking[student_id]
                face_tracking[student_id] = (start_time, (current_time - start_time).total_seconds())
            else:
                face_tracking[student_id] = (current_time, 0)

            if face_tracking[student_id][1] > 2 and student_id not in detected_students:
                print(f"[INFO] Marked present: {names[matchIndex]} (ID: {student_id})")
                detected_students.append(student_id)

            # Yüze kare çizilmesi
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{names[matchIndex]}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    # Video görüntüsünün resize edilmesi
    video_width = 960
    video_height = 540
    x_start = (1280 - video_width) // 2
    y_start = 120

    frame_resized = cv2.resize(frame, (video_width, video_height))

    frame_resized = cv2.resize(frame, (video_width, video_height))

    if y_start + video_height <= current_background.shape[0] and x_start + video_width <= current_background.shape[1]:
        current_background[y_start:y_start + video_height, x_start:x_start + video_width] = frame_resized
    else:
        print("[ERROR] Frame does not fit in the background image.")

    cv2.imshow("Face Recognition Attendance", current_background)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    for student_id in list(face_tracking.keys()):
        if student_id not in detected_ids_in_frame:
            del face_tracking[student_id]

cap.release()
cv2.destroyAllWindows()
print("[INFO] Video processing completed.")

#Yoklama
attendance_data = []
for student_id, name in zip(studentIds, names):
    attendance_data.append({
        "Student ID": student_id,
        "Name": name,
        "Attendance": "Girdi" if student_id in detected_students else "Girmedi"
    })

attendance_df = pd.DataFrame(attendance_data)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_file = os.path.join(OUTPUT_DIR, f"Attendance_{timestamp}.xlsx")

try:
    with pd.ExcelWriter(output_file) as writer:
        attendance_df.to_excel(writer, sheet_name="Attendance", index=False)
    print(f"[INFO] Attendance saved to: {output_file}")
except Exception as e:
    print(f"[ERROR] Failed to save attendance: {str(e)}")