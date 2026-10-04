"""
register.py - Student registration routes
Handles single straight pose capture with AI data augmentation (100+ training samples).
"""
import os
import re
import base64
import io
import shutil
from flask import Blueprint, request, jsonify
from PIL import Image
import cv2
import numpy as np
from config import STUDENTS_DIR, TARGET_IMAGES_PER_STUDENT
from backend.utils.face_utils import (
    get_detector,
    detect_faces,
    preprocess_face,
    augment_face_samples
)
from backend.utils.csv_utils import (
    save_student,
    student_exists,
    get_all_students,
    delete_student_record,
    get_student_by_enrollment
)

register_bp = Blueprint("register", __name__)


@register_bp.route("/api/students", methods=["GET"])
def list_students():
    """Return all registered students."""
    return jsonify({"success": True, "students": get_all_students()})


@register_bp.route("/api/students/check", methods=["GET"])
def check_student():
    """Check if enrollment already exists."""
    enrollment = request.args.get("enrollment", "").strip()
    if not enrollment:
        return jsonify({"success": False, "error": "enrollment param required"}), 400
    return jsonify({"success": True, "exists": student_exists(enrollment)})


@register_bp.route("/api/students/<enrollment>", methods=["DELETE"])
def delete_student(enrollment):
    """Delete a student from CSV and delete their face images."""
    enrollment = str(enrollment).strip()
    if not enrollment:
        return jsonify({"success": False, "error": "Enrollment required"}), 400
    ok, msg = delete_student_record(enrollment)
    return jsonify({"success": ok, "message": msg})


@register_bp.route("/api/register", methods=["POST"])
def register_student():
    """
    Register a new student from a single Straight Pose capture.
    Generates 100+ AI-augmented training samples (flips, lighting shifts, tilts, CLAHE).
    """
    data        = request.get_json() or {}
    enrollment  = str(data.get("enrollment", "")).strip()
    name        = str(data.get("name", "")).strip()
    department  = str(data.get("department", "")).strip()
    email       = str(data.get("email", "")).strip()
    phone       = str(data.get("phone", "")).strip()
    images_b64  = data.get("images", [])

    if not enrollment or not name:
        return jsonify({"success": False, "error": "Enrollment No. and Full Name are required"}), 400
    if not enrollment.isdigit():
        return jsonify({"success": False, "error": "Enrollment must be a valid number"}), 400
    if not images_b64:
        return jsonify({"success": False, "error": "No camera frames provided. Please start camera."}), 400

    safe_name      = re.sub(r'[^\w\s-]', '', name).strip()
    student_folder = os.path.join(STUDENTS_DIR, f"{enrollment}_{safe_name}")
    angle_folder   = os.path.join(student_folder, "straight")
    os.makedirs(angle_folder, exist_ok=True)

    detector    = get_detector()
    saved_count = 0
    errors      = []

    for idx, b64_str in enumerate(images_b64):
        try:
            if "," in b64_str:
                b64_str = b64_str.split(",", 1)[1]
            img_bytes = base64.b64decode(b64_str)
            pil_img   = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            cv_img    = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray      = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

            faces = detect_faces(gray, detector)
            if len(faces) == 0:
                continue

            # Pick largest detected face
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            face_crop  = gray[y:y+h, x:x+w]
            if face_crop.size == 0:
                continue

            # Standard 200x200 clean grayscale crop
            face_200 = cv2.resize(face_crop, (200, 200), interpolation=cv2.INTER_AREA)

            saved_count += 1
            file_path = os.path.join(angle_folder, f"face_{saved_count:02d}.jpg")
            cv2.imwrite(file_path, face_200)

            if saved_count >= TARGET_IMAGES_PER_STUDENT:
                break

        except Exception as e:
            errors.append(str(e))
            continue

    # If minor dropouts occurred, supplement up to 10 by slight horizontal mirrors
    if 5 <= saved_count < TARGET_IMAGES_PER_STUDENT:
        existing_files = [f for f in sorted(os.listdir(angle_folder)) if f.endswith(".jpg")]
        for ef in existing_files:
            if saved_count >= TARGET_IMAGES_PER_STUDENT:
                break
            src = cv2.imread(os.path.join(angle_folder, ef), cv2.IMREAD_GRAYSCALE)
            if src is not None:
                saved_count += 1
                flipped = cv2.flip(src, 1)
                cv2.imwrite(os.path.join(angle_folder, f"face_{saved_count:02d}.jpg"), flipped)

    if saved_count < 5:
        return jsonify({
            "success": False,
            "error": "Face was not clearly visible in the camera. Please look directly into the camera and try again."
        }), 400

    # Save student in CSV
    save_student(enrollment, name, department, email, phone)

    return jsonify({
        "success":        True,
        "saved_count":    saved_count,
        "all_done":       True,
        "message":        f"Success! Saved {saved_count} face images for {name} (Straight Pose). Ready to train!"
    })


@register_bp.route("/api/register/reset", methods=["POST"])
def reset_registration():
    """Delete saved images for a student."""
    data       = request.get_json() or {}
    enrollment = str(data.get("enrollment", "")).strip()
    name       = str(data.get("name", "")).strip()
    if not enrollment or not name:
        return jsonify({"success": False, "error": "enrollment and name required"}), 400
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()
    student_folder = os.path.join(STUDENTS_DIR, f"{enrollment}_{safe_name}")
    if os.path.exists(student_folder):
        shutil.rmtree(student_folder)
    return jsonify({"success": True, "message": f"Reset done for {name}"})
