# ============================================
# orthopedics_routes.py
# Blueprint for the Orthopedics fracture detection module.
# Uses a trained YOLOv8 model to detect fractures and other
# bone-related structures in uploaded X-ray images.
# ============================================

import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from ultralytics import YOLO

# Create the Blueprint - this groups all Orthopedics routes together,
# the same way dentistry_routes.py groups the dental routes.
orthopedics_bp = Blueprint('orthopedics', __name__, template_folder='../templates/orthopedics')

# Path to the trained model file
MODEL_PATH = os.path.join('ml_models', 'fracture_yolo_best.pt')

# Load the model once when the app starts (not on every request,
# since loading is slow and would make the app very sluggish).
model = YOLO(MODEL_PATH)

# Class names must match exactly what the model was trained with
CLASS_NAMES = ['fractured', 'hand', 'hardware', 'hip', 'leg', 'shoulder']

# Where uploaded images and result images will be saved
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'orthopedics')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check that the uploaded file has an allowed image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------------------------------------
# Route 1: Home page - project title, description, upload button
# ------------------------------------------------
@orthopedics_bp.route('/orthopedics')
def orthopedics_home():
    return render_template('orthopedics/home.html')


# ------------------------------------------------
# Route 2: Handle the image upload and run AI prediction
# ------------------------------------------------
@orthopedics_bp.route('/orthopedics/upload', methods=['GET', 'POST'])
def orthopedics_upload():
    if request.method == 'POST':
        # Check a file was actually submitted
        if 'xray_image' not in request.files:
            flash('No file selected.')
            return redirect(request.url)

        file = request.files['xray_image']

        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Only JPG, JPEG, and PNG files are allowed.')
            return redirect(request.url)

        # Save the uploaded file with a unique name to avoid overwriting
        original_filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex[:8]
        saved_filename = f"{unique_id}_{original_filename}"
        upload_path = os.path.join(UPLOAD_FOLDER, saved_filename)
        file.save(upload_path)

        # Run the YOLO model on the uploaded image
        results = model.predict(source=upload_path, imgsz=640, conf=0.15)
        result = results[0]

        # Save the annotated image (with bounding boxes drawn on it)
        annotated_filename = f"annotated_{saved_filename}"
        annotated_path = os.path.join(UPLOAD_FOLDER, annotated_filename)
        result.save(filename=annotated_path)

        # Check whether a 'fractured' box was detected, and get its confidence
        fracture_detected = False
        fracture_confidence = 0.0
        detected_parts = []

        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = CLASS_NAMES[class_id]
            confidence = float(box.conf[0])

            if class_name == 'fractured':
                fracture_detected = True
                fracture_confidence = max(fracture_confidence, confidence)
            else:
                detected_parts.append(class_name)

        # Build a simple result summary
        return render_template(
            'orthopedics/result.html',
            original_image=upload_path.replace('\\', '/'),
            annotated_image=annotated_path.replace('\\', '/'),
            fracture_detected=fracture_detected,
            fracture_confidence=round(fracture_confidence * 100, 1),
            detected_parts=list(set(detected_parts))
        )

    # GET request: just show the upload form
    return render_template('orthopedics/upload.html')