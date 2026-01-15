# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

Create a calendar using ics based on the dates extracted from a PDF file using
pypdf. The process involves reading the document to extract a list of dates,
creating a calendar from that list, and finally, writing the calendar to a
file.
"""
# Standard library
import argparse
import collections
import glob
import datetime
import itertools
import logging
import os
import re
import typing
# Third party
import ics
import pypdf
# Constants
HOURS_BEFORE_MIDNIGHT: int = 4
HOURS_AFTER_MIDNIGHT: int = 16
CRLF: str = "\n"
FILENAME: str = "calendar.ics"


class InvalidInputError(Exception):
    """Raised when user input is invalid"""
    pass


def verified_path(path: str) -> str:
    """
    Verifies if the given path is a valid directory.

    Parameters:
        path : The path to be verified.

    Returns:
        The valid directory path.

    Raises:
        argparse.ArgumentTypeError: If the path is not a valid directory.
    """
    if os.path.isfile(os.path.join(os.getcwd(), path)):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"{path} is not a valid path")


def take_cli_input() -> str:
    """
    Takes command line input for the file path.

    Parameters:
        None

    Returns:
        The file path provided by the user.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="Garbage Calendar")  # TODO: elaborate
    parser.add_argument("-p", "--path", type=verified_path, required=True,
                        help="The path to the input file to process.")
    args: argparse.Namespace = parser.parse_args()
    logger.debug(f"The provided path is: {args.path}")
    return args.path


def _determine_spacing(lines: typing.List[str]) -> typing.List[int]:
    """
    Determine the starting positions of the four most common words (with two
    or more lowercase letters before a digit) in a list of lines, which will
    be the starting word of the columns.

    Parameters:
        lines: A list of strings, where each string represents a line of text.

    Returns:
        spacing : A sorted list of the starting positions of the four most
        common words.
    """
    matches: collections.Counter = collections.Counter([
        match.start() for line in lines
        for match in re.finditer(r"\b[a-z]{2,}\b\s+\d", line)])
    spacing: typing.List[int] = sorted([val[0]
                                        for val in matches.most_common(4)])
    logger.debug(f"Determined spacing: {spacing}")
    return spacing


def read_document(path) -> typing.List[typing.Tuple[int, int, int, str]]:
    """
    Extracts dates and descriptions from a PDF file to a list of dates.

    Parameters:
        path : The path to the PDF file.

    Returns:
        collection_dates : List of tuples containing year, month, day, and
        description.

    Raises:
        FileNotFoundError: If the PDF file is not found.
        pypdf.errors.PyPdfError: If an error occurs while reading the PDF file.
        ValueError: If the PDF does not contain valid dates.
    """
    try:
        reader: pypdf.PdfReader = pypdf.PdfReader(path)
        logger.debug(f"{reader.get_num_pages()} page was loaded.")
    except FileNotFoundError:
        raise FileNotFoundError("The desired input file was not found")
    except pypdf.errors.PyPdfError:
        raise pypdf.errors.PyPdfError(
            "An error occurred while reading the PDF file.")
    front_page: pypdf.PageObject = reader.pages[0]
    # Extract text preserving horizontal positioning without excess vertical
    # whitespace (removes blank and "whitespace only" lines)
    text: str = front_page.extract_text(extraction_mode="layout",
                                        layout_mode_space_vertically=True
                                        )
    if not text.strip():
        raise ValueError(
            "The PDF file is empty or does not contain valid text.")
    year: int = int(re.findall(r"\d{4}", text)[0])
    logger.debug(f"The extracted year is: {year}.")
    lines: typing.List[str] = text.split("\n")
    date_column_found: bool = False
    collection_dates: typing.List[typing.Tuple[int, int, int, str]] = []
    all_months: typing.List[str] = []

    for index, line in enumerate(lines):
        # Look for the first month to find the beginning of the calender
        if line.strip().lower().startswith("jan"):
            date_column_found = True
            logger.debug(f"Date column found on line {index}")
            spacing = _determine_spacing(lines[index:])
        # If the table doesn't start in this line go to the next line
        if not date_column_found:
            continue
        # Stop at the line containing the version because it is below the
        # calender section
        if line.strip().lower().startswith("ver"):
            logger.debug(f"End found on line {index}: {line}")
            break
        # Skip empty lines
        if not line:
            continue

        # Whenever the months are mentioned, repopulate the parts list
        parts: typing.List[str] = line.strip().split()
        if len(parts) == 4:
            all_months.extend((months := parts))
            continue

        logger.debug(f"Processing line {index}: {line}")
        # Loop over the line after it has been divided according to the spacing
        # to extract the dates and descriptions
        for step, text in enumerate([line[begin:end].strip() for begin, end
                                     in itertools.pairwise([*spacing, None])]
                                    ):
            if not text:  # Skip empty columns
                continue
            logger.debug(f"Extracted text from line {index}: {text}")
            try:
                _, day, description = text.strip().split()
            except ValueError as exc:
                if str(exc) == (
                        "not enough values to unpack (expected 3, got 1)"):
                    description = text.strip().split()[0]
                else:
                    continue
            logger.debug((f"Extracted information from line {index}:"
                          f" {year} {step} {day} {description}"))
            collection_dates.append((year,
                                     all_months.index(months[step])+1,
                                     int(day),
                                     description))
    if not collection_dates:
        raise ValueError("No valid dates found in the PDF file.")
    logger.info(f"Number of dates gathered: {len(collection_dates)}.")
    return collection_dates


def make_calendar(pickup_dates: typing.List[typing.Tuple[int, int, int, str]]
                  ) -> ics.Calendar:
    """
    Creates a calendar by adding an event for every provided date with a
    duration.

    Parameters:
        pickup_dates : list of year, month, day, and description.

    Returns:
        calendar : The resulting calendar.
    """
    calendar: ics.Calendar = ics.Calendar()
    # For every date add an event to the calendar
    for (year, month, day, description) in pickup_dates:
        event_date: datetime.datetime = datetime.datetime(year, month, day)
        event: ics.Event = ics.Event()
        event.begin = event_date -\
            datetime.timedelta(hours=HOURS_BEFORE_MIDNIGHT)
        event.end = event_date +\
            datetime.timedelta(hours=HOURS_AFTER_MIDNIGHT)
        event.name = description
        calendar.events.add(event)
    else:
        logger.info(f"Calendar created with {len(calendar.events)} events.")
    return calendar


def write_calendar(calendar: ics.Calendar) -> None:
    """
    Writes the calendar object to a file.

    Parameters:
        calendar : The created calendar.

    Returns:
        None.
    """
    with open(FILENAME, mode="w", encoding="utf-8") as file:
        timestamp: str = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        for line in calendar.serialize_iter():
            # Replace the current CRLF sequence with a new one
            file.write(line.replace("\r\n", CRLF))
            # Write the timestamp of creating the event in the event
            if line.startswith("BEGIN:VEVENT"):
                file.write(f"DTSTAMP:{timestamp}{CRLF}")
        else:
            logger.info("All events were written to the file.")
    if glob.glob(FILENAME):  # Verify if the file is created
        logger.info("File was created successfully.")


def main() -> None:
    """
    Executes the main workflow of taking in the CLI argument, reading the
    document, creating the calendar, and writing it to a file.

    Parameters:
        None

    Returns:
        None
    """
    # TODO: remark
    path = take_cli_input()
    # TODO: remark
    dates: typing.List[typing.Tuple[int, int, int, str]] = read_document(path)
    calendar: ics.Calendar = make_calendar(dates)
    write_calendar(calendar)


if __name__ == "__main__":
    """
    """
    logger: logging.Logger = logging.getLogger(__name__,)
    logging.basicConfig(
        filename='log.log', filemode="w", level=logging.DEBUG,
        format="%(funcName)s %(lineno)d | %(message)s")
    main()
