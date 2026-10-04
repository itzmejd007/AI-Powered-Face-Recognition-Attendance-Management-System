"""
csv_utils.py - Student and attendance CSV helpers
"""
import os
import csv
import shutil
import datetime
import pandas as pd
from config import STUDENTS_CSV, ATTENDANCE_DIR, STUDENTS_DIR


# ──────────────────────────── STUDENTS CSV ────────────────────────────

def get_all_students():
    """Return list of student dicts from students.csv"""
    if not os.path.exists(STUDENTS_CSV):
        return []
    try:
        df = pd.read_csv(STUDENTS_CSV, dtype=str).dropna(how="all")
        df = df.fillna("")
        # Strip all column names and string cells
        df.columns = [c.strip() for c in df.columns]
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading students CSV: {e}")
        return []


def student_exists(enrollment):
    """Return True if enrollment already exists in CSV."""
    target = str(enrollment).strip()
    target_int = int(target) if target.isdigit() else None
    for s in get_all_students():
        curr = str(s.get("Enrollment", "")).strip()
        if curr == target:
            return True
        if target_int is not None and curr.isdigit() and int(curr) == target_int:
            return True
    return False


def save_student(enrollment, name, department="", email="", phone=""):
    """Append a student record to students.csv (if not already there)."""
    if student_exists(enrollment):
        return False, "Student already registered."
    with open(STUDENTS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            str(enrollment).strip(),
            str(name).strip(),
            str(department).strip(),
            str(email).strip(),
            str(phone).strip()
        ])
    return True, "Student saved to CSV."


def get_student_by_enrollment(enrollment):
    """Find one student dict by enrollment number."""
    target = str(enrollment).strip()
    target_int = int(target) if target.isdigit() else None
    for s in get_all_students():
        curr = str(s.get("Enrollment", "")).strip()
        if curr == target:
            return s
        if target_int is not None and curr.isdigit() and int(curr) == target_int:
            return s
    return None


def delete_student_record(enrollment):
    """
    Remove student from students.csv and delete their face folder.
    Returns (True, message) on success.
    """
    enroll_str = str(enrollment).strip()
    enroll_int = int(enroll_str) if enroll_str.isdigit() else None

    # 1. Remove from CSV
    if os.path.exists(STUDENTS_CSV):
        try:
            df = pd.read_csv(STUDENTS_CSV, dtype=str)
            df.columns = [c.strip() for c in df.columns]
            if "Enrollment" in df.columns:
                def is_match(val):
                    v = str(val).strip()
                    if v == enroll_str:
                        return True
                    if enroll_int is not None and v.isdigit() and int(v) == enroll_int:
                        return True
                    return False

                df = df[~df["Enrollment"].apply(is_match)]
                df.to_csv(STUDENTS_CSV, index=False)
        except Exception as e:
            print(f"Error updating students.csv: {e}")

    # 2. Delete student face folder in data/students
    if os.path.exists(STUDENTS_DIR):
        for fname in os.listdir(STUDENTS_DIR):
            fpath = os.path.join(STUDENTS_DIR, fname)
            if not os.path.isdir(fpath):
                continue
            parts = fname.split("_", 1)
            folder_enroll = parts[0].strip()
            if folder_enroll == enroll_str or (
                enroll_int is not None and folder_enroll.isdigit() and int(folder_enroll) == enroll_int
            ):
                shutil.rmtree(fpath, ignore_errors=True)

    return True, f"Student #{enroll_str} deleted successfully."


# ──────────────────────────── ATTENDANCE CSV ────────────────────────────

def sanitize_subject(subject):
    """Sanitize subject name to prevent path traversal."""
    s = "".join(c for c in str(subject).strip() if c.isalnum() or c in ("-", "_", " ")).strip()
    return s or "General"


def get_today_attendance_file(subject):
    """Get or create today's attendance CSV file for a subject."""
    subj = sanitize_subject(subject)
    subj_dir = os.path.join(ATTENDANCE_DIR, subj)
    os.makedirs(subj_dir, exist_ok=True)
    date_str = datetime.date.today().isoformat()
    file_path = os.path.join(subj_dir, f"{subj}_{date_str}.csv")
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["Enrollment", "Name", "Date", "Time", "Status"])
    return file_path


def mark_attendance(subject, enrollment, name):
    """
    Mark a student as present for today.
    Returns (True, msg) if newly marked, (False, msg) if already marked.
    """
    file_path = get_today_attendance_file(subject)
    enroll_str = str(enrollment).strip()
    try:
        df = pd.read_csv(file_path, dtype=str)
        if not df.empty and "Enrollment" in df.columns:
            existing_enrolls = set(df["Enrollment"].astype(str).str.strip().values)
            if enroll_str in existing_enrolls:
                return False, "Already marked present."
    except Exception:
        pass

    now = datetime.datetime.now()
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            enroll_str,
            str(name).strip(),
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            "Present"
        ])
    return True, "Marked present."


def get_today_attendance_records(subject):
    """Return all attendance records marked today for a specific subject."""
    subj = sanitize_subject(subject)
    file_path = get_today_attendance_file(subj)
    if not os.path.exists(file_path):
        return []
    try:
        df = pd.read_csv(file_path, dtype=str)
        df = df.fillna("")
        if df.empty or "Enrollment" not in df.columns:
            return []
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading today's attendance for {subj}: {e}")
        return []


def get_attendance_report(subject):
    """Return all attendance records for a subject as list of dicts."""
    subj = sanitize_subject(subject)
    subj_dir = os.path.join(ATTENDANCE_DIR, subj)
    if not os.path.exists(subj_dir):
        return []
    records = []
    for f in sorted(os.listdir(subj_dir), reverse=True):
        if f.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(subj_dir, f), dtype=str)
                df = df.fillna("")
                records.extend(df.to_dict(orient="records"))
            except Exception:
                continue
    return records


def get_all_subjects():
    """Return list of subject names (subdirs of attendance dir)."""
    if not os.path.exists(ATTENDANCE_DIR):
        return []
    return [
        d for d in sorted(os.listdir(ATTENDANCE_DIR))
        if os.path.isdir(os.path.join(ATTENDANCE_DIR, d))
    ]


def delete_attendance_entry(subject, enrollment, date=None, time=None):
    """
    Remove an attendance entry for a given subject and enrollment.
    Optionally matches specific date and/or time.
    Returns (True, message) on success.
    """
    subj = sanitize_subject(subject)
    subj_dir = os.path.join(ATTENDANCE_DIR, subj)
    if not os.path.exists(subj_dir):
        return False, f"Subject directory '{subj}' not found."

    enroll_str = str(enrollment).strip()
    enroll_int = int(enroll_str) if enroll_str.isdigit() else None
    deleted_any = False

    csv_files = [f for f in sorted(os.listdir(subj_dir)) if f.endswith(".csv")]
    if date:
        date_str = str(date).strip()
        exact_file = f"{subj}_{date_str}.csv"
        if exact_file in csv_files:
            csv_files = [exact_file]

    for fname in csv_files:
        fpath = os.path.join(subj_dir, fname)
        try:
            df = pd.read_csv(fpath, dtype=str)
            if df.empty or "Enrollment" not in df.columns:
                continue

            df.columns = [c.strip() for c in df.columns]

            def row_matches(row):
                r_enroll = str(row.get("Enrollment", "")).strip()
                enroll_matches = (r_enroll == enroll_str) or (
                    enroll_int is not None and r_enroll.isdigit() and int(r_enroll) == enroll_int
                )
                if not enroll_matches:
                    return False
                if date and str(row.get("Date", "")).strip() != str(date).strip():
                    return False
                if time and str(row.get("Time", "")).strip() != str(time).strip():
                    return False
                return True

            mask = df.apply(row_matches, axis=1)
            if mask.any():
                df = df[~mask]
                df.to_csv(fpath, index=False)
                deleted_any = True
        except Exception as e:
            print(f"Error deleting attendance in {fname}: {e}")

    if deleted_any:
        return True, f"Attendance record for #{enroll_str} deleted from '{subj}'."
    return False, f"Record for #{enroll_str} not found in '{subj}'."


def clear_subject_attendance(subject, date=None):
    """
    Clear attendance records for a subject.
    If date is given, clears that date's CSV.
    If date is None, clears all CSVs for that subject.
    Returns (True, message).
    """
    subj = sanitize_subject(subject)
    subj_dir = os.path.join(ATTENDANCE_DIR, subj)
    if not os.path.exists(subj_dir):
        return True, f"No attendance files found for '{subj}'."

    if date:
        fname = f"{subj}_{str(date).strip()}.csv"
        fpath = os.path.join(subj_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Enrollment", "Name", "Date", "Time", "Status"])
            return True, f"Cleared attendance records for {subj} on {date}."
        return True, f"No records found for date {date}."

    # Clear all CSVs in subject directory
    for f in os.listdir(subj_dir):
        if f.endswith(".csv"):
            try:
                os.remove(os.path.join(subj_dir, f))
            except Exception:
                pass
    return True, f"All attendance records for '{subj}' have been cleared."

