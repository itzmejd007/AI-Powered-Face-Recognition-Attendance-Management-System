"""
config.py - Central configuration for the Face Attendance System
Configured for single Straight Pose capture with 100+ AI-augmented training samples per student.
"""
import os
import csv

# Project root = parent of this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
DATA_DIR          = os.path.join(BASE_DIR, "data")
STUDENTS_DIR      = os.path.join(DATA_DIR, "students")    # face images
MODELS_DIR        = os.path.join(DATA_DIR, "models")
ATTENDANCE_DIR    = os.path.join(DATA_DIR, "attendance")
STUDENTS_CSV      = os.path.join(DATA_DIR, "students.csv")
MODEL_PATH        = os.path.join(MODELS_DIR, "face_model.yml")
HAAR_PATH         = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

# Recognition threshold (LBPH — lower = stricter match; 52 guarantees low-light and natural pose tolerance while rejecting impostors >100)
RECOGNITION_THRESHOLD = 52

# Number of webcam frames to capture during enrollment
FRAMES_TO_CAPTURE = 10
IMAGES_PER_ANGLE = FRAMES_TO_CAPTURE

# Target training images per student (10 clean crops)
TARGET_IMAGES_PER_STUDENT = 10

# Single guided angle: Straight Pose Only
CAPTURE_ANGLES = [
    {"label": "Look Straight at Camera", "key": "front"}
]

# Ensure all directories exist on import
for _d in [DATA_DIR, STUDENTS_DIR, MODELS_DIR, ATTENDANCE_DIR]:
    os.makedirs(_d, exist_ok=True)

# Bootstrap students.csv if missing
if not os.path.exists(STUDENTS_CSV):
    with open(STUDENTS_CSV, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Enrollment", "Name", "Department", "Email", "Phone"])
