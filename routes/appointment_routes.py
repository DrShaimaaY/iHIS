from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from datetime import datetime

appointments = Blueprint('appointments', __name__)

@appointments.route('/appointments')
@login_required
def list_appointments():
    all_appointments = Appointment.query.all()
    return render_template('appointments/list.html', appointments=all_appointments)

@appointments.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    
    if request.method == 'POST':
        new_appointment = Appointment(
            patient_id=request.form.get('patient_id'),
            doctor_id=request.form.get('doctor_id'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            time=datetime.strptime(request.form.get('time'), '%H:%M').time(),
            status=request.form.get('status'),
            notes=request.form.get('notes')
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('appointments.list_appointments'))
    
    return render_template('appointments/add.html', patients=patients, doctors=doctors)