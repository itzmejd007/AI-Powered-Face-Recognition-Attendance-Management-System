"""
stats.py - Dashboard stats route
"""
import os
from flask import Blueprint, jsonify
from config import MODEL_PATH, STUDENTS_DIR, CAPTURE_ANGLES, IMAGES_PER_ANGLE
from backend.utils.csv_utils import get_all_students, get_all_subjects

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/api/stats", methods=["GET"])
def get_stats():
    students    = get_all_students()
    subjects    = get_all_subjects()
    trained     = os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 100
    face_folders = 0
    if os.path.exists(STUDENTS_DIR):
        for folder in os.listdir(STUDENTS_DIR):
            if os.path.isdir(os.path.join(STUDENTS_DIR, folder)):
                face_folders += 1
    return jsonify({
        "success":          True,
        "students_count":   len(students),
        "face_folders":     face_folders,
        "subjects":         subjects,
        "model_trained":    trained,
        "angles":           CAPTURE_ANGLES,
        "images_per_angle": IMAGES_PER_ANGLE
    })
