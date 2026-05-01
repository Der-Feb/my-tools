import uuid
import jwt

def get_uuids(count=1):
    # Ensure it's an integer and stays within the 1-200 range
    safe_count = max(1, min(int(count), 200))
    return [str(uuid.uuid4()) for _ in range(safe_count)]

# ... keep your decode_jwt function here

def decode_jwt(token):
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        return f"Error: {e}"