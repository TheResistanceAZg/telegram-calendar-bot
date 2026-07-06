from dateparser.search import search_dates
import datetime

def extract_date_from_text(text):
    """Searches a full sentence for a date/time and returns a timezone-aware datetime object."""
    matches = search_dates(text, settings={
        'PREFER_DATES_FROM': 'future',
        'TIMEZONE': 'America/Chicago',
        'RETURN_AS_TIMEZONE_AWARE': True
    })
    
    if matches:
        return matches[0][1]
        
    return None

def get_end_time(start_time, hours=1):
    """Returns an end time based on the expected duration."""
    return start_time + datetime.timedelta(hours=hours)