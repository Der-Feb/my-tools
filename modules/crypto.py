import uuid
import jwt
import warnings

def get_uuids(count=1):
    # Ensure it's an integer and stays within the 1-200 range
    safe_count = max(1, min(int(count), 200))
    return [str(uuid.uuid4()) for _ in range(safe_count)]

def decode_jwt(token, key=None):
    """
    Decodes a JWT token. 
    If key is provided, it verifies the signature. 
    Otherwise, it decodes without verification.
    """
    try:
        # Suppress the insecure key length warning for quick testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            if key:
                # Auto-detect algorithm from token header
                header = jwt.get_unverified_header(token)
                alg = header.get('alg', 'HS256')
                return jwt.decode(token, key, algorithms=[alg])
            else:
                return jwt.decode(token, options={"verify_signature": False})
    except jwt.ExpiredSignatureError:
        return "Error: Token has expired."
    except jwt.InvalidSignatureError:
        return "Error: Invalid signature. Check your key."
    except jwt.DecodeError:
        return "Error: Failed to decode token. Ensure it's a valid JWT string."
    except Exception as e:
        return f"Error: {str(e)}"

def create_jwt(payload, key, algorithm='HS256'):
    """
    Creates a JWT token from a payload and secret key.
    """
    try:
        # Suppress the insecure key length warning for quick testing
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return jwt.encode(payload, key, algorithm=algorithm)
    except Exception as e:
        return f"Error: {str(e)}"