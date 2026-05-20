from datetime import datetime

# Validate request fields

def validate_fields(data, fields):

    for field in fields:

        if field not in data:
            return False

        if not data[field]:
            return False

    return True


def format_timestamp(timestamp):
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_time

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))