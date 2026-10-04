"""
train.py - Model training route
"""
import os
from flask import Blueprint, jsonify
from config import STUDENTS_DIR, MODEL_PATH
from backend.utils.face_utils import train_model_from_dir

train_bp = Blueprint("train", __name__)


@train_bp.route("/api/train", methods=["POST"])
def train_model():
    """Train the LBPH model on all registered student images."""
    try:
        if not os.path.exists(STUDENTS_DIR):
            return jsonify({"success": False, "error": "No students directory found"}), 400

        student_folders = [
            d for d in os.listdir(STUDENTS_DIR)
            if os.path.isdir(os.path.join(STUDENTS_DIR, d)) and "_" in d
        ]

        if not student_folders:
            return jsonify({
                "success": False,
                "error": "No registered students found. Please register students first."
            }), 400

        success, message, stats = train_model_from_dir(STUDENTS_DIR)
        if success:
            return jsonify({"success": True, "message": message, "stats": stats})
        return jsonify({"success": False, "error": message}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@train_bp.route("/api/train/status", methods=["GET"])
def train_status():
    """Check if model is trained."""
    trained = os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 100
    return jsonify({"success": True, "model_trained": trained})
