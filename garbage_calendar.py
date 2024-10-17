# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

Create a calendar using ics based on the dates extracting from the PDF file
using pypdf. The process involves reading the document to extract a list of
dates, creating a calendar from that list, and finally, saving the calendar
to a file.
"""
# Standard library
import glob
import datetime
import itertools
import typing
# Third party
import ics
import pypdf


def read_document() -> typing.List[typing.Tuple[int, int, int, str]]:
    """
    Extracts dates and descriptions from a PDF file to a list of dates.

    Parameters
    ----------
    None

    Returns
    -------
    collection_dates : typing.List[typing.Tuple[int, int, int, str]]
        List of tuples containing year, month, day, and description.
    """
    path: str = glob.glob("data/a*9.pdf")[0]
    try:
        reader: pypdf.PdfReader = pypdf.PdfReader(path)
    except FileNotFoundError:
        raise FileNotFoundError("The desired input file was not found")
    except pypdf.errors.PyPdfError:
        raise pypdf.errors.PyPdfError(
            "While reading the PDF file an error occured.")
    front_page: pypdf.PageObject = reader.pages[0]
    # extract text preserving horizontal positioning without excess vertical
    # whitespace (removes blank and "whitespace only" lines)
    lines: str = front_page.extract_text(extraction_mode="layout",
                                         layout_mode_space_vertically=False
                                         ).split("\n")
    date_column_found: bool = False
    collection_dates: typing.List[typing.Tuple[int, int, int, str]] = []
    current_year: int = datetime.datetime.now().year
    spacing: typing.List[int] = [1,    # start of first column
                                 58,   # start of second column
                                 114,  # start of third column
                                 172   # start of fourth column
                                 ]
    all_months: typing.List = []

    for line in lines:
        # Look for the first month to find the beginning of the calender
        if line.strip().startswith("Jan"):
            date_column_found = True
        if not date_column_found:
            continue
        # Stop at the line containing the version because it is below the
        # calender section
        if line.strip().startswith("Ver"):
            break

        # Whenever the months are mentioned, repopulate the parts list
        parts: typing.List[str] = line.strip().split()
        if len(parts) == 4:
            months: typing.List = parts
            all_months.extend(months)
            continue
        # Loop over the line after it has been divided according to the spacing
        for step, text in enumerate([line[a:b].strip()
                                     for a, b
                                     in itertools.pairwise([*spacing, None])]
                                    ):
            if not text:  # Skip empty columns
                continue
            _, day, description = text.strip().split()
            collection_dates.append((current_year,
                                     all_months.index(months[step])+1,
                                     int(day),
                                     description))
    return collection_dates


def make_calendar(pickup_dates: typing.List[typing.Tuple[int, int, int, str]]
                  ) -> ics.Calendar:
    """
    Creates a calendar by adding an event for every provided date with a
    duration.

    Parameters
    ----------
    pickup_dates : typing.List[typing.Tuple[int, int, int, str]]
        typing.List of year, month, day, and description.

    Returns
    -------
    calendar : ics.Calendar
        The resulting calendar.

    """
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
        event.transparent: bool = True
        calendar.events.add(event)
    return calendar


def write_calendar(cal: ics.Calendar) -> None:
    """
    Writes the calendar object to a file.

    Parameters
    ----------
    cal : ics.Calendar
        The created calendar.

    Returns
    -------
    None.

    """
    with open("calendar.ics", mode="w", encoding="utf-8") as my_file:
        timestamp: str = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        clrf: str = "\n"
        for line in cal.serialize_iter():
            line: str = line.strip("\r\n")
            # remove all the new lines characters
            my_file.write(f"{line}{clrf}")
            # write the timestamp of creating the event in the event
            if line.startswith("BEGIN:VE"):
                my_file.write(f"DTSTAMP:{timestamp}{clrf}")


def main() -> None:
    """
    After taking the path from the text file call all the functions in order.

    Returns
    -------
    None.
    """
    dates: typing.List = read_document()
    calendar: ics.Calendar = make_calendar(dates)
    write_calendar(calendar)


if __name__ == "__main__":
    main()
