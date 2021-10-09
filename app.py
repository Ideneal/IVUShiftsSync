import yaml
from datetime import datetime
from ivu import IVU
from cal import Calendar
from event import EventAdapter
from utils import progress_bar


def get_init_date(events):
    now = datetime.utcnow()
    try:
        start_date = datetime.strptime(
            events[0]['start']['dateTime'], '%Y-%m-%dT%H:%M:%S') if len(events) > 0 else now
    except Exception as e:
        start_date = now

    return start_date


def main():
    # Load configs
    with open('config.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Retrieve shifts
    client = IVU()
    client.login(config['ivu']['username'], config['ivu']['password'])
    shifts = client.shifts()

    # Adapt shifts to events
    adapter = EventAdapter()
    events = adapter.get_events(shifts)
    events_length = len(events)

    calendar = Calendar()
    calendar.switch_calendar(config['google']['calendar'])

    # Retrieve all existent calendar events
    calendar_events = {}
    start_date = get_init_date(events).isoformat() + 'Z'  # 'Z' indicates UTC time

    for event in calendar.get_events(start_date, max_result=events_length):
        event_date = event['start']['dateTime'].split('T')[0]
        calendar_events[event_date] = event

    progress_bar(0, events_length, prefix='Progress:', suffix='Complete', length=50)
    # Update the existent events and create the new ones
    for i, event in enumerate(events):
        event_date = event['start']['dateTime'].split('T')[0]
        calendar_event = calendar_events.get(event_date)
        if calendar_event:
            calendar.update_event(calendar_event, event)
        else:
            calendar.create_event(event)
        progress_bar(i+1, events_length, prefix='Progress:', suffix='Complete', length=50)

    print('Event synchronized!')


if __name__ == '__main__':
    main()
