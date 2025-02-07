import os
import base64
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ==========================================
# Hashing password before store
# ==========================================
def generate_salt(length=16):
    """Generate a randrom salt of specified length."""
    return base64.b64encode(os.urandom(length)).decode('utf-8')

def hash_password(password):
    """
    Hash a password with a custome salt
    """
    salt = generate_salt()
    
    # Combine salt
    salted=hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    # Hashing on top of our salt hash
    final_hash=generate_password_hash(salted)
    
    return f"{salt}:{final_hash}"

def verify_password(stored_hash,password_attempt):
    """
    Verify password againt a stored hash.
    stored_hash format be "salt:hashed_password"
    """
    try:
        # Split store value into salt and hash
        salt,stored_werkeug_hash=stored_hash.split(':',1)
        
        # Recreate salt hash with provide password
        salted_attempt=hashlib.sha256(f"{salt}{password_attempt}".encode()).hexdigest()
        
        # Verify user Werkzeug check
        return check_password_hash(stored_werkeug_hash,salted_attempt)
    except:
        return False
    
# ==========================================
# DateTime format
# ==========================================
def format_datetime(dt: datetime):
    """Format a datetime object to a string in GMT format."""
    if dt is None:
        return None
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")