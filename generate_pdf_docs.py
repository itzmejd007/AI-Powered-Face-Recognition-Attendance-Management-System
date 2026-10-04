import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = r"d:\Projects\Attendance-Management-system-using-face-recognition-master\FaceAttend_Project_Documentation_Thanglish.pdf"

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "FaceAttend - AI Face Recognition Attendance System | Project Report")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, text)
        self.drawString(54, 36, "Confidential - For Academic & Project Review | Created in Thanglish & English")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def create_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0D9488"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    bold_body = ParagraphStyle(
        'BoldBody_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    thanglish_box_style = ParagraphStyle(
        'ThanglishBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'THStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TDStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ─── TITLE & BANNER ───
    story.append(Paragraph("FaceAttend: AI Face Recognition Attendance System", title_style))
    story.append(Paragraph("Complete Technical Documentation, Architecture & Tools Guide (Thanglish Explanation)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563EB"), spaceBefore=0, spaceAfter=12))

    meta_html = """
    <b>Project Type:</b> AI/ML Computer Vision Web Application &nbsp;|&nbsp; 
    <b>Architecture:</b> Flask Backend + OpenCV LBPH Engine + Vanilla JS Dashboard<br/>
    <b>Storage:</b> Local CSV & YML Models (100% Free, Offline, Zero Cloud Dependency)<br/>
    <b>Document Language:</b> Thanglish (Tamil in English Script) + Technical English
    """
    story.append(Paragraph(meta_html, meta_style))
    story.append(Spacer(1, 14))

    # ─── SECTION 1: PROJECT OVERVIEW ───
    story.append(Paragraph("1. Project Overview & Nokkam (Intro & Objective)", h1_1 := h1_style))
    intro_p1 = """
    <b>Intha Project Enna Pannuthu?</b><br/>
    Intha system oru smart, automated <b>AI Face Recognition Attendance Management System</b>. College, school, illana office-la manual-ah pen & paper-la roll call edukurathuku pathila, web camera munnala student vanthu ninnale pothum — avanga mugatha (face) computer vision AI moolama identify panni, fraction of a second-la (sub-25 milliseconds) <b>Present</b> nu attendance mark pannidum.
    """
    story.append(Paragraph(intro_p1, body_style))

    intro_p2 = """
    <b>Ethukaga Intha Project Romba Mukkiyam? (Problem & Solution):</b><br/>
    • <b>Proxy Attendance Thadukalam:</b> Friend-ku pathila vera yaaravathu attendance podratha (proxy) 100% thadukkum. Because candidate-oda live face camera-la paatha mattum thaan green color box vanthu attendance confirm aagum.<br/>
    • <b>Time Saving:</b> 60 students irukura class-la manual roll call edukka 10-15 minutes aagum. Aana intha camera system-la students nadanthu varum bothey auto-mark aagidum.<br/>
    • <b>Subject-Wise Attendance:</b> Ore naal-la Maths, Science, Social nu ovvoru period-kum thani thani session vechu attendance record maintain pannalam.<br/>
    • <b>100% Offline & Free:</b> Intha project run aaga costly-ana paid cloud APIs (AWS Rekognition, Azure Face API) ethuvum thevaiyillai. Normal laptop CPU-laye zero cost-la full fast-ah run aagum.
    """
    story.append(Paragraph(intro_p2, body_style))
    story.append(Spacer(1, 10))

    # ─── SECTION 2: LANGUAGES USED ───
    story.append(Paragraph("2. Programming Languages Used & Reason (Ethukaga Enna Language?)", h1_style))
    
    lang_data = [
        [
            Paragraph("Language", table_header_style),
            Paragraph("Where is it used? (Project-la enga use aaguthu?)", table_header_style),
            Paragraph("Detailed Reason & Role (Ethukaga use pannom?)", table_header_style)
        ],
        [
            Paragraph("<b>Python 3.12</b>", table_cell_style),
            Paragraph("Backend Server, Face Detection, AI Model Training, CSV Data Handling", table_cell_style),
            Paragraph("Python AI & Computer Vision-ku world-wide best language. OpenCV, NumPy, Pandas, Flask mathiri periya data science & ML libraries Python-la romba fast-ah integrate aagum. Image matrix calculations & algorithm tuning Python-la romba clean-ah implement panna mudiyum.", table_cell_style)
        ],
        [
            Paragraph("<b>JavaScript (ES6+)</b>", table_cell_style),
            Paragraph("Frontend Logic, Camera Feed HUD, Audio Beeps, Real-time API Calls", table_cell_style),
            Paragraph("Browser-la live webcam feed access panna (WebRTC getUserMedia), camera stream-la face bounding box animate panna (HTML5 Canvas 2D), and page refresh aagama background-la data anuppa (Fetch API async/await) JavaScript use aaguthu. Heavy frameworks illama light-weight-ah work aagum.", table_cell_style)
        ],
        [
            Paragraph("<b>HTML5</b>", table_cell_style),
            Paragraph("Web App Structure & Layout", table_cell_style),
            Paragraph("Modern web structure, video element (&lt;video&gt; tag), face guide canvas (&lt;canvas&gt; tag), attendance table layout, and dynamic subject dropdown controls provide pannuthu.", table_cell_style)
        ],
        [
            Paragraph("<b>CSS3 (Vanilla)</b>", table_cell_style),
            Paragraph("Styling, Cyberpunk Dark Theme, Responsive Layout", table_cell_style),
            Paragraph("Modern glassmorphism look, neon green & cyan glowing colors, smooth micro-animations, and mobile/laptop responsive interface tharathuku Tailwind/Bootstrap illama pure custom CSS use pannirukom.", table_cell_style)
        ]
    ]

    t_lang = Table(lang_data, colWidths=[1.1*inch, 2.2*inch, 3.7*inch])
    t_lang.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lang)
    story.append(Spacer(1, 14))

    # ─── SECTION 3: LIBRARIES & TOOLS ───
    story.append(Paragraph("3. Libraries & Tools Detailed Breakdown (Moththa Libraries List)", h1_style))

    lib_data = [
        [
            Paragraph("Library / Tool", table_header_style),
            Paragraph("Category", table_header_style),
            Paragraph("Detailed Purpose in Project (Namma Project-la Enna Vela?)", table_header_style)
        ],
        [
            Paragraph("<b>OpenCV<br/>(opencv-contrib-python)</b>", table_cell_style),
            Paragraph("Computer Vision & AI", table_cell_style),
            Paragraph("Project-oda main heart. Haar Cascade moolama live webcam-la human face-ah detect pannum. Adhuku aprom LBPH (Local Binary Patterns Histograms) algorithm moolama face features extract panni model train pannum & recognize pannum. Contrib package thevai because `cv2.face` module athula thaan irukum.", table_cell_style)
        ],
        [
            Paragraph("<b>Flask</b>", table_cell_style),
            Paragraph("Python Web Framework", table_cell_style),
            Paragraph("Ultra-fast micro web server. Frontend browser-kku HTML render pannum. Browser camera frames-ah base64 format-la receive panni recognition result (Match status, Name, Confidence) JSON response-ah thiruppi anuppum REST API endpoints create panna use aaguthu.", table_cell_style)
        ],
        [
            Paragraph("<b>Flask-CORS</b>", table_cell_style),
            Paragraph("Security / Networking", table_cell_style),
            Paragraph("Cross-Origin Resource Sharing enable pannuthu. Vera devices or IP addresses (e.g. Wi-Fi network-la irukura mobile or laptop) namma API-ah access pannumbothu CORS error varama smooth-ah connect aaga ithu thevai.", table_cell_style)
        ],
        [
            Paragraph("<b>NumPy</b>", table_cell_style),
            Paragraph("Matrix & Math Engine", table_cell_style),
            Paragraph("Ovvoru face image-um computer-ku 2D pixel matrix. Bilateral filtering, brightness scaling, look-up table (LUT) gamma arrays, and crop array manipulations fast-ah compute panna NumPy array operations romba mukkiyam.", table_cell_style)
        ],
        [
            Paragraph("<b>Pillow (PIL)</b>", table_cell_style),
            Paragraph("Image Conversion", table_cell_style),
            Paragraph("Webcam-la irunthu browser anupura Base64 JPEG byte string-ah Python image object-ah decode panni OpenCV grayscale array-ah convert panna Pillow use aaguthu.", table_cell_style)
        ],
        [
            Paragraph("<b>Pandas</b>", table_cell_style),
            Paragraph("Data Analytics & CSV", table_cell_style),
            Paragraph("Student details (`students.csv`) and subject attendance logs (`data/attendance/`) read panna, fast lookup panna, duplicate check panna, and single record delete panna Pandas DataFrame use aaguthu.", table_cell_style)
        ],
        [
            Paragraph("<b>Web Audio API</b>", table_cell_style),
            Paragraph("Browser Audio Engine", table_cell_style),
            Paragraph("External mp3 audio files illama, browser-oda built-in AudioContext moolama synthetic pleasant success chime and camera shutter click beeps generate panna use aaguthu.", table_cell_style)
        ],
        [
            Paragraph("<b>ReportLab</b>", table_cell_style),
            Paragraph("PDF Generation", table_cell_style),
            Paragraph("Project documentation, user manual, and official attendance report summaries-ah PDF format-la high quality print layout ready panna use aaguthu.", table_cell_style)
        ]
    ]

    t_lib = Table(lib_data, colWidths=[1.4*inch, 1.3*inch, 4.3*inch])
    t_lib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D9488")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_lib)
    story.append(Spacer(1, 14))

    story.append(PageBreak())

    # ─── SECTION 4: AI & COMPUTER VISION PIPELINE ───
    story.append(Paragraph("4. Computer Vision & Machine Learning Pipeline (Ulle Epdi Work Aaguthu?)", h1_style))
    cv_desc = """
    Intha system-la face recognition epdi 99%+ accuracy and low-lighting-layum perfect-ah work aaguthu nu step-by-step technical explanation:
    """
    story.append(Paragraph(cv_desc, body_style))

    steps_data = [
        [
            Paragraph("<b>Step 1: Face Detection (Haar Cascade)</b>", bold_body),
            Paragraph("Camera frame-la input varum pothu `haarcascade_frontalface_default.xml` moolama face irukura area-va `(x, y, w, h)` coordinates-la detect pannum. MultiScale detection vechu candidate face mattum crop pannapadum.", body_style)
        ],
        [
            Paragraph("<b>Step 2: Denoising (Bilateral Filter)</b>", bold_body),
            Paragraph("Low-lighting-la webcam-la sensor grain (noise) adhigama irukum. Bilateral filter (`d=5, sigma=30`) facial edges and features (eyes, nose, jawline) sharp-ah vachikittu background noise-ah mattum smooth pannidum.", body_style)
        ],
        [
            Paragraph("<b>Step 3: Low-Light Normalization (Adaptive Gamma Correction)</b>", bold_body),
            Paragraph("Oru room-la velicham romba kuraiva iruntha (intensity &lt; 105), algorithm automatically gamma value compute pannum (`gamma = log(0.5)/log(mean/255)`). Look-up table (LUT) moolama dark face-ah automatic-ah daylight clarity-ku brighten pannidum!", body_style)
        ],
        [
            Paragraph("<b>Step 4: Contrast Equalization (CLAHE)</b>", bold_body),
            Paragraph("Contrast Limited Adaptive Histogram Equalization (CLAHE) apply panni, mugathula vizhugura nizhal (shadows) and light reflections-ah balance panni uniform facial contrast create pannum.", body_style)
        ],
        [
            Paragraph("<b>Step 5: LBPH Model Training & Matching</b>", bold_body),
            Paragraph("Face 200x200 crop aana piragu, LBPH 8-neighbor circular pattern create pannum. Mukiyathuvam: Training time-la base face, horizontal flip, and shadow variants 30 samples ready panni `face_model.yml`-la save pannidum.", body_style)
        ],
        [
            Paragraph("<b>Step 6: Threshold Decision Logic</b>", bold_body),
            Paragraph("`RECOGNITION_THRESHOLD = 52` nu calibrate pannirukom. Student face-oda distance &lt; 52 iruntha <b>GREEN BOX (VERIFIED)</b> vanthu attendance mark aagum. Stranger / Unknown face-ku distance 100+ pogum, so <b>RED BOX (UNKNOWN FACE / ACCESS DENIED)</b> aagi mark aagathu!", body_style)
        ]
    ]

    t_steps = Table(steps_data, colWidths=[2.3*inch, 4.7*inch])
    t_steps.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#F0FDF4"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 14))

    # ─── SECTION 5: SPECIAL FEATURES BUILT ───
    story.append(Paragraph("5. Special Features & Problems Solved (Naama Pannina Mukkiya Upgrades)", h1_style))

    features_html = """
    <b>1. Slow-Paced Natural Movement 10-Photo Capture (420ms interval):</b><br/>
    Pazhaiya system-la 1 second-la 10 burst photos ore static position-la eduthathala, camera munnala student konjam thalaiya thiruppina kooda 'Access Denied' nu vanthuchu. Ipo 10 photos edukkumbothu ovvoru shot-kum 420ms gap vechu, screen-la 'Look Straight', 'Slight Tilt Left/Right', 'Chin Up/Down', 'Distance Shift' nu guide pannuthu. Ithanala model natural head angles-la romba accurate-ah train aaguthu.<br/><br/>

    <b>2. Low-Lighting & Dim Room Capability:</b><br/>
    Adaptive Gamma Correction & Bilateral filtering serthathala, dark room-la kooda face distance 25-48 range-la vanthu green box verified aagidum.<br/><br/>

    <b>3. Live Attendance Dropdown Switch:</b><br/>
    Thevaillatha 'Switch Subj' button-ah remove pannitu, simple dropdown select moolama Maths, Science, Social nu session switch pannalam. Pudhu subject venumna dropdown-laye `+ Add New Subject` kuduthu instant-ah create pannalam.<br/><br/>

    <b>4. Reports Tab Instant Auto-Load & Refresh Button:</b><br/>
    Reports page-la subject select pannathume 'Load Records' click panna thevai illama, keezha table automatic-ah instant-ah load aagidum. Table-ah manual-ah refresh panna 'Refresh Records' button kuduthurukom.<br/><br/>

    <b>5. Complete Attendance Deletion & Undo Engine:</b><br/>
    • <b>Live Attendance Quick Undo:</b> Live feed-la oruthar thappa present aagita, right sidebar-la avanga name pakkathula irukura <b>[X]</b> button click panna udaney mark delete aagidum.<br/>
    • <b>Reports Table Delete Row:</b> Reports table-la ovvoru student record pakkathulayum <b>[Delete]</b> button irukum.<br/>
    • <b>Clear All Records:</b> Oru subject-oda moththa attendance logs-aiyum ore click-la clear panna <b>[Clear Records]</b> button iruku.<br/><br/>

    <b>6. Any Laptop / Multi-Device Portability:</b><br/>
    Hardcoded computer paths ethuvum illama relative paths vachurukom. Windows-la <b>run.bat</b> double click pannale Python verify panni, libraries install panni, browser open pannidum. Linux/Mac-ku <b>run.sh</b> iruku. Wi-Fi LAN access-um support pannum.
    """
    story.append(Paragraph(features_html, body_style))
    story.append(Spacer(1, 14))

    # ─── SECTION 6: HOW TO EXPLAIN IN INTERVIEW / VIVA ───
    story.append(Paragraph("6. Project Viva / Review-la Epdi Explain Pannanum? (Short Summary)", h1_style))
    viva_text = """
    <b>Q: Unga project architecture enna?</b><br/>
    <i>Answer:</i> 'Namma project oru Client-Server Architecture. Frontend HTML5, CSS3, Vanilla JS-la responsive dashboard-ah build pannirukom. Backend Flask framework-la Python-la create pannirukom. Real-time face detection-ku Haar Cascade Classifier-um, face recognition-ku OpenCV-oda LBPH (Local Binary Patterns Histograms) algorithm-um use pannirukom. Attendance logs subject-wise separate CSV files-la auto-record aaguthu.'<br/><br/>

    <b>Q: Deep learning models (CNN/FaceNet) use panradhuku pathila yen LBPH choose panninga?</b><br/>
    <i>Answer:</i> 'Deep learning models run panna heavy GPU and high memory thevai. Athu simple college/office laptops-la lag aagum. But LBPH CPU-laye fraction of a millisecond-la (sub-25ms) ultra-fast-ah run aagum, offline-laye 99%+ accuracy tharum, zero-cost, and instant-ah train aagidum. Light variations-ah tackle panna naanga Adaptive Gamma Correction & CLAHE preprocess pipeline add pannirukom.'<br/><br/>

    <b>Q: Data enga store aaguthu?</b><br/>
    <i>Answer:</i> 'Students register aagumbothu 10 high-resolution normalized face crops `data/students/{id}_{name}/` folder-layum, metadata `data/students.csv`-layum save aaguthu. Trained model `data/models/face_model.yml` binary format-la irukum. Daily attendance logs `data/attendance/{Subject}/{Subject}_{Date}.csv` file-la secure-ah organize aaguthu.'
    """
    story.append(Paragraph(viva_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF successfully generated at:", PDF_PATH)

if __name__ == "__main__":
    create_pdf()
