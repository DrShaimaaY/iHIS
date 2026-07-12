from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_login import login_required
from models import db
from models.patient import Patient

patients = Blueprint('patients', __name__)

@patients.route('/patients')
@login_required
def list_patients():
    all_patients = Patient.query.all()
    return render_template('patients/list.html', patients=all_patients)

@patients.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        new_patient = Patient(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            date_of_birth=datetime(int(request.form.get('year')), int(request.form.get('month')), int(request.form.get('day'))).date(),
            gender=request.form.get('gender'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            blood_type=request.form.get('blood_type')
        )
        db.session.add(new_patient)
        db.session.commit()
        
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients.list_patients'))
    
    return render_template('patients/add.html')