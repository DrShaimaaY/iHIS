# Cleaned version - conflict resolved
import os
import uuid
import numpy as np
import cv2
import tensorflow as tf
from flask import Blueprint, render_template, request, url_for
from PIL import Image

dentistry_bp = Blueprint('dentistry', __name__)

IMG_SIZE = 256
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'unet_teeth_final.h5')

def dice_coef(y_true, y_pred, smooth=1e-6):
    y_true_f = tf.keras.backend.flatten(y_true)
    y_pred_f = tf.keras.backend.flatten(y_pred)
    intersection = tf.keras.backend.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (
        tf.keras.backend.sum(y_true_f) + tf.keras.backend.sum(y_pred_f) + smooth)

def dice_loss(y_true, y_pred):
    return 1 - dice_coef(y_true, y_pred)

def bce_dice_loss(y_true, y_pred):
    bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)
    return bce + dice_loss(y_true, y_pred)

def iou_metric(y_true, y_pred, smooth=1e-6):
    y_true_f = tf.keras.backend.flatten(y_true)
    y_pred_f = tf.keras.backend.flatten(tf.cast(y_pred > 0.5, tf.float32))
    intersection = tf.keras.backend.sum(y_true_f * y_pred_f)
    union = tf.keras.backend.sum(y_true_f) + tf.keras.backend.sum(y_pred_f) - intersection
    return (intersection + smooth) / (union + smooth)

model = tf.keras.models.load_model(MODEL_PATH, custom_objects={
    'bce_dice_loss': bce_dice_loss,
    'dice_coef': dice_coef,
    'iou_metric': iou_metric
})

@dentistry_bp.route('/dentistry', methods=['GET'])
def dentistry():
    return render_template('dentistry/dentistry.html')

@dentistry_bp.route('/dentistry/analyze', methods=['POST'])
def analyze():
    if 'xray' not in request.files:
        return render_template('dentistry/dentistry.html', error='Please upload an image.')

    file = request.files['xray']
    unique_id = uuid.uuid4().hex[:8]
    upload_path = os.path.join('static', 'uploads', unique_id + '_' + file.filename)
    file.save(upload_path)

    img = np.array(Image.open(upload_path).convert('RGB'))
    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img_norm = img_resized / 255.0
    pred = model.predict(np.expand_dims(img_norm, axis=0))[0]
    mask = (pred.squeeze() > 0.5).astype(np.uint8) * 255

    mask_rgb = np.zeros_like(img_resized)
    mask_rgb[mask > 0] = [0, 255, 0]
    overlay = cv2.addWeighted(img_resized, 0.7, mask_rgb, 0.3, 0)

    result_path = os.path.join('static', 'uploads', unique_id + '_result.png')
    cv2.imwrite(result_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

    return render_template('dentistry/dentistry.html',
                           original=upload_path,
                           result=result_path)
