# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

Create a calendar using ics based on the dates extracted from a PDF file using
pypdf. The process involves reading the document to extract a list of dates,
creating a calendar from that list, and finally, writing the calendar to a
file.
"""
# Standard library
import collections
import glob
import datetime
import itertools
import re
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
    collection_dates : List of tuples containing year, month, day, and
    description.
    """
    path: str = glob.glob(r"data/a*[0-9].pdf")[0]
    try:
        reader: pypdf.PdfReader = pypdf.PdfReader(path)
    except FileNotFoundError:
        raise FileNotFoundError("The desired input file was not found")
    except pypdf.errors.PyPdfError:
        raise pypdf.errors.PyPdfError(
            "An error occurred while reading the PDF file.")
    front_page: pypdf.PageObject = reader.pages[0]
    # Extract text preserving horizontal positioning without excess vertical
    # whitespace (removes blank and "whitespace only" lines)
    lines: str = front_page.extract_text(extraction_mode="layout",
                                         layout_mode_space_vertically=True
                                         ).split("\n")
    date_column_found: bool = False
    collection_dates: typing.List[typing.Tuple[int, int, int, str]] = []
    current_year: int = int(lines[0].strip())
    all_months: typing.List = []

    spacing = _determine_spacing(lines)

    for line in lines:
        # Look for the first month to find the beginning of the calender
        if line.strip().startswith("Jan"):
            date_column_found = True
        # If the table doesn't start in this line go to the next line
        if not date_column_found:
            continue
        # Stop at the line containing the version because it is below the
        # calender section
        if line.strip().startswith("Ver"):
            break

        # Whenever the months are mentioned, repopulate the parts list
        parts: typing.List[str] = line.strip().split()
        if len(parts) == 4:
            all_months.extend((months := parts))
            continue

        # Loop over the line after it has been divided according to the spacing
        # to extract the dates and descriptions
        for step, text in enumerate([line[a:b].strip()
                                     for a, b
                                     in itertools.pairwise([*spacing, None])]
                                    ):
            if not text:  # Skip empty columns
                continue
            _, day, *_, description = text.strip().split()
            collection_dates.append((current_year,
                                     all_months.index(months[step])+1,
                                     int(day),
                                     description))
    return collection_dates


def _determine_spacing(lines: typing.List[str]) -> typing.List[int]:
    """
    Determine the starting positions of the four most common words (with three
    or more lowercase letters) in a list of lines, which will be the starting
    word of the columns.

    Parameters
    ----------
        lines: A list of strings, where each string represents a
        line of text.

    Returns
    -------
        spacing : A sorted list of the starting positions of the four most
        common words.
    """
    matches: collections.Counter = collections.Counter([
                            match.start()
                            for line in lines
                            for match in re.finditer(r"\b[a-z]{3,}\b", line)])
    spacing: list[int] = sorted([val[0] for val in matches.most_common(4)])
    return spacing


def make_calendar(pickup_dates: typing.List[typing.Tuple[int, int, int, str]]
                  ) -> ics.Calendar:
    """
    Creates a calendar by adding an event for every provided date with a
    duration.

    Parameters
    ----------
    pickup_dates : list of year, month, day, and description.

    Returns
    -------
    calendar : The resulting calendar.
    """
    HOURS_BEFORE_MIDNIGHT: int = 4
    HOURS_AFTER_MIDNIGHT: int = 16
    calendar: ics.Calendar = ics.Calendar()
    for (year, month, day, description) in pickup_dates:
        event_date: datetime.datetime = datetime.datetime(year, month, day)
        event: ics.Event = ics.Event()
        event.begin = event_date -\
            datetime.timedelta(hours=HOURS_BEFORE_MIDNIGHT)
        event.end = event_date +\
            datetime.timedelta(hours=HOURS_AFTER_MIDNIGHT)
        event.name = description
        calendar.events.add(event)
    return calendar


def write_calendar(calendar: ics.Calendar) -> None:
    """
    Writes the calendar object to a file.

    Parameters
    ----------
    calendar : The created calendar.

    Returns
    -------
    None.
    """
    with open("calendar.ics", mode="w", encoding="utf-8") as file:
        timestamp: str = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        crlf: str = "\n"
        for line in calendar.serialize_iter():
            # Replace the current CRLF sequence with a new one
            file.write(line.replace("\r\n", crlf))
            # Write the timestamp of creating the event in the event
            if line.startswith("BEGIN:VEVENT"):
                file.write(f"DTSTAMP:{timestamp}{crlf}")


def main() -> None:
    """
    Executes the main workflow of reading the document, creating the calendar,
    and writing it to a file.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    dates: typing.List[typing.Tuple[int, int, int, str]] = read_document()
    calendar: ics.Calendar = make_calendar(dates)
    write_calendar(calendar)


if __name__ == "__main__":
    main()
