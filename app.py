from datetime import datetime
from ivu import IVU
from cal import Calendar
from event import EventAdapter
from config import config
from utils import progress_bar, str2date, str2datetime, add_days, date2datetime


def sync(events, calendar):
    init_date = str2date(events[0]['start']['dateTime']) if len(events) > 0 else datetime.today()
    last_date = str2date(events[-1]['start']['dateTime'])
    current_date = init_date
    days = (last_date - current_date).days

    # Retrieve all existent calendar events
    calendar_events = calendar.get_events(date2datetime(init_date), max_result=max(days, 10))

    # Map events by dates
    mapped_calendar_events = {str2date(event['start']['dateTime']): event for event in calendar_events}
    mapped_events = {str2date(event['start']['dateTime']): event for event in events}

    progress_bar(0, days, prefix='Progress:', suffix='Complete', length=50)

    while current_date < last_date:
        event = mapped_events.get(current_date)
        calendar_event = mapped_calendar_events.get(current_date)

        if event and calendar_event is None:
            calendar.create_event(event)
        
        if event is None and calendar_event:
            calendar.delete_event(calendar_event)
        
        if event and calendar_event:
            calendar.update_event(calendar_event, event)

        current_date = add_days(current_date, 1)
        progress = days - (last_date - current_date).days
        progress_bar(progress, days, prefix='Progress:', suffix='Complete', length=50)


def main():
    # Retrieve shifts
    client = IVU()
    client.login(config['ivu']['username'], config['ivu']['password'])
    shifts = client.shifts()

    # Adapt shifts to events
    adapter = EventAdapter()
    events = adapter.get_events(shifts)

    # Switch calendar
    calendar = Calendar()
    calendar.switch_calendar(config['google']['calendar'])

    # Sync shifts
    sync(events, calendar)
    print('Event synchronized!')


if __name__ == '__main__':
    main()
