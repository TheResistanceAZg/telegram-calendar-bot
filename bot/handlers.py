from telegram import Update
from telegram.ext import ContextTypes
from services.google_calendar import check_overlap, create_event
from utils.date_helpers import extract_date_from_text, get_end_time

async def check_availability(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Listens to regular messages, looks for questions and dates, and replies."""
    text = update.message.text
    
    # 1. Only process messages that are questions
    if not text or "?" not in text:
        return

    # 2. Try to extract a date from the sentence
    parsed_date = extract_date_from_text(text)
    
    # If no date was found in the text, quietly ignore it and do nothing
    if not parsed_date:
        return

    # 3. Assume a 1-hour event block
    end_date = get_end_time(parsed_date)

    # 4. Check for overlap using services
    has_conflict = check_overlap(parsed_date, end_date)

    # 5. Respond directly to the chat
    if has_conflict:
        await update.message.reply_text("probably no")
    else:
    # We are free! Let's add it to the calendar.
        create_event(parsed_date, end_date, event_name="Tentative Plans")
        await update.message.reply_text("probably yes, I just blocked it off on my calendar!")