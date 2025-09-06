# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

"""

import datetime
import ics

pickup_dates: list[tuple[int, int, int, str]] = ...

HOURS_BEFORE_MIDNIGHT: int = 4
HOURS_AFTER_MIDNIGHT: int = 16
calendar: ics.Calendar = ics.Calendar()
for (year, month, day, description) in pickup_dates:
    event_date: datetime.datetime = datetime.datetime(year, month, day)
    event: ics.Event = ics.Event()
    event.begin: datetime.datetime =\
        event_date - datetime.timedelta(hours=HOURS_BEFORE_MIDNIGHT)
    event.end: datetime.datetime =\
        event_date + datetime.timedelta(hours=HOURS_AFTER_MIDNIGHT)
    event.name: str = description
    calendar.events.add(event)
with open("calendar.ics", mode="w", encoding="utf-8") as my_file:
    my_file.write(calendar.serialize().replace("\n", ""))
