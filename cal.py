import os.path
from requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class Calendar:

    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)
        self.current_calendar_id = 'primary'

    def get_calendars(self):
        """
        Returns a list of calendars.
        """
        calendars_result = self.service.calendarList().list().execute()
        return calendars_result.get('items', [])

    def switch_calendar(self, name):
        """
        Switch the selected calendar.
        """
        calendars = self.get_calendars()
        if not calendars:
            return

        for calendar in calendars:
            if name == calendar['summary']:
                self.current_calendar_id = calendar['id']
                return

    def get_events(self, datetime, max_result=10):
        """
        Returns a list of last events.
        """
        events_result = self.service.events().list(
            calendarId=self.current_calendar_id,
            timeMin=datetime.isoformat() + 'Z',
            maxResults=max_result,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])

    def create_event(self, event_body):
        """
        Creates an event.
        """
        event_result = self.service.events().insert(
            calendarId=self.current_calendar_id,
            body=event_body
        ).execute()
        return event_result

    def update_event(self, event, event_body):
        """
        Updates an event.
        """
        event_result = self.service.events().update(
            calendarId=self.current_calendar_id,
            eventId=event['id'],
            body=event_body,
        ).execute()
        return event_result

    def delete_event(self, event):
        """
        Deletes an event.
        """
        try:
            self.service.events().delete(
                calendarId=self.current_calendar_id,
                eventId=event['id'],
            ).execute()
        except HttpError:
            print("Failed to delete event")
