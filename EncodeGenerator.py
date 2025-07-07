import cv2
import face_recognition
import pickle
import numpy as np
import pyodbc
import os

# Database
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=CAPKAN\SQLEXPRESS;"
    "Database=StudentsFace;"
    "Trusted_Connection=yes;"
)

# Database'den bilgi çekiyor
cursor = conn.cursor()
cursor.execute("SELECT StudentID, Name, Major, PhotoPath FROM Students")
rows = cursor.fetchall()

# debug
print("Fetched rows from the database:")
for row in rows:
    print(row)

studentIds = []
imgList = []
names = []
majors = []

for row in rows:
    studentIds.append(row.StudentID)
    names.append(row.Name)
    majors.append(row.Major)

    photo_path = row.PhotoPath
    if os.path.exists(photo_path):
        img = cv2.imread(photo_path)
        if img is not None:
            imgList.append(img)
            print(f"Loaded image for {row.Name} from {photo_path}")
        else:
            print(f"Warning: Could not load image from {photo_path}")
    else:
        print(f"Warning: File not found at {photo_path}")

# Encode
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if len(face_encodings) > 0:
            encode = face_encodings[0]
            encodeList.append(encode)
            print(f"Generated encoding for an image")
        else:
            print(f"Warning: No face found in an image")
    return encodeList

print("Encoding started")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDs = [encodeListKnown, studentIds, names, majors]
print("Encoding ended")

# Encode listesini kaydet
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIDs, file)
file.close()
print("File saved")

# Tekrar yükle
with open("EncodeFile.p", 'rb') as file:
    loaded_data = pickle.load(file)
file.close()

# Data print et
print("Loaded data from EncodeFile.p:")
print("Encodings:", len(loaded_data[0]))
print("Student IDs:", loaded_data[1])
print("Names:", loaded_data[2])
print("Majors:", loaded_data[3])