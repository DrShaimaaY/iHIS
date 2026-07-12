from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.doctor import Doctor
from datetime import datetime

doctors = Blueprint('doctors', __name__)

@doctors.route('/doctors')
@login_required
def list_doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors/list.html', doctors=all_doctors)

@doctors.route('/doctors/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if request.method == 'POST':
        new_doctor = Doctor(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            specialty=request.form.get('specialty'),
            license_number=request.form.get('license_number'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            department=request.form.get('department')
        )
        db.session.add(new_doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctors.list_doctors'))
    
    return render_template('doctors/add.html')