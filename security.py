import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session
import re

# Security configuration
SECRET_KEY = secrets.token_hex(32)
JWT_EXPIRATION_HOURS = 8

# User roles for healthcare system
ROLES = {
    'admin': ['all'],
    'doctor': ['patient_read', 'patient_write', 'monitoring'],
    'nurse': ['patient_read', 'monitoring', 'notifications'],
    'staff': ['patient_read', 'monitoring']
}

class SecurityManager:
    def __init__(self):
        self.active_sessions = {}
        self.failed_attempts = {}
        
    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id, role):
        """Generate JWT token for authenticated user"""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def validate_input(self, data, field_type):
        """Validate and sanitize input data"""
        if field_type == 'patient_id':
            # Patient ID: alphanumeric, 3-20 chars
            return re.match(r'^[A-Za-z0-9]{3,20}$', str(data)) is not None
        elif field_type == 'name':
            # Name: letters, spaces, hyphens, 2-50 chars
            return re.match(r'^[A-Za-z\s\-]{2,50}$', str(data)) is not None
        elif field_type == 'room_bed':
            # Room/Bed: alphanumeric, 1-10 chars
            return re.match(r'^[A-Za-z0-9]{1,10}$', str(data)) is not None
        elif field_type == 'medical_text':
            # Medical text: letters, numbers, spaces, basic punctuation
            return re.match(r'^[A-Za-z0-9\s\.\,\-\(\)]{0,500}$', str(data)) is not None
        return False
    
    def check_rate_limit(self, ip_address, max_attempts=5, window_minutes=15):
        """Check if IP has exceeded rate limit"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = []
        
        # Remove old attempts
        self.failed_attempts[ip_address] = [
            attempt for attempt in self.failed_attempts[ip_address] 
            if attempt > window_start
        ]
        
        return len(self.failed_attempts[ip_address]) < max_attempts
    
    def record_failed_attempt(self, ip_address):
        """Record failed login attempt"""
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = []
        self.failed_attempts[ip_address].append(datetime.utcnow())

# Initialize security manager
security = SecurityManager()

def require_auth(required_permission=None):
    """Decorator to require authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Authentication required'}), 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = security.verify_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Check permissions
            if required_permission:
                user_role = payload.get('role')
                user_permissions = ROLES.get(user_role, [])
                if required_permission not in user_permissions and 'all' not in user_permissions:
                    return jsonify({'error': 'Insufficient permissions'}), 403
            
            request.current_user = payload
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_patient_data(data):
    """Validate patient registration data"""
    required_fields = ['fullName', 'patientId', 'bedNumber', 'roomNumber', 'primaryCondition']
    errors = []
    
    # Check required fields
    for field in required_fields:
        if not data.get(field):
            errors.append(f'{field} is required')
    
    # Validate field formats
    if data.get('fullName') and not security.validate_input(data['fullName'], 'name'):
        errors.append('Invalid name format')
    
    if data.get('patientId') and not security.validate_input(data['patientId'], 'patient_id'):
        errors.append('Invalid patient ID format')
    
    if data.get('bedNumber') and not security.validate_input(data['bedNumber'], 'room_bed'):
        errors.append('Invalid bed number format')
    
    if data.get('roomNumber') and not security.validate_input(data['roomNumber'], 'room_bed'):
        errors.append('Invalid room number format')
    
    if data.get('primaryCondition') and not security.validate_input(data['primaryCondition'], 'medical_text'):
        errors.append('Invalid primary condition format')
    
    return errors

def sanitize_patient_data(data):
    """Sanitize patient data before storage"""
    sanitized = {}
    
    # Only allow specific fields
    allowed_fields = [
        'fullName', 'patientId', 'bedNumber', 'roomNumber', 'primaryCondition',
        'dateOfBirth', 'gender', 'department', 'careLevel', 'mobilityLevel',
        'medicalHistory', 'attendingPhysician', 'admissionDate'
    ]
    
    for field in allowed_fields:
        if field in data:
            # Basic sanitization - remove potential script tags
            value = str(data[field]).replace('<', '&lt;').replace('>', '&gt;')
            sanitized[field] = value[:500]  # Limit length
    
    return sanitized

def log_security_event(event_type, details, ip_address=None):
    """Log security events for audit trail"""
    timestamp = datetime.utcnow().isoformat()
    ip = ip_address or request.remote_addr if request else 'unknown'
    
    log_entry = f"[{timestamp}] SECURITY: {event_type} - {details} - IP: {ip}"
    print(log_entry)
    
    # In production, write to secure log file
    # with open('/var/log/bedsidebot_security.log', 'a') as f:
    #     f.write(log_entry + '\n')