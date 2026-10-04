"""
attendance.py - Live attendance recognition routes
Known face (registered) → GREEN box → mark Present in CSV
Unknown face            → RED box  → "Unknown Face", NEVER create new user
"""
import os
import glob
import datetime
from flask import Blueprint, request, jsonify, send_file
from config import ATTENDANCE_DIR
from backend.utils.face_utils import (
    get_detector,
    get_recognizer,
    detect_faces,
    b64_to_gray,
    predict_face,
    compute_match_score,
    is_registered
)
from backend.utils.csv_utils import (
    mark_attendance,
    get_student_by_enrollment,
    get_all_subjects,
    get_attendance_report,
    get_today_attendance_records,
    sanitize_subject,
    delete_attendance_entry,
    clear_subject_attendance
)

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.route("/api/recognize", methods=["POST"])
def recognize_frame():
    """
    Recognize faces in a single camera frame.
    Returns face bounding boxes with recognition status.
    Known student (in CSV and confidence < threshold) -> GREEN box, mark Present.
    Unknown or low-confidence face                     -> RED box, NO user created, NO attendance.
    """
    data        = request.get_json() or {}
    image_b64   = data.get("image", "")
    raw_subject = data.get("subject", "General")
    subject     = sanitize_subject(raw_subject)
    should_mark = bool(data.get("mark", False))

    if not image_b64:
        return jsonify({"success": False, "error": "Image data missing"}), 400

    recognizer = get_recognizer()
    if recognizer is None:
        return jsonify({
            "success": False,
            "error":   "Model not trained yet. Go to Train Model tab first!"
        }), 400

    detector = get_detector()

    try:
        gray = b64_to_gray(image_b64)
        faces = detect_faces(gray, detector)
        results = []

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            pred_id, conf = predict_face(face_roi, recognizer)

            # Check both threshold AND verify student actually exists in registered CSV
            conf_ok = is_registered(conf)
            student = get_student_by_enrollment(pred_id) if (conf_ok and pred_id is not None) else None

            # CRITICAL: A face is ONLY matched if it passes confidence check AND exists in students.csv!
            if conf_ok and student is not None:
                matched        = True
                enrollment_str = str(student.get("Enrollment", pred_id))
                student_name   = student.get("Name", f"Student #{pred_id}")
            else:
                matched        = False
                enrollment_str = None
                student_name   = "Unknown Face"

            newly_marked = False
            if matched and should_mark and enrollment_str:
                ok, _ = mark_attendance(subject, enrollment_str, student_name)
                newly_marked = ok

            # High-accuracy match score (95% - 99.8% for verified student)
            match_score = compute_match_score(conf) if matched else 0.0

            results.append({
                "box":          [int(x), int(y), int(w), int(h)],
                "matched":      matched,
                "enrollment":   enrollment_str,
                "name":         student_name,
                "confidence":   match_score,
                "newly_marked": newly_marked
            })

        return jsonify({
            "success":    True,
            "face_count": len(faces),
            "results":    results
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@attendance_bp.route("/api/attendance/subjects", methods=["GET"])
def list_subjects():
    subjects = get_all_subjects()
    return jsonify({"success": True, "subjects": subjects})


@attendance_bp.route("/api/attendance/today", methods=["GET"])
def get_today_attendance():
    """Get list of students marked present today for a specific subject."""
    raw_subject = request.args.get("subject", "General")
    subject = sanitize_subject(raw_subject)
    records = get_today_attendance_records(subject)
    return jsonify({
        "success": True,
        "subject": subject,
        "date": datetime.date.today().isoformat(),
        "total": len(records),
        "records": records
    })


@attendance_bp.route("/api/attendance/<subject>", methods=["GET"])
def subject_attendance(subject):
    clean_subj = sanitize_subject(subject)
    records = get_attendance_report(clean_subj)
    return jsonify({
        "success": True,
        "subject": clean_subj,
        "total":   len(records),
        "records": records
    })


@attendance_bp.route("/api/attendance/download/<subject>", methods=["GET"])
def download_attendance(subject):
    clean_subj = sanitize_subject(subject)
    subj_dir   = os.path.join(ATTENDANCE_DIR, clean_subj)
    if not os.path.exists(subj_dir):
        return jsonify({"error": f"Subject '{clean_subj}' not found"}), 404
    files = glob.glob(os.path.join(subj_dir, "*.csv"))
    if not files:
        return jsonify({"error": f"No attendance files found for '{clean_subj}'"}), 404
    latest = max(files, key=os.path.getmtime)
    return send_file(
        latest,
        as_attachment=True,
        download_name=f"{clean_subj}_attendance.csv",
        mimetype="text/csv"
    )


@attendance_bp.route("/api/attendance/<subject>", methods=["DELETE"])
def remove_subject_attendance(subject):
    """
    Delete attendance records for a subject.
    Query parameters or JSON body:
      - enrollment: (optional) if specified, deletes this student's attendance.
      - date: (optional)
      - time: (optional)
    If no enrollment specified, clears all records for this subject (or given date).
    """
    clean_subj = sanitize_subject(subject)
    data = request.get_json(silent=True) or {}
    enrollment = request.args.get("enrollment") or data.get("enrollment")
    date_val   = request.args.get("date") or data.get("date")
    time_val   = request.args.get("time") or data.get("time")

    if enrollment:
        ok, msg = delete_attendance_entry(clean_subj, enrollment, date=date_val, time=time_val)
        return jsonify({"success": ok, "message": msg}), (200 if ok else 404)
    else:
        ok, msg = clear_subject_attendance(clean_subj, date=date_val)
        return jsonify({"success": ok, "message": msg})


@attendance_bp.route("/api/attendance/<subject>/<enrollment>", methods=["DELETE"])
def remove_student_attendance(subject, enrollment):
    """Delete a specific student's attendance from a subject."""
    clean_subj = sanitize_subject(subject)
    date_val   = request.args.get("date")
    time_val   = request.args.get("time")
    ok, msg = delete_attendance_entry(clean_subj, enrollment, date=date_val, time=time_val)
    return jsonify({"success": ok, "message": msg}), (200 if ok else 404)
