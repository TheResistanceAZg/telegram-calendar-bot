import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CALENDAR_ID = os.getenv('CALENDAR_ID', 'primary')