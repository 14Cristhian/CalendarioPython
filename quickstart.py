import datetime
import os.path
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_credentials():
    """Get valid user credentials from storage or run the OAuth2 flow if necessary."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials available.")
    return creds

def get_calendar_events(service):
    """Get upcoming calendar events."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = (
        service.events()
        .list(
            calendarId="cristhianmorales0714@gmail.com",
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return events

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar if there are changes."""
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        # Initialize variable to store last events
        last_events = []

        # Continuously get and display upcoming events
        while True:
            events = get_calendar_events(service)
            if not events:
                print("No upcoming events found.")
            else:
                # Check for changes in events
                if events != last_events:
                    print("Changes detected in events:")
                    for event in events:
                        start = event["start"].get("dateTime", event["start"].get("date"))
                        print(start, event.get("summary", "No summary"))
                    last_events = events

            # Wait for the specified interval before checking again
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
