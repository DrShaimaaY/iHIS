from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Create the application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
from models import db
db.init_app(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes
from routes.auth_routes import auth
app.register_blueprint(auth)
from routes.patient_routes import patients
app.register_blueprint(patients)
from routes.appointment_routes import appointments
app.register_blueprint(appointments)
from routes.doctor_routes import doctors
app.register_blueprint(doctors)
from routes.dentistry_routes import dentistry_bp
app.register_blueprint(dentistry_bp)
from routes.orthopedics_routes import orthopedics_bp
app.register_blueprint(orthopedics_bp)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)