#!/usr/bin/python

import os
import sys
import argparse
import yaml
import datetime
import caldav

# The tzlocal module reads local timezone information from /etc/localtime.
# https://github.com/regebro/tzlocal
import tzlocal
localtime = tzlocal.get_localzone()

cfg = {}
default_config_file = os.path.join(os.environ['HOME'],
                                   '.config', 'icsremind.yaml')


class ConfigurationError(Exception):
    pass


def process_event(event, cal_props):
    print '#', event.uid.value

    dtstart = event.dtstart.value
    dtend   = event.dtend.value
    spec    = []

    if isinstance(dtstart, datetime.datetime):
        # Convert times to local timezone.
        dtstart = dtstart.astimezone(localtime)
        dtend   = dtend.astimezone(localtime)

        spec.append(dtstart.strftime('%Y-%m-%d AT %H:%M'))
        duration = dtend - dtstart
        spec.append('DURATION %s' % ':'.join(str(duration).split(':')[:2]))
    elif isinstance(dtstart, datetime.date):
        spec.append(dtstart.strftime('%Y-%m-%d'))
        spec.append('THROUGH %s' % (dtend.strftime('%Y-%m-%d')))

    if cal_props and 'priority' in cal_props:
        spec.append('PRIORITY %s' % cal_props['priority'])

    spec = ' '.join(spec)

    print spec, 'MSG', event.summary.value


def process_calendar(cal, from_date, to_date):
    cal_props = cfg['calendars'].get(str(cal.url))

    print '#', cal.url

    events = cal.date_search(from_date, to_date)
    for event in events:
        event = event.get_instance().vevent
        process_event(event, cal_props)


def parse_args():
    p  = argparse.ArgumentParser()
    p.add_argument('--config', '-f',
                   default=default_config_file)
    p.add_argument('--days', '-d',
                   default=7,
                   type=int)
    p.add_argument('--output', '-o')

    return p.parse_args()


def main():
    global cfg

    args = parse_args()
    with open(args.config) as fd:
        cfg = yaml.load(fd).get('icsremind', {})

    if not 'url' in cfg:
        raise ConfigurationError('missing url')

    client = caldav.DAVClient(cfg['url'],
                              username=cfg.get('username'),
                              password=cfg.get('password'))

    principal = caldav.Principal(client)

    # Point sys.stdout at a file if --output option was used.
    sys.stdout = open(args.output, 'w') if args.output else sys.stdout

    # We look for reminders between now and now+days.
    now  = datetime.datetime.now()
    days = datetime.timedelta(args.days)
    then = now + days

    for cal in principal.calendars():
        # If the configuration file has an explicit list of calendars
        # check the current calendar url against the list.  If there is no
        # explicit list of calendars, we process all of them.
        if cfg.get('calendars') and not str(cal.url) in cfg['calendars']:
            continue

        process_calendar(cal, now, then)

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except ConfigurationError as detail:
        print >>sys.stderr, 'configuration error:', detail
        sys.exit(2)

