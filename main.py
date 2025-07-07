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
from PIL import Image, ImageDraw, ImageFont

# Ses için

speaker = GTTSWrapper()

# Giriş ve çıkış için
entry_times = {}
exit_times = {}
durations = {}
last_seen_times = {}  # Öğrenci son görüldüğü zamanı takip etmek için

# Database connection timer
start_time = time.time()
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=CAPKAN\SQLEXPRESS;"
    "Database=StudentsFace;"
    "Trusted_Connection=yes;"
)
end_time = time.time()
print(f"[TIMER] Database connection established in {end_time - start_time:.4f} seconds")

# Webcam setup timer
start_time = time.time()
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
end_time = time.time()
print(f"[TIMER] Webcam setup completed in {end_time - start_time:.4f} seconds")

start_time = time.time()
imgBackground = cv2.imread('Resources/background.jpg')
end_time = time.time()
print(f"[TIMER] Background image loaded in {end_time - start_time:.4f} seconds")

start_time = time.time()
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]
end_time = time.time()
print(f"[TIMER] Mode images loaded in {end_time - start_time:.4f} seconds (count: {len(imgModeList)})")

# Encoding file loading timer
start_time = time.time()
try:
    with open('EncodeFile.p', 'rb') as file:
        encodeListKnownWithIDs = pickle.load(file)
    encodeListKnown, studentIds, names, majors = encodeListKnownWithIDs
except Exception as e:
    print(f"[ERROR] Failed to load encoding file: {str(e)}")
    exit()

if len(encodeListKnown) == 0:
    print("[ERROR] No known encodings found in EncodeFile.p")
    exit()

# Initialize variables
detected_students = []
face_tracking = {}
distance_threshold = 0.45
is_student_info_displayed = False
current_student_id = None
current_student_info = None

def fetch_student_info(student_id):
    start_time = time.time()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Major, PhotoPath FROM Students "
                       "WHERE StudentID = ?", (student_id,))
        row = cursor.fetchone()
        elapsed = time.time() - start_time
        print(f"[TIMER] SQL query executed in {elapsed:.4f} seconds")

        if row:
            return {
                "name": row.Name,
                "major": row.Major,
                "photo_path": row.PhotoPath
            }
        return None
    except Exception as e:
        print(f"[ERROR] SQL query failed: {str(e)}")
        return None


def display_student_info(student_info, imgBackground):
    start_time = time.time()
    if student_info:
        # Öğrenci fotoğrafını yükle
        try:
            if os.path.exists(student_info["photo_path"]):
                imgStudent = cv2.imread(student_info["photo_path"])
                imgStudent = cv2.resize(imgStudent, (216, 216))
                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
        except Exception as e:
            print(f"[ERROR] Failed to load student image: {str(e)}")

        # 🔽 TÜRKÇE KARAKTERLERİ YAZAN KISIM BURADA HER ZAMAN ÇALIŞMALI
        # OpenCV to PIL
        img_pil = Image.fromarray(cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Türkçe karakterleri destekleyen font
        try:
            font_path = "arial.ttf"  # Windows'ta: C:/Windows/Fonts/arial.ttf
            font = ImageFont.truetype(font_path, 20)
        except IOError:
            print("[WARNING] 'arial.ttf' not found. Using default font.")
            font = ImageFont.load_default()

        # Yazı yaz
        draw.text((808, 445), f"Ad: {student_info['name']}", font=font, fill=(0, 0, 0))
        draw.text((808, 470), f"No: {current_student_id}", font=font, fill=(0, 0, 0))
        draw.text((808, 495), f"Bölüm: {student_info['major']}", font=font, fill=(0, 0, 0))

        # PIL'den tekrar OpenCV formatına çevir
        imgBackground[:, :] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    print(f"[TIMER] Total display_student_info took {time.time() - start_time:.4f} seconds")
frame_counter = 0
frame_time_total = 0
min_frame_time = float('inf')
max_frame_time = 0

while True:
    frame_start_time = time.time()

    # Frame capture timer
    capture_start = time.time()
    success, img = cap.read()
    if not success:
        print("[WARNING] Failed to capture frame from webcam")
        continue
    capture_time = time.time() - capture_start

    # Preprocessing timer
    prep_start = time.time()
    imgSmall = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
    prep_time = time.time() - prep_start

    # Face detection timer
    face_detect_start = time.time()
    faceCurrentFrame = face_recognition.face_locations(imgSmall)
    if frame_counter % 20 == 0:
        encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurrentFrame)
    face_detect_time = time.time() - face_detect_start

    # Skip if no faces found
    if len(faceCurrentFrame) == 0:
        if is_student_info_displayed:
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]
            is_student_info_displayed = False
            current_student_id = None
            current_student_info = None
        frame_time = time.time() - frame_start_time
        frame_time_total += frame_time
        frame_counter += 1
        min_frame_time = min(min_frame_time, frame_time)
        max_frame_time = max(max_frame_time, frame_time)

        cv2.imshow("Face Recognition Attendance", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Background update timer
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
            if not is_student_info_displayed or current_student_id != student_id:
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]
                current_student_info = fetch_student_info(student_id)
                current_student_id = student_id
                is_student_info_displayed = True
            # İlk kez tanındıysa
            if student_id not in entry_times:
                entry_times[student_id] = now

                speaker.speak(f"Hoşgeldin {names[matchIndex]}")
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

            # OpenCV görüntüsünü PIL formatına çevir
            img_pil = Image.fromarray(cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)

            try:
                font_path = "arial.ttf"  # Türkçe karakterleri destekleyen font yolu
                font = ImageFont.truetype(font_path, 20)
            except IOError:
                print("[WARNING] 'arial.ttf' not found. Using default font.")
                font = ImageFont.load_default()

            # Türkçe karakterleri destekleyen yazıları yaz
            draw.text((bbox[0], bbox[1] - 30), f"Ad: {names[matchIndex]}", font=font, fill=(49, 14, 123))
            draw.text((bbox[0], bbox[1] - 10), f"ID: {studentIds[matchIndex]}", font=font, fill=(49, 14, 123))

            # Tekrar OpenCV formatına çevir
            imgBackground = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    for student_id in list(face_tracking.keys()):
        if student_id not in detected_ids_in_frame:
            del face_tracking[student_id]

    if is_student_info_displayed and current_student_info:
        display_student_info(current_student_info, imgBackground)
    else:
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    cv2.imshow("Face Recognition Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

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
