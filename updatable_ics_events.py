"""
author: UnicornOnAzur

A demonstration of the correct and incorrect method of creating an update to an
event.
"""
# Standard library
import typing
# Third party
import ics
# Constants
BEGIN_TIME: str = "20260101T100000Z"
END_TIME: str = "20260101T110000Z"
NEW_END_TIME: str = "20260101T120000Z"
UID: str = "20260101@UnicornOnAzur"


def create_calendar(
        name: str,
        begin_time: str,
        end_time: str,
        uid: typing.Optional[str],
        file_name: str
        ) -> None:
    """
    Create a calendar event and save it to an ICS file.

    Parameters:
        - name : The name of the event.
        - begin_time : The start time of the event in ISO format.
        - end_time : The end time of the event in ISO format.
        - uid : A unique identifier for the event.
        - file_name : The name of the file to save the calendar event.

    Returns:
        None
    """
    clrf: str = "\n"
    calendar = ics.Calendar()
    event = ics.Event(name=name, begin=begin_time, end=end_time, uid=uid)
    calendar.events.add(event)
    with open(file_name, mode="w") as file:
        for line in calendar.serialize_iter():
            file.write(line.replace("\r\n", clrf))
            if line.startswith("DTSTART"):
                file.write(f"METHOD:REQUEST{clrf}")


if __name__ == "__main__":
    create_calendar(
        "Meeting", BEGIN_TIME, END_TIME, UID, "original_meeting.ics")
    create_calendar(
        "Meeting v2", BEGIN_TIME, NEW_END_TIME, None,
        "not_changing_meeting.ics")
    create_calendar(
        "Meeting v3", BEGIN_TIME, NEW_END_TIME, UID, "meeting_changed.ics")
