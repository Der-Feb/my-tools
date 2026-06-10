from datetime import datetime
import dateparser
from urllib.parse import urlparse, parse_qs

def format_timestamp(ts, ms=False):
    """Timestamp to readable string"""
    try:
        ts_float = float(ts)
        # If it looks like milliseconds (13 digits), convert to seconds
        if ts_float > 1e11: 
            ts_float /= 1000
        
        fmt = '%Y-%m-%d %H:%M:%S'
        if ms:
            fmt += '.%f'
            
        return datetime.fromtimestamp(ts_float).strftime(fmt)[:-3] if ms else datetime.fromtimestamp(ts_float).strftime(fmt)
    except Exception as e:
        return f"Error: {e}"

def string_to_timestamp(date_str, ms=False):
    """String to Unix Timestamp"""
    date_obj = dateparser.parse(date_str)
    if date_obj:
        ts = date_obj.timestamp()
        return int(ts * 1000) if ms else int(ts)
    return "Error: Could not parse date string."

def parse_url_details(url):
    """Parse URL into its components, with query params as nested dict"""
    try:
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query, keep_blank_values=True)
        # Convert lists to single values if only one item
        for key, value in query_dict.items():
            if len(value) == 1:
                query_dict[key] = value[0]
        
        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": query_dict,
            "fragment": parsed.fragment,
            "hostname": parsed.hostname,
            "port": parsed.port
        }
    except Exception as e:
        return {"error": str(e)}

def format_jwt_times(payload):
    """Convert exp and iat in JWT payload to readable dates"""
    if not isinstance(payload, dict):
        return payload
    
    new_payload = payload.copy()
    for key in ['exp', 'iat', 'nbf']:
        if key in new_payload and isinstance(new_payload[key], (int, float)):
            new_payload[f"{key}_readable"] = format_timestamp(new_payload[key])
    return new_payload

