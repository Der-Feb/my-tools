from datetime import datetime
import dateparser

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def format_timestamp(ts):
    """Timestamp to readable string"""
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def string_to_timestamp(date_str):
    """String to Unix Timestamp"""
    date_obj = dateparser.parse(date_str)
    if date_obj:
        return int(date_obj.timestamp())
    return "Error: Could not parse date string."

