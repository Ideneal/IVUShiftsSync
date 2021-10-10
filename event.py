from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from utils import remove_control_chars


class EventAdapter:

    def get_events(self, shifts):
        """
        Adapt the IVU client response to the Google Calendar events.
        @param shifts: The shifts given by the IVU client response.
        @return: The list of events.
        """
        events = []

        content = bs(shifts, features='html.parser')
        days = content.findAll('td', {'class': 'day'})

        for day in days:
            duty = day.find('div', {'class': 'duty-nr'})

            if not duty:
                continue

            date = day.find('div', {'class': 'date'}).text
            time_begin = day.find('span', {'class': 'time begin'}).text
            time_end = day.find('span', {'class': 'time end'}).text
            day_after = time_end[-1:] == '+'
            confirmed = day.find('div', {'class': 'confirm'}) is None

            if not confirmed:
                continue

            # Remove symbol + at the end of the string
            if day_after:
                time_end = time_end[:-1]

            start_date_time = datetime.strptime(date + ' ' + time_begin , '%d/%m/%y %H:%M')
            end_date_time = datetime.strptime(date + ' ' + time_end , '%d/%m/%y %H:%M')

            if day_after:
                end_date_time += timedelta(days=1)

            event = {
                'summary': 'Work',
                'description': remove_control_chars(duty.text),
                'start': {'dateTime': start_date_time.isoformat(), 'timeZone': 'Europe/Rome'},
                'end': {'dateTime': end_date_time.isoformat(), 'timeZone': 'Europe/Rome'}
            }
            events.append(event)

        return events
