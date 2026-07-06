import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config.settings import CALENDAR_ID

# --- File Paths ---
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'telegram_credentials.json')
TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'token.json')

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """Authenticates and returns the Google Calendar service."""
    creds = None
    
    # 1. Check if we already have a saved token.json
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    # 2. If there are no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This is the line that opens the browser using your telegram_credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 3. Save the new token.json for the next time the bot runs
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            
    # 4. Build and return the service
    service = build('calendar', 'v3', credentials=creds)
    return service

def check_overlap(start_time, end_time):
    """Checks Google Calendar for existing events in the given timeframe."""
    service = get_calendar_service()
    
    # Notice the + 'Z' has been completely removed from these two lines
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    return len(events) > 0