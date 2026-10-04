"""
app.py - Main Flask application entry point
Face Recognition Attendance System

Run from project root:
    python app.py
"""
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# Import blueprints
from backend.routes.register   import register_bp
from backend.routes.train      import train_bp
from backend.routes.attendance import attendance_bp
from backend.routes.stats      import stats_bp

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max request body for images
CORS(app, resources={r"/*": {"origins": "*"}})

# Register all API blueprints
app.register_blueprint(register_bp)
app.register_blueprint(train_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(stats_bp)


# ── Serve Frontend ──────────────────────────────────────────────────────
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """Serve static files or fall back to index.html."""
    full_path = os.path.join(FRONTEND_DIR, path)
    if path and os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, "index.html")


if __name__ == "__main__":
    print("=" * 55)
    print("  Face Recognition Attendance System")
    print("  Open: http://localhost:5000")
    print("=" * 55)
    # debug=False prevents auto-reloader from rebooting when images/CSVs are saved to data/
    app.run(host="0.0.0.0", port=5000, debug=False)
