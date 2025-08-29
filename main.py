import re
from datetime import datetime, timedelta
import pytz
import schedule
import time
from calendar_helper import create_event  # Google Calendar integration

# -----------------------
# CONFIGURATION
# -----------------------
TIMEZONE = "Africa/Addis_Ababa"
tz = pytz.timezone(TIMEZONE)

CONTACTS = {
    "john": "realjohn@gmail.com",
    "betelhem": "betelhemyegzaw468@gmail.com",
    "beza": "bezanigusie7@gmail.com",
    "Betelhem": "betelhemyimamd@gmail.com"
}

DEFAULT_DURATION_MINUTES = 30

# -----------------------
# HELPER FUNCTIONS
# -----------------------
def get_target_datetime(day_str, hour, minute=0):
    """
    Returns a timezone-aware datetime for a day string and hour:minute.
    Supports: 'today', 'tomorrow', 'Friday', 'next Tuesday', etc.
    """
    day_str = day_str.lower()
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    now = datetime.now(tz)

    # Today or tomorrow
    if day_str == "today":
        target_date = now
    elif day_str == "tomorrow":
        target_date = now + timedelta(days=1)
    else:
        # Handle "next Tuesday" or "Friday"
        if day_str.startswith("next "):
            weekday_name = day_str.replace("next ", "")
            offset = 7
        else:
            weekday_name = day_str
            offset = 0

        weekday_name = weekday_name.strip()
        if weekday_name not in weekdays:
            return None

        days_ahead = weekdays[weekday_name] - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        days_ahead += offset - 7 if offset else 0
        target_date = now + timedelta(days=days_ahead)

    target_datetime = tz.localize(datetime(
        year=target_date.year,
        month=target_date.month,
        day=target_date.day,
        hour=hour,
        minute=minute
    ))
    return target_datetime

# -----------------------
# COMMAND PARSING
# -----------------------
def parse_command(command):
    """
    Parses a manual command into structured data.
    Supports multiple attendees, flexible time, and optional duration.
    """
    match = re.match(
        r"schedule a meeting with ([\w@.,\s]+) (today|tomorrow|next \w+|\w+) at (\d+)(?::(\d+))?\s*(am|pm)?(?: for (\d+)\s*(minutes?|hours?))?",
        command,
        re.IGNORECASE
    )
    if match:
        attendees_raw = match.group(1).strip()
        day_str = match.group(2).strip()
        hour = int(match.group(3))
        minute = int(match.group(4)) if match.group(4) else 0
        period = match.group(5)
        duration_value = int(match.group(6)) if match.group(6) else None
        duration_unit = match.group(7).lower() if match.group(7) else None

        # Convert to 24-hour
        if period:
            period = period.lower()
            if period == "pm" and hour != 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0

        # Split attendees by comma and strip whitespace
        attendees = [a.strip() for a in attendees_raw.split(",")]

        # Calculate duration in minutes
        if duration_value:
            if "hour" in duration_unit:
                duration_minutes = duration_value * 60
            else:
                duration_minutes = duration_value
        else:
            duration_minutes = DEFAULT_DURATION_MINUTES

        return {
            "intent": "schedule_meeting",
            "attendees": attendees,
            "hour": hour,
            "minute": minute,
            "day_str": day_str,
            "duration_minutes": duration_minutes
        }

    return None

# -----------------------
# SCHEDULING MEETING
# -----------------------
def schedule_meeting(details):
    attendees_list = details.get("attendees", [])
    hour = details.get("hour")
    minute = details.get("minute", 0)
    day_str = details.get("day_str")
    duration_minutes = details.get("duration_minutes", DEFAULT_DURATION_MINUTES)

    if not attendees_list or hour is None or not day_str:
        print("Missing required details for scheduling.")
        return

    # Resolve emails
    resolved_emails = []
    for attendee in attendees_list:
        email = CONTACTS.get(attendee.lower(), attendee)
        resolved_emails.append(email)

    start_dt = get_target_datetime(day_str, hour, minute)
    if start_dt is None:
        print(f"Could not resolve day: '{day_str}'")
        return

    end_dt = start_dt + timedelta(minutes=duration_minutes)
    attendee_str = ", ".join(resolved_emails)

    # Create Google Calendar event
    try:
        created_event = create_event(f"Meeting with {attendee_str}", start_dt, end_dt, resolved_emails)
        print(f"📅 Meeting scheduled with {attendee_str} on {start_dt.strftime('%A %Y-%m-%d %H:%M')}")
        print(f"⏰ Start: {start_dt}, End: {end_dt} (Duration: {duration_minutes} minutes)")
        print(f"🔗 Event link: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f" Failed to create Google Calendar event: {e}")

# -----------------------
# DAILY REMINDERS
# -----------------------
def daily_reminders():
    print("🔔 Daily Reminder: Review your tasks and meetings for today.")

schedule.every().day.at("09:00").do(daily_reminders)

# -----------------------
# COMMAND HANDLER
# -----------------------
def handle_command(command):
    try:
        parsed = parse_command(command)
        if not parsed:
            print("Command parsing failed: Could not understand the input.")
            return

        intent = parsed.get("intent")
        if intent == "schedule_meeting":
            schedule_meeting(parsed)
        else:
            print(f"⚠️ Unknown intent: {intent}")

    except Exception as e:
        print(f" Error during command handling: {e}")

# -----------------------
# MAIN LOOP
# -----------------------
if __name__ == "__main__":
    print("🤖 Executive Assistant is running. Type commands or wait for daily reminders.")
    while True:
        schedule.run_pending()
        try:
            command = input("Enter command (or 'exit' to quit): ").strip()
            if command.lower() == "exit":
                break
            handle_command(command)
        except KeyboardInterrupt:
            print("\nExiting assistant...")
            break
        time.sleep(1)
