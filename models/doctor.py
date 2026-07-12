from models import db
from datetime import datetime

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic info
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    # Medical info
    specialty = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Contact info
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    # Work info
    department = db.Column(db.String(100))
    is_available = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Link to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name}>'