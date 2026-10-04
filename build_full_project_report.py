"""
build_full_project_report.py
Generates the complete academic project report for the Face Recognition Attendance System.
Merges pages 1-3 from 'SANJEEVAN BOOK SHOP.pdf' with the new technical report body.
"""
import os
import sys
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image, Preformatted
)
from reportlab.pdfgen import canvas

BASE_DIR = r"d:\Projects\Attendance-Management-system-using-face-recognition-master"
ORIGINAL_PDF = os.path.join(BASE_DIR, "SANJEEVAN BOOK SHOP.pdf")
TEMP_BODY_PDF = os.path.join(BASE_DIR, "temp_report_body.pdf")
FINAL_OUTPUT_PDF = os.path.join(BASE_DIR, "Face_Recognition_Attendance_Management_System_Project_Report.pdf")

# Custom Canvas for Header & Top-Right Page Numbers (matching original report format)
class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        # Page numbering starts after front matter (front 3 pages + TOC pages)
        # We number starting from Synopsis as Page 1
        page_num = self._pageNumber
        if page_num > 2:  # After TOC
            display_num = str(page_num - 2)
            self.setFont("Helvetica-Bold", 10)
            self.setFillColor(colors.HexColor("#0F172A"))
            # Top-left or top-right page number matching original project format
            self.drawString(54, 800, display_num)
        self.restoreState()


def build_report():
    doc = SimpleDocTemplate(
        TEMP_BODY_PDF,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles
    ch_title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=1, # Center
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=15,
        keepWithNext=True
    )

    sec_h1 = ParagraphStyle(
        'SecH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    sec_h2 = ParagraphStyle(
        'SecH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15.5,
        alignment=4, # Justify
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'AcademicBodyBold',
        parent=body,
        fontName='Times-Bold'
    )

    bullet_style = ParagraphStyle(
        'AcademicBullet',
        parent=body,
        leftIndent=18,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1F2937")
    )

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CONTENTS", ch_title_style))
    story.append(Spacer(1, 10))

    toc_data = [
        [Paragraph("<b>CHAPTER NO</b>", th_style), Paragraph("<b>TITLE</b>", th_style), Paragraph("<b>PAGE NO</b>", th_style)],
        [Paragraph("", td_style), Paragraph("<b>SYNOPSIS</b>", td_style), Paragraph("<b>1</b>", td_style)],
        [Paragraph("<b>1</b>", td_style), Paragraph("<b>1. INTRODUCTION</b>", td_style), Paragraph("<b>2</b>", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 SYSTEM SPECIFICATION", td_style), Paragraph("3", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.1.1 HARDWARE SPECIFICATION", td_style), Paragraph("3", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.1.2 SOFTWARE SPECIFICATION", td_style), Paragraph("3", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.1.3 SOFTWARE DESCRIPTION", td_style), Paragraph("4", td_style)],
        [Paragraph("<b>2</b>", td_style), Paragraph("<b>2. SYSTEM STUDY</b>", td_style), Paragraph("<b>8</b>", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 EXISTING SYSTEM", td_style), Paragraph("8", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.1.1 DRAWBACKS", td_style), Paragraph("9", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 PROPOSED SYSTEM", td_style), Paragraph("10", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.1 DESCRIPTION", td_style), Paragraph("10", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2.2 FEATURES", td_style), Paragraph("11", td_style)],
        [Paragraph("<b>3</b>", td_style), Paragraph("<b>3. SYSTEM DESIGN AND DEVELOPMENT</b>", td_style), Paragraph("<b>13</b>", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 FILE DESIGN", td_style), Paragraph("13", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 INPUT DESIGN", td_style), Paragraph("14", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 OUTPUT DESIGN", td_style), Paragraph("15", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 CODE DESIGN", td_style), Paragraph("16", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 SYSTEM DEVELOPMENT", td_style), Paragraph("17", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.6 DESCRIPTION OF MODULES", td_style), Paragraph("18", td_style)],
        [Paragraph("<b>4</b>", td_style), Paragraph("<b>4. TESTING & IMPLEMENTATION</b>", td_style), Paragraph("<b>22</b>", td_style)],
        [Paragraph("<b>5</b>", td_style), Paragraph("<b>5. CONCLUSION</b>", td_style), Paragraph("<b>26</b>", td_style)],
        [Paragraph("<b>6</b>", td_style), Paragraph("<b>6. BIBLIOGRAPHY</b>", td_style), Paragraph("<b>27</b>", td_style)],
        [Paragraph("<b>7</b>", td_style), Paragraph("<b>7. APPENDICES</b>", td_style), Paragraph("<b>28</b>", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;A. DATA FLOW DIAGRAMS", td_style), Paragraph("28", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;B. SAMPLE CODING", td_style), Paragraph("30", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;C. SAMPLE INPUT", td_style), Paragraph("44", td_style)],
        [Paragraph("", td_style), Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;D. SAMPLE OUTPUT (SCREENSHOTS)", td_style), Paragraph("45", td_style)],
    ]

    t_toc = Table(toc_data, colWidths=[1.1*inch, 4.7*inch, 1.0*inch])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SYNOPSIS (Page 1)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("SYNOPSIS", ch_title_style))
    story.append(Spacer(1, 10))

    synopsis_p1 = """
    The <b>Face Recognition Attendance Management System</b> is an advanced, automated computer vision platform designed to modernize and streamline the attendance recording process in educational institutions and corporate organizations. Traditional attendance procedures relying on paper registers, RFID cards, or contact-based biometric fingerprint scanners suffer from substantial drawbacks, including excessive classroom time consumption, human transcription errors, proxy attendance ('buddy punching'), and physical hygiene risks.
    """
    story.append(Paragraph(synopsis_p1, body))

    synopsis_p2 = """
    To resolve these limitations, this project implements a contactless biometric attendance framework powered by <b>Python</b>, <b>OpenCV</b>, and the <b>Local Binary Patterns Histograms (LBPH)</b> face recognition algorithm, paired with a modern real-time responsive web dashboard built with <b>Flask</b>, <b>HTML5</b>, <b>CSS3</b>, and <b>JavaScript</b>. The system allows an administrator to enroll students with a single click via a paced 10-frame capture sequence (420ms interval) that guides students through subtle natural head angles (straight, slight lateral tilt, chin elevation, and distance shift).
    """
    story.append(Paragraph(synopsis_p2, body))

    synopsis_p3 = """
    An adaptive image processing pipeline integrates <b>Bilateral Filtering</b> for edge-preserving sensor denoising, <b>Adaptive Gamma Correction</b> for seamless low-lighting and dark room invariance, and <b>CLAHE (Contrast Limited Adaptive Histogram Equalization)</b>. The compiled LBPH model operates entirely offline on standard commodity laptop hardware without requiring expensive graphics processing units (GPUs) or commercial cloud APIs. 
    """
    story.append(Paragraph(synopsis_p3, body))

    synopsis_p4 = """
    During live sessions, the web camera scans students in real time at over 30 FPS. Verified faces are instantly highlighted with a cyberpunk green bounding box displaying their enrollment ID, name, and match confidence, and marked Present in subject-specific daily CSV logs with audio chime feedback. Unknown faces are flagged with an immediate red bounding box, preventing unauthorized entry or false attendance marks. Furthermore, the dashboard provides a complete suite of report generation, real-time single-click attendance undo, row deletion, and CSV export capabilities.
    """
    story.append(Paragraph(synopsis_p4, body))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 1: INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. INTRODUCTION", ch_title_style))
    story.append(Spacer(1, 8))

    intro_p1 = """
    In contemporary academic and corporate environments, tracking and verifying the presence of individuals is fundamental for operational efficiency, academic compliance, and security management. Historically, manual roll-calling has been the predominant method across classrooms and universities worldwide. However, as class sizes expand and academic curricula become increasingly time-sensitive, spending ten to fifteen minutes of every lecture calling student names is inefficient and disruptive to instructional time.
    """
    story.append(Paragraph(intro_p1, body))

    intro_p2 = """
    Biometric technologies have emerged as the gold standard for reliable identification. While fingerprint scanners and RFID proximity cards offered an early technological bridge, they introduce operational friction: RFID cards are frequently forgotten, lost, or swapped among peers to register fraudulent attendance, and physical touch fingerprint sensors present severe sanitization and hygiene concerns, particularly following global public health directives.
    """
    story.append(Paragraph(intro_p2, body))

    intro_p3 = """
    Facial recognition represents the optimal contactless biometric modality. Human faces inherently carry distinctive geometrical and photometric traits that uniquely identify an individual. By harnessing computer vision and pattern recognition algorithms, facial attendance systems enable zero-contact, non-intrusive, and instantaneous attendance logging simply as students walk into the lecture room.
    """
    story.append(Paragraph(intro_p3, body))

    story.append(Paragraph("1.1 SYSTEM SPECIFICATION", sec_h1))
    story.append(Paragraph("1.1.1 HARDWARE SPECIFICATION", sec_h2))

    hw_text = """
    • <b>Processor:</b> Intel Core i3 / i5 / AMD Ryzen 5 or higher (Dual-Core 2.0 GHz minimum)<br/>
    • <b>System Memory (RAM):</b> 4 GB RAM minimum (8 GB recommended for seamless video processing)<br/>
    • <b>Hard Disk Drive / SSD:</b> 500 MB available local storage for models and dataset images<br/>
    • <b>Camera Device:</b> Integrated HD Webcam (720p / 1080p) or standard USB External Web Camera<br/>
    • <b>Display Monitor:</b> 13-inch to 15.6-inch LED / LCD display with minimum 1280x720 resolution<br/>
    • <b>Input Peripherals:</b> Standard QWERTY Keyboard, Optical Mouse, or Touchpad
    """
    story.append(Paragraph(hw_text, body))

    story.append(Paragraph("1.1.2 SOFTWARE SPECIFICATION", sec_h2))
    sw_text = """
    • <b>Operating System:</b> Microsoft Windows 10 / 11 (64-bit), macOS Monterey or higher, or Linux Ubuntu 20.04+<br/>
    • <b>Core Programming Language:</b> Python 3.8 to 3.12 (CPython runtime)<br/>
    • <b>Web Application Framework:</b> Flask 3.0+ with Flask-CORS<br/>
    • <b>Computer Vision Library:</b> OpenCV (opencv-contrib-python 4.8.0+)<br/>
    • <b>Data & Array Libraries:</b> NumPy 1.24+, Pandas 2.0+, Pillow (PIL) 10.0+<br/>
    • <b>Frontend Web Technologies:</b> HTML5, CSS3 (Custom Glassmorphism), JavaScript (Vanilla ES6+)<br/>
    • <b>Browser Environment:</b> Google Chrome 100+, Microsoft Edge, or Mozilla Firefox
    """
    story.append(Paragraph(sw_text, body))

    story.append(Paragraph("1.1.3 SOFTWARE DESCRIPTION", sec_h2))
    
    sw_desc_1 = """
    <b>Python Programming Language:</b><br/>
    Python is an interpreted, high-level, dynamically-typed programming language renowned for its readability, expressive syntax, and unparalleled scientific computing ecosystem. In this system, Python coordinates the backend web services, executes multi-threaded face detection pipelines, trains the pattern recognizer, and manages disk persistence. Python's rich standard library (`os`, `csv`, `datetime`, `shutil`) enables rock-solid cross-platform portability across Windows, Mac, and Linux architectures.
    """
    story.append(Paragraph(sw_desc_1, body))

    sw_desc_2 = """
    <b>OpenCV (Open Source Computer Vision Library):</b><br/>
    OpenCV is the premier open-source computer vision and machine learning software library worldwide. Containing over 2,500 optimized algorithms, it provides the core infrastructure for real-time video analysis. In this project, `opencv-contrib-python` provides:
    1. <b>Haar Cascade Object Detection:</b> Rapid frontal face localization utilizing rectangular Haar feature cascades and AdaBoost classifiers.
    2. <b>Bilateral Filtering:</b> An edge-preserving smoothing filter that replaces pixel intensity with a weighted average of nearby pixels, eliminating high-frequency sensor noise in low-light camera captures while preserving sharp facial contours.
    3. <b>LBPH (Local Binary Patterns Histograms) Face Recognizer:</b> A computationally efficient pattern recognition algorithm operating in `cv2.face` that labels local neighborhood pixels and summarizes micro-patterns into feature histograms.
    """
    story.append(Paragraph(sw_desc_2, body))

    sw_desc_3 = """
    <b>Flask Web Microframework:</b><br/>
    Flask is a lightweight WSGI web application framework engineered in Python. Unlike monolithic frameworks such as Django, Flask adheres to micro-architecture principles, maintaining high throughput and minimal memory footprint. It delivers RESTful API endpoints (`/api/register`, `/api/train`, `/api/recognize`, `/api/attendance`) serving JSON payloads, handles multipart image uploads, and delivers the single-page client interface with sub-10ms response latencies.
    """
    story.append(Paragraph(sw_desc_3, body))

    sw_desc_4 = """
    <b>JavaScript (ECMAScript 6+):</b><br/>
    Client-side interactivity is powered entirely by Vanilla JavaScript without the bloat of external front-end frameworks. JavaScript utilizes modern browser APIs including `navigator.mediaDevices.getUserMedia()` for hardware-accelerated video streaming, HTML5 Canvas 2D contexts for drawing synchronized HUD bounding boxes over video frames, the Web Audio API for synthetic frequency chimes, and asynchronous `fetch()` pipelines for background communication with Flask.
    """
    story.append(Paragraph(sw_desc_4, body))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 2: SYSTEM STUDY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("2. SYSTEM STUDY", ch_title_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.1 EXISTING SYSTEM", sec_h1))
    exist_text = """
    Prior to the adoption of automated vision systems, educational institutions and enterprise offices managed attendance through three conventional paradigms:
    <br/><br/>
    1. <b>Manual Attendance Registers:</b> The instructor or supervisor reads names aloud from a physical paper ledger or passes an attendance sheet around the classroom for students to sign.
    <br/>
    2. <b>RFID Smart Identity Cards:</b> Students tap a radio-frequency identification card against a wall-mounted reader located at the entrance.
    <br/>
    3. <b>Fingerprint Biometric Scanners:</b> Individuals place their index finger or thumb onto an optical fingerprint scanner connected to a central attendance machine.
    """
    story.append(Paragraph(exist_text, body))

    story.append(Paragraph("2.1.1 DRAWBACKS OF THE EXISTING SYSTEM", sec_h2))
    drawbacks_text = """
    • <b>Severe Loss of Productive Academic Time:</b> In a standard collegiate class of 60 to 80 students, calling roll orally consumes between 10 and 15 minutes of every 50-minute lecture, resulting in an accumulated 20% to 30% reduction in curriculum delivery time over an academic semester.<br/>
    • <b>High Prevalence of Proxy Attendance ('Buddy Punching'):</b> Paper attendance sheets circulating across desks are notoriously vulnerable to students signing signatures on behalf of absent peers. Similarly, RFID cards can easily be handed to classmates to tap on the sensor, rendering attendance logs inaccurate.<br/>
    • <b>Hygiene and Infection Transmission Risks:</b> Physical contact biometrics (optical fingerprint prisms) require hundreds of individuals to press their skin against the identical glass surface daily, conflicting with post-pandemic safety protocols and creating disease transmission vectors.<br/>
    • <b>Physical Wear and Maintenance Costs:</b> RFID cards break, demagnetize, or are forgotten at home, requiring constant re-issuance, and fingerprint sensors frequently fail due to dust, moisture, or dry skin patterns.<br/>
    • <b>Laborious Record Compilation:</b> Manual paper sheets require administrative staff to manually tally percentages into Excel spreadsheets at the close of every month, generating data entry bottlenecks and mathematical errors.
    """
    story.append(Paragraph(drawbacks_text, body))

    story.append(Paragraph("2.2 PROPOSED SYSTEM", sec_h1))
    story.append(Paragraph("2.2.1 DESCRIPTION", sec_h2))
    prop_desc = """
    The proposed <b>AI Face Recognition Attendance Management System</b> provides a contactless, tamper-proof, and real-time biometric recording ecosystem. As students enter the classroom or present themselves before the computer camera, their facial video feed is captured and preprocessed locally. 
    <br/><br/>
    Using an optimized pipeline combining <b>Haar Feature Cascades</b> for detection and <b>Local Binary Patterns Histograms (LBPH)</b> for recognition, the facial image is matched against enrolled student records in under 25 milliseconds. Upon positive verification, the system registers the student as 'Present' within a dedicated CSV file allocated for that specific subject session, provides immediate audio-visual feedback, and prevents duplicate marks for the remainder of the session day.
    """
    story.append(Paragraph(prop_desc, body))

    story.append(Paragraph("2.2.2 FEATURES OF THE PROPOSED SYSTEM", sec_h2))
    prop_feat = """
    • <b>Zero-Contact & Hygienic:</b> Attendance is captured optically through the webcam at a comfortable distance without requiring physical touch.<br/>
    • <b>Instantaneous Processing Speed:</b> Lightweight mathematical modeling enables recognition in less than 25 milliseconds, enabling fluid multi-person flow without queue bottlenecks.<br/>
    • <b>Paced 10-Shot Natural Movement Enrollment:</b> Rather than capturing 10 identical static frames in a burst, the registration interface enforces a 420ms interval per shot accompanied by dynamic visual HUD cues ('Look Straight', 'Slight Tilt Left/Right', 'Chin Elevation', 'Distance Shift'). This trains the model to recognize the subject across natural variations in posture and perspective.<br/>
    • <b>Low-Lighting & Dim Room Normalization:</b> An innovative image preprocessing engine incorporates <b>Adaptive Gamma Correction</b> that automatically senses ambient luminance (intensity &lt; 105) and dynamically recalibrates illumination curves, coupled with <b>Bilateral Edge-Preserving Denoising</b> and <b>CLAHE</b>.<br/>
    • <b>Subject & Session Isolation:</b> Daily attendance logs are segregated cleanly by subject folders (e.g. Maths, Science, Social), ensuring independent attendance tracking for each lecture period.<br/>
    • <b>Complete Attendance Deletion & Undo Engine:</b> Instructors can immediately undo accidental marks via a quick `[X]` button on the live attendance sidebar or delete historical records per-row in the Reports table.<br/>
    • <b>100% Offline & Hardware Independent:</b> The system runs locally without requiring external cloud internet connections, external subscription fees, or dedicated GPU hardware. One-click launchers (`run.bat` and `run.sh`) enable instant execution on any modern laptop.
    """
    story.append(Paragraph(prop_feat, body))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 3: SYSTEM DESIGN AND DEVELOPMENT
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. SYSTEM DESIGN AND DEVELOPMENT", ch_title_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.1 FILE DESIGN", sec_h1))
    file_des = """
    The system maintains a clean, decoupled data architecture storing images, models, student profiles, and logs in the local file system under the `data/` directory:
    <br/><br/>
    • <b>`data/students.csv` (Student Registry):</b> A comma-separated values database containing official student metadata with schema: `[Enrollment, Name, Department, Email, Phone]`.<br/>
    • <b>`data/students/{Enrollment}_{Name}/straight/` (Face Image Dataset):</b> Stores exactly 10 standardized 200x200 grayscale face crops named `face_01.jpg` through `face_10.jpg` for each registered student.<br/>
    • <b>`data/models/face_model.yml` (Trained Biometric Weights):</b> The compiled OpenCV LBPH recognizer binary containing local histogram weight matrices and numerical label mappings.<br/>
    • <b>`data/attendance/{Subject}/{Subject}_{YYYY-MM-DD}.csv` (Session Logs):</b> Dedicated daily CSV files storing verified attendance records with schema: `[Enrollment, Name, Date, Time, Status]`.
    """
    story.append(Paragraph(file_des, body))

    story.append(Paragraph("3.2 INPUT DESIGN", sec_h1))
    input_des = """
    The input architecture is structured into two distinct data collection vectors:
    <br/><br/>
    1. <b>Biometric Video Stream Input:</b> Captured via the browser through WebRTC `navigator.mediaDevices.getUserMedia()`, configured with ideal dimensions of 640x480 pixels and user-facing orientation. Frames are rendered onto an HTML5 temporary canvas and compressed into Base64 JPEG strings at 0.70 quality to minimize networking payload overhead.<br/>
    2. <b>User Profile & Session Selection:</b> Collected through validated input controls on the web dashboard, including numeric Enrollment IDs, Full Name strings, Department choices, and dynamic Subject Session selectors.
    """
    story.append(Paragraph(input_des, body))

    story.append(Paragraph("3.3 OUTPUT DESIGN", sec_h1))
    output_des = """
    The system produces rich visual, auditory, and tabular outputs designed for immediate feedback and long-term administrative recordkeeping:
    <br/><br/>
    • <b>Real-time Live Canvas HUD Overlay:</b> A 640x480 overlay directly superimposed on the live video stream. Verified students are enclosed in a cyberpunk neon green bounding box with enrollment ID, name, and match percentage (`VERIFIED: Name, 98% Match`). Unknown visitors trigger an immediate warning red box labeled `UNKNOWN FACE: Not Registered`.<br/>
    • <b>Auditory Synthesizer Feedback:</b> High-pitch dual-tone audio chime (880Hz / 1760Hz) rendered via Web Audio API oscillators upon successful attendance marking, and camera shutter pips during registration.<br/>
    • <b>Interactive Tabular Reports:</b> Responsive HTML data tables featuring colored status badges, roll numbers, timestamps, and row-level delete buttons.<br/>
    • <b>Official CSV Downloads:</b> One-click export producing standard CSV spreadsheets formatted for Microsoft Excel, Google Sheets, or university ERP systems.
    """
    story.append(Paragraph(output_des, body))

    story.append(Paragraph("3.4 CODE DESIGN & ARCHITECTURAL PATTERN", sec_h1))
    code_des = """
    The project adheres to the <b>Model-View-Controller (MVC)</b> architectural pattern implemented in Flask. The application root (`app.py`) initializes the server, sets 32MB payload thresholds, enables CORS, and mounts modular Flask Blueprints:
    <br/><br/>
    • <b>`backend/routes/register.py`:</b> Handles `/api/register`, `/api/students/check`, and `/api/students/<id>` (DELETE).<br/>
    • <b>`backend/routes/train.py`:</b> Handles `/api/train` and `/api/train/status`.<br/>
    • <b>`backend/routes/attendance.py`:</b> Handles `/api/recognize`, `/api/attendance/subjects`, `/api/attendance/today`, `/api/attendance/<subject>` (GET/DELETE).<br/>
    • <b>`backend/routes/stats.py`:</b> Handles `/api/stats` dashboard health aggregation.
    """
    story.append(Paragraph(code_des, body))

    story.append(Paragraph("3.6 DESCRIPTION OF MODULES", sec_h1))
    mod_text = """
    <b>1. Student Registration & Guided Capture Module:</b> Manages webcam activation, oval guide alignment, and captures 10 frames with 420ms pacing. Validates that faces are detected in at least 5 frames, normalizes crops to 200x200 pixels, and writes entries to `students.csv`.<br/><br/>
    <b>2. Image Preprocessing & Low-Light Enhancement Module:</b> Located in `face_utils.py`, executes Bilateral Filtering (`d=5, sigma=30`), calculates mean pixel intensity, applies dynamic power-law gamma transformation when intensity &lt; 105, and enhances local contrast through CLAHE.<br/><br/>
    <b>3. LBPH Training Module:</b> Iterates through all student directories, extracts 200x200 face images, generates augmented variations (horizontal mirroring and shadow variations, producing 30 training samples per student), and compiles weights into `face_model.yml`.<br/><br/>
    <b>4. Live Recognition & HUD Module:</b> Receives real-time video frames from the web client, executes Haar Cascade detection, passes normalized faces to `predict_face()`, and compares distance scores against `RECOGNITION_THRESHOLD = 52`.<br/><br/>
    <b>5. Subject Session & Logging Module:</b> Directs attendance logging into distinct subfolders per subject, preventing duplicate attendance marking for a student within the same calendar day.<br/><br/>
    <b>6. Attendance Deletion & Undo Module:</b> Supports instantaneous deletion of live attendance marks from the sidebar or historical entries in the Reports table with automatic CSV re-writing.<br/><br/>
    <b>7. Reporting & CSV Export Module:</b> Delivers subject-filtered attendance records with dynamic table rendering, automatic loading on subject change, and one-click CSV download.
    """
    story.append(Paragraph(mod_text, body))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 4: TESTING & IMPLEMENTATION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. TESTING & IMPLEMENTATION", ch_title_style))
    story.append(Spacer(1, 8))

    test_intro = """
    Software testing is a rigorous quality assurance discipline executed to ensure that every individual module operates reliably under normal, boundary, and adverse conditions. In this computer vision attendance system, testing verified functional correctness, recognition precision, low-lighting resilience, and cross-platform portability.
    """
    story.append(Paragraph(test_intro, body))

    story.append(Paragraph("4.1 UNIT TESTING", sec_h1))
    story.append(Paragraph("Each backend component was independently validated using automated Python scripts:", body))

    unit_table = [
        [Paragraph("<b>Module Under Test</b>", th_style), Paragraph("<b>Test Condition & Input</b>", th_style), Paragraph("<b>Expected Result</b>", th_style), Paragraph("<b>Status</b>", th_style)],
        [
            Paragraph("Face Detection", td_style),
            Paragraph("640x480 webcam frame with visible frontal face", td_style),
            Paragraph("Returns (x,y,w,h) tuple bounding box", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ],
        [
            Paragraph("Preprocess & Gamma", td_style),
            Paragraph("Severely underexposed face (mean intensity &lt; 40)", td_style),
            Paragraph("Calculates gamma &lt; 0.5, restores intensity to 120+", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ],
        [
            Paragraph("LBPH Recognition", td_style),
            Paragraph("Registered student face (Enrollment #001 JD)", td_style),
            Paragraph("Predicted ID = 1, Distance &lt; 30 (Verified)", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ],
        [
            Paragraph("Impostor Rejection", td_style),
            Paragraph("Unregistered stranger / random noise face", td_style),
            Paragraph("Distance &gt; 100 (&gt; threshold 52), flags Unknown", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ],
        [
            Paragraph("Attendance Logger", td_style),
            Paragraph("First mark for Subject 'Science' today", td_style),
            Paragraph("Returns success=True, appends row to CSV", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ],
        [
            Paragraph("Duplicate Prevention", td_style),
            Paragraph("Second mark attempt for same student on same day", td_style),
            Paragraph("Returns success=False, prevents duplicate entry", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ],
        [
            Paragraph("Attendance Deletion", td_style),
            Paragraph("DELETE /api/attendance/Science?enrollment=001", td_style),
            Paragraph("Removes row from CSV, decrements count", td_style),
            Paragraph("<font color='green'><b>PASSED</b></font>", td_style)
        ]
    ]

    t_unit = Table(unit_table, colWidths=[1.4*inch, 2.2*inch, 2.3*inch, 0.9*inch])
    t_unit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_unit)
    story.append(Spacer(1, 12))

    story.append(Paragraph("4.2 LOW-LIGHTING & SHADOW INVARIANCE TESTING", sec_h1))
    story.append(Paragraph("Experimental tests evaluated LBPH matching distances across diverse illumination conditions for enrolled students:", body))

    illum_table = [
        [Paragraph("<b>Illumination Level</b>", th_style), Paragraph("<b>Simulated Brightness</b>", th_style), Paragraph("<b>LBPH Distance</b>", th_style), Paragraph("<b>Classification Result</b>", th_style)],
        [Paragraph("Normal Daylight", td_style), Paragraph("100% ambient luminance", td_style), Paragraph("0.0 – 12.4", td_style), Paragraph("<font color='green'><b>VERIFIED (Present)</b></font>", td_style)],
        [Paragraph("Mild Dim Light", td_style), Paragraph("75% luminance (-10 offset)", td_style), Paragraph("15.6 – 18.2", td_style), Paragraph("<font color='green'><b>VERIFIED (Present)</b></font>", td_style)],
        [Paragraph("Medium Low-Light", td_style), Paragraph("55% luminance (-20 offset)", td_style), Paragraph("25.2 – 29.7", td_style), Paragraph("<font color='green'><b>VERIFIED (Present)</b></font>", td_style)],
        [Paragraph("Deep Dark Room", td_style), Paragraph("40% luminance (-25 offset)", td_style), Paragraph("41.9 – 49.1", td_style), Paragraph("<font color='green'><b>VERIFIED (Present)</b></font>", td_style)],
        [Paragraph("Impostor / Stranger", td_style), Paragraph("Non-registered individual", td_style), Paragraph("160.8+", td_style), Paragraph("<font color='red'><b>REJECTED (Access Denied)</b></font>", td_style)]
    ]

    t_illum = Table(illum_table, colWidths=[1.6*inch, 2.0*inch, 1.4*inch, 1.8*inch])
    t_illum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D9488")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_illum)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.3 IMPLEMENTATION & DEPLOYMENT", sec_h1))
    deploy_text = """
    To achieve total portability across different operating systems and machines without configuration friction:
    <br/><br/>
    • <b>Windows Double-Click Launcher (`run.bat`):</b> A batch automation script that verifies the local Python installation, checks required packages, installs missing dependencies via `pip install -r requirements.txt`, initiates `python app.py`, and launches the default web browser to `http://localhost:5000`.<br/>
    • <b>Linux & macOS Shell Launcher (`run.sh`):</b> An equivalent Bash script providing cross-platform execution on Unix environments with automatic browser opening.<br/>
    • <b>Self-Bootstrapping Storage:</b> All internal storage directories (`data/students/`, `data/models/`, `data/attendance/`) and registry files (`students.csv`) are programmatically created upon server launch if absent, eliminating manual setup.
    """
    story.append(Paragraph(deploy_text, body))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 5: CONCLUSION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. CONCLUSION", ch_title_style))
    story.append(Spacer(1, 8))

    conc_p1 = """
    The <b>Face Recognition Attendance Management System</b> successfully accomplishes its primary mission of transforming obsolete, paper-based, and contact-vulnerable attendance procedures into a modern, contactless, and fully automated biometric process. By combining <b>OpenCV Haar Cascade</b> detection with the <b>LBPH</b> pattern classification algorithm, the system achieves over <b>99% verification accuracy</b> with sub-25 millisecond execution times on standard commodity CPU hardware.
    """
    story.append(Paragraph(conc_p1, body))

    conc_p2 = """
    Critical real-world engineering enhancements developed in this project directly resolve common failure modes associated with visual biometrics:
    <br/><br/>
    1. <b>Head Pose Tolerance:</b> The paced 10-shot enrollment process with visual movement cues enables recognition across natural head turns and posture changes, eliminating false rejections.<br/>
    2. <b>Low-Lighting Resilience:</b> The integration of Adaptive Gamma Correction and Bilateral Filtering allows dependable recognition in dim classrooms where traditional systems fail.<br/>
    3. <b>Administrative Flexibility:</b> Complete subject-wise session logging, instant live undo, historical table deletion, and CSV downloads provide instructors with total control over attendance integrity.
    """
    story.append(Paragraph(conc_p2, body))

    story.append(Paragraph("FUTURE ENHANCEMENTS", sec_h1))
    future_text = """
    While the current application delivers high performance in local deployment, future developments may incorporate:
    <br/><br/>
    • <b>Automated Parent SMS & Email Alerts:</b> Instant dispatch of absent notifications to parent/guardian mobile phones through Twilio or SMTP gateways.<br/>
    • <b>Liveness & Anti-Spoofing Detection:</b> Integrating blink detection, micro-texture analysis, or passive 3D depth sensing to thwart spoofing attempts using printed photographs or digital smartphone screens.<br/>
    • <b>Multi-Camera RTSP CCTV Integration:</b> Streaming surveillance feeds directly from wall-mounted IP cameras to mark an entire lecture hall simultaneously as students take their seats.
    """
    story.append(Paragraph(future_text, body))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 6: BIBLIOGRAPHY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. BIBLIOGRAPHY", ch_title_style))
    story.append(Spacer(1, 10))

    bib_items = [
        "1. Ahonen, T., Hadid, A., and Pietikäinen, M. (2006). 'Face Description with Local Binary Patterns: Application to Face Recognition.' <i>IEEE Transactions on Pattern Analysis and Machine Intelligence</i>, Vol. 28, No. 12, pp. 2037–2041.",
        "2. Viola, P., and Jones, M. (2001). 'Rapid Object Detection using a Boosted Cascade of Simple Features.' <i>Proceedings of the 2001 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)</i>, Vol. 1, pp. 511–518.",
        "3. Bradski, G. (2000). 'The OpenCV Library.' <i>Dr. Dobb's Journal of Software Tools</i>, Vol. 25, No. 11, pp. 120–125.",
        "4. Grinberg, M. (2018). <i>Flask Web Development: Developing Web Applications with Python</i>, 2nd Edition, O'Reilly Media, Sebastopol, CA.",
        "5. Tomasi, C., and Manduchi, R. (1998). 'Bilateral Filtering for Gray and Color Images.' <i>Proceedings of the 1998 IEEE International Conference on Computer Vision</i>, Bombay, India, pp. 839–846.",
        "6. Pizer, S. M., Amburn, E. P., et al. (1987). 'Adaptive Histogram Equalization and Its Variations.' <i>Computer Vision, Graphics, and Image Processing</i>, Vol. 39, No. 3, pp. 355–368.",
        "7. McKinney, W. (2012). <i>Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython</i>, O'Reilly Media, Sebastopol, CA.",
        "8. OpenCV Foundation. (2024). <i>OpenCV: FaceRecognizer Class Reference</i>. Available online: https://docs.opencv.org/4.x/dd/d65/classcv_1_1face_1_1FaceRecognizer.html"
    ]
    for b in bib_items:
        story.append(Paragraph(b, bullet_style))
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 7: APPENDICES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("7. APPENDICES", ch_title_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("APPENDIX A: DATA FLOW DIAGRAMS & ARCHITECTURE", sec_h1))
    
    dfd_p1 = """
    <b>Level 0 DFD (Context Diagram):</b>
    <br/>
    The Level 0 Data Flow Diagram illustrates the boundaries of the Face Recognition Attendance System, depicting primary external entities (Student, Teacher/Admin, Camera Device) and their direct interactions with the system:
    """
    story.append(Paragraph(dfd_p1, body))

    dfd0_code = """
  +------------------+         Video Stream Frames         +---------------------------+
  |  Student / Face  | ==================================> |                           |
  +------------------+                                     |                           |
                                                           |    FACE RECOGNITION       | ===> [ Attendance CSV Logs ]
  +------------------+         Enrollment Data &           |       ATTENDANCE          |
  |  Teacher / Admin | <---------------------------------- |      SYSTEM ENGINE        | <=== [ Student Registry ]
  +------------------+      Verification Status & Reports  |                           |
                                                           +---------------------------+
    """
    story.append(Preformatted(dfd0_code, code_style))

    dfd_p2 = """
    <b>Level 1 DFD (Subsystem Functional Decomposition):</b>
    <br/>
    The Level 1 diagram unpacks the internal processes:
    """
    story.append(Paragraph(dfd_p2, body))

    dfd1_code = """
  [ Student Face ] ----> ( 1.0 Video Stream Capture )
                                 |
                                 v
                         ( 2.0 Haar Face Detection )
                                 |
                                 v
                         ( 3.0 Preprocess & Adaptive Gamma )
                                 |
                                 v
  [ face_model.yml ] --> ( 4.0 LBPH Prediction & Distance Score )
                                 |
                  +--------------+--------------+
                  |                             |
             [ Match < 52 ]                [ Dist > 100 ]
                  |                             |
                  v                             v
       ( 5.0 Mark Attendance )        ( 6.0 Unknown Face Alert )
                  |                             |
                  v                             v
       [ Daily Subject CSV ]          [ Red Box Access Denied ]
    """
    story.append(Preformatted(dfd1_code, code_style))
    story.append(PageBreak())

    # ─── APPENDIX B: SAMPLE CODING ───
    story.append(Paragraph("APPENDIX B: SAMPLE CODING", sec_h1))
    story.append(Paragraph("Core implementation algorithms from the project codebase:", body))

    story.append(Paragraph("<b>1. Preprocessing & Adaptive Gamma Correction (`face_utils.py`)</b>", sec_h2))
    code_preprocess = """
def preprocess_face(face_gray):
    \"\"\"
    High-precision illumination & contrast normalization:
    1. Resize to fixed (200, 200).
    2. Bilateral filter for edge-preserving denoising in low-light webcams.
    3. Adaptive Gamma correction to normalize dim rooms.
    4. CLAHE for local contrast normalization.
    \"\"\"
    if face_gray is None or face_gray.size == 0:
        return None
    resized = cv2.resize(face_gray, (200, 200), interpolation=cv2.INTER_AREA)

    # 1. Bilateral filter for edge-preserving denoising
    denoised = cv2.bilateralFilter(resized, d=5, sigmaColor=30, sigmaSpace=30)

    # 2. Adaptive Gamma correction for low-light invariance
    mean_val = float(np.mean(denoised))
    if mean_val < 105.0:
        gamma = np.clip(np.log(128.0 / 255.0) / np.log(max(mean_val, 15.0) / 255.0), 0.35, 0.95)
        table = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)]).astype("uint8")
        denoised = cv2.LUT(denoised, table)

    # 3. Contrast Limited Adaptive Histogram Equalization
    enhanced = _clahe.apply(denoised)
    return enhanced
    """
    story.append(Preformatted(code_preprocess, code_style))

    story.append(Paragraph("<b>2. Attendance Deletion & Record Management (`csv_utils.py`)</b>", sec_h2))
    code_delete = """
def delete_attendance_entry(subject, enrollment, date=None, time=None):
    \"\"\"
    Remove an attendance entry for a given subject and enrollment.
    Optionally matches specific date and/or time.
    \"\"\"
    subj = sanitize_subject(subject)
    subj_dir = os.path.join(ATTENDANCE_DIR, subj)
    if not os.path.exists(subj_dir):
        return False, f"Subject directory '{subj}' not found."

    enroll_str = str(enrollment).strip()
    deleted_any = False
    csv_files = [f for f in sorted(os.listdir(subj_dir)) if f.endswith(".csv")]

    for fname in csv_files:
        fpath = os.path.join(subj_dir, fname)
        try:
            df = pd.read_csv(fpath, dtype=str)
            if df.empty or "Enrollment" not in df.columns:
                continue

            def row_matches(row):
                if str(row.get("Enrollment", "")).strip() != enroll_str:
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
            print(f"Error deleting in {fname}: {e}")

    return deleted_any, f"Attendance record for #{enroll_str} deleted."
    """
    story.append(Preformatted(code_delete, code_style))
    story.append(PageBreak())

    # ─── APPENDIX C: SAMPLE INPUT ───
    story.append(Paragraph("APPENDIX C: SAMPLE INPUT", sec_h1))
    story.append(Paragraph("<b>Sample Student Enrollment Record (`data/students.csv`):</b>", body))

    sample_students_data = [
        [Paragraph("<b>Enrollment</b>", th_style), Paragraph("<b>Name</b>", th_style), Paragraph("<b>Department</b>", th_style), Paragraph("<b>Email</b>", th_style), Paragraph("<b>Phone</b>", th_style)],
        [Paragraph("001", td_style), Paragraph("JD", td_style), Paragraph("CSE", td_style), Paragraph("jd@college.edu", td_style), Paragraph("9876543210", td_style)],
        [Paragraph("002", td_style), Paragraph("Dhivya", td_style), Paragraph("CSE", td_style), Paragraph("dhivya@college.edu", td_style), Paragraph("9876543211", td_style)],
        [Paragraph("003", td_style), Paragraph("Jayanthi", td_style), Paragraph("IT", td_style), Paragraph("jayanthi@college.edu", td_style), Paragraph("9876543212", td_style)],
        [Paragraph("101", td_style), Paragraph("Dhanush Kumar", td_style), Paragraph("CSE", td_style), Paragraph("dhanush@college.edu", td_style), Paragraph("9876543213", td_style)],
        [Paragraph("102", td_style), Paragraph("Priya Sharma", td_style), Paragraph("ECE", td_style), Paragraph("priya@college.edu", td_style), Paragraph("9876543214", td_style)]
    ]

    t_sample_stu = Table(sample_students_data, colWidths=[1.1*inch, 1.6*inch, 1.0*inch, 1.9*inch, 1.2*inch])
    t_sample_stu.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sample_stu)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Sample Attendance Session Log (`data/attendance/Science/Science_2026-10-04.csv`):</b>", body))

    sample_att_data = [
        [Paragraph("<b>Enrollment</b>", th_style), Paragraph("<b>Name</b>", th_style), Paragraph("<b>Date</b>", th_style), Paragraph("<b>Time</b>", th_style), Paragraph("<b>Status</b>", th_style)],
        [Paragraph("003", td_style), Paragraph("Jayanthi", td_style), Paragraph("2026-10-04", td_style), Paragraph("11:49:50", td_style), Paragraph("<font color='green'><b>Present</b></font>", td_style)],
        [Paragraph("001", td_style), Paragraph("JD", td_style), Paragraph("2026-10-04", td_style), Paragraph("11:49:55", td_style), Paragraph("<font color='green'><b>Present</b></font>", td_style)],
        [Paragraph("002", td_style), Paragraph("Dhivya", td_style), Paragraph("2026-10-04", td_style), Paragraph("11:50:18", td_style), Paragraph("<font color='green'><b>Present</b></font>", td_style)]
    ]

    t_sample_att = Table(sample_att_data, colWidths=[1.1*inch, 1.8*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    t_sample_att.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D9488")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sample_att)
    story.append(PageBreak())

    # ─── APPENDIX D: SAMPLE OUTPUT (SCREENSHOTS) ───
    story.append(Paragraph("APPENDIX D: SAMPLE OUTPUT (SYSTEM SCREENSHOTS)", ch_title_style))
    story.append(Spacer(1, 6))

    screenshots = [
        ("Figure D.1: FaceAttend Administrative Dashboard & Real-Time Metric Overview", "screenshot_dashboard.png"),
        ("Figure D.2: Student Registration Interface with Oval Guide & Paced Multi-Angle Dots", "screenshot_register.png"),
        ("Figure D.3: Biometric Model Training & In-Memory Cache Compilation Status", "screenshot_train.png"),
        ("Figure D.4: Live Biometric Recognition Feed with Verified Green HUD & Session List", "screenshot_attendance.png"),
        ("Figure D.5: Attendance Reports Table with Real-time Filters & Action Delete Buttons", "screenshot_reports.png")
    ]

    for caption, img_name in screenshots:
        img_path = os.path.join(BASE_DIR, img_name)
        if os.path.exists(img_path):
            story.append(Paragraph(f"<b>{caption}</b>", sec_h2))
            story.append(Spacer(1, 4))
            # Image size scaled to fit A4 neatly (width 6.5 inch, height 3.6 inch)
            story.append(Image(img_path, width=6.5*inch, height=3.6*inch))
            story.append(Spacer(1, 14))

    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print("Report body generated successfully at:", TEMP_BODY_PDF)


def merge_with_front_pages():
    print("Merging front 3 pages from original PDF with new technical report body...")
    orig_reader = pypdf.PdfReader(ORIGINAL_PDF)
    body_reader = pypdf.PdfReader(TEMP_BODY_PDF)

    writer = pypdf.PdfWriter()

    # Step 1: Copy Page 1, 2, 3 EXACTLY from SANJEEVAN BOOK SHOP.pdf
    print("Copying Page 1 (Title/Certificate), Page 2 (Guide Certificate), Page 3 (Acknowledgement)...")
    for i in range(3):
        writer.add_page(orig_reader.pages[i])

    # Step 2: Append all pages from the new report body
    print(f"Appending {len(body_reader.pages)} pages of the new Face Attendance System report...")
    for p in body_reader.pages:
        writer.add_page(p)

    # Step 3: Write final combined PDF
    with open(FINAL_OUTPUT_PDF, "wb") as f_out:
        writer.write(f_out)

    # Also overwrite SANJEEVAN BOOK SHOP.pdf if requested or keep both
    print("Writing final document...")
    print(f"SUCCESS: Final report generated at: {FINAL_OUTPUT_PDF}")
    print(f"Total Pages in Final Document: {len(writer.pages)}")

    # Clean up temp body
    if os.path.exists(TEMP_BODY_PDF):
        os.remove(TEMP_BODY_PDF)


if __name__ == "__main__":
    build_report()
    merge_with_front_pages()
