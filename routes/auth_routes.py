from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from routes import auth
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        # Check password
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Wrong username or password', 'danger')
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/dashboard')
@login_required
def dashboard():
    from models.patient import Patient
    from models.doctor import Doctor
    from models.appointment import Appointment
    
    patients_count = Patient.query.count()
    doctors_count = Doctor.query.count()
    appointments_count = Appointment.query.count()
    
    return render_template('dashboard.html',
        patients_count=patients_count,
        doctors_count=doctors_count,
        appointments_count=appointments_count
    )

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))