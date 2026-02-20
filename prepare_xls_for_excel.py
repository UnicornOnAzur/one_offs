# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

A module for saving DataFrames and Styler object to Excel while maintaining
(a large part of) the formatting and styling. There are functions for setting
the column width, text wrapping, the formatting, saving the styling and
finally, combining it all.
"""
# Standard library
import functools
import logging
import typing
# Third party
import pandas as pd
from pandas.io.formats import style
import xlsxwriter
#
from pandas_to_excel_format_string import determine_format_string
# Constants
FOLDER: str = "output/"
SHEET_NAME: str = "This sheet"
WRITER_ENGINE: str = "xlsxwriter"
MAX_COLUMN_WIDTH_PIXELS: int = 300
logger: logging.Logger = logging.getLogger(__name__)


def _set_column_width_string_length(dataframe: pd.DataFrame):
    """
    Sets the width of columns in an Excel sheet based on the maximum length of
    the data in each column.

    Parameters:
        dataframe : The DataFrame whose column widths are to be set.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_column_width_1.xlsx",
                        engine=WRITER_ENGINE) as writer:
        dataframe.to_excel(
            excel_writer=writer, sheet_name=SHEET_NAME, index=False)
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]

        for idx, column_name in enumerate(dataframe.keys()):
            series: pd.Series = dataframe[column_name]
            max_length: int = max((
                # Length of the largest item
                series.fillna("").astype(str).map(len).max(),
                # Length of the column name/header
                len(str(series.name))
                ))
            result: int = worksheet.set_column(idx, idx, max_length)
            logger.debug((
                f"{column_name[:10].ljust(10, ' ')} {max_length} successfull:"
                f" {result == 0}"))
        else:
            logger.info("All columns widths are set successfully")
    logger.info("File saved successfully")


def _set_column_width_cell_autofit_width(dataframe: pd.DataFrame):
    """
    Sets the width of columns in an Excel sheet based on the maximum length of
    the data in each column using cell_autofit_width.

    Parameters:
        dataframe : The DataFrame whose column widths are to be set.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_column_width_2.xlsx",
                        engine=WRITER_ENGINE) as writer:
        dataframe.to_excel(
            excel_writer=writer, sheet_name=SHEET_NAME, index=False)
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]

        for idx, column_name in enumerate(dataframe.keys()):
            series: pd.Series = dataframe[column_name]
            column_width: int = functools.reduce(
                max,
                map(xlsxwriter.utility.cell_autofit_width,
                    [column_name] + series.fillna("").astype(str).to_list()))
            result: int = worksheet.set_column_pixels(idx, idx, column_width)
            logger.debug((
                f"{column_name[:10].ljust(10, ' ')} {column_width} "
                f"successfull: {result == 0}"))
        else:
            logger.info("All columns widths are set successfully")
    logger.info("File saved successfully")


def _set_column_width_with_autofit(dataframe: pd.DataFrame):
    """
    Sets the width of columns in an Excel sheet using autofit.

    Parameters:
        dataframe : The DataFrame whose column widths are to be set.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_column_width_3.xlsx",
                        engine=WRITER_ENGINE) as writer:
        dataframe.to_excel(
            excel_writer=writer, sheet_name=SHEET_NAME, index=False)
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]
        worksheet.autofit()
        logger.info("Successfully autofitted the column widths")
    logger.info("File saved successfully")


def set_column_width(dataframe: pd.DataFrame) -> None:
    """
    Set the column widths for the given DataFrame.

    Parameters:
        dataframe : The DataFrame to write to Excel.

    Returns:
        None
    """
    _set_column_width_string_length(dataframe)
    _set_column_width_cell_autofit_width(dataframe)
    _set_column_width_with_autofit(dataframe)
    logger.info("All column width options are done.")


def _set_textwrap_keyword_argument(dataframe: pd.DataFrame) -> None:
    """
    Writes a DataFrame to an Excel file with text wrapping enabled for each
    column using a keyword argument.

    Parameters:
        dataframe : The DataFrame to be written to Excel.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_textwrap_1.xlsx",
                        engine=WRITER_ENGINE) as writer:
        dataframe.to_excel(
            excel_writer=writer, sheet_name=SHEET_NAME, index=False)
        workbook: xlsxwriter.workbook.Workbook = writer.book
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]

        for idx, _ in enumerate(dataframe.keys()):
            format: xlsxwriter.format.Format = workbook.add_format(
                {"text_wrap": True})
            worksheet.set_column_pixels(idx, idx, None, format)
        else:
            logger.info("All columns widths are set successfully")
    logger.info("File saved successfully")


def _set_textwrap_with_method(dataframe: pd.DataFrame) -> None:
    """
    Writes a DataFrame to an Excel file with text wrapping enabled for each
    column using the method.

    Parameters:
        dataframe : The DataFrame to be written to Excel.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_textwrap_2.xlsx",
                        engine=WRITER_ENGINE) as writer:
        dataframe.to_excel(
            excel_writer=writer, sheet_name=SHEET_NAME, index=False)
        workbook: xlsxwriter.workbook.Workbook = writer.book
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]

        for idx, _ in enumerate(dataframe.keys()):
            format: xlsxwriter.format.Format = workbook.add_format()
            format.set_text_wrap()
            worksheet.set_column_pixels(idx, idx, None, format)
        else:
            logger.info("All columns widths are set successfully")
    logger.info("File saved successfully")


def set_textwrap(dataframe: pd.DataFrame) -> None:
    """
    Set text wrapping for the given DataFrame.

    Parameters:
        dataframe : The DataFrame to write to Excel.

    Returns:
        None
    """
    _set_textwrap_keyword_argument(dataframe)
    _set_textwrap_with_method(dataframe)
    logger.info("All text wrap options are done.")


def set_column_datatype(dataframe: pd.DataFrame) -> None:
    """
    Sets the data type formatting for each column in the provided DataFrame
    and saves it to an Excel file.

    Parameters:
        dataframe : The DataFrame containing the data to be formatted.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_set_datatype.xlsx",
                        engine=WRITER_ENGINE) as writer:
        dataframe.to_excel(
            excel_writer=writer, sheet_name=SHEET_NAME, index=False)
        workbook: xlsxwriter.workbook.Workbook = writer.book
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]

        for idx, column_name in enumerate(dataframe.keys()):
            series: pd.Series = dataframe[column_name]
            format: xlsxwriter.format.Format = workbook.add_format()
            format_string = determine_format_string(series)
            format.set_num_format(format_string)
            result: int = worksheet.set_column_pixels(idx, idx, None, format)
            logger.debug(f"{column_name}: {format_string} {result}")
        logger.debug("\n".join([f"{k} {v}" for k, v
                                in worksheet.col_info.items()]))
    logger.info("File saved successfully with formatting")


def save_styling(styler: style.Styler) -> None:
    """
    Save a styled DataFrame to an Excel file with custom formatting.

    Parameters:
        styler : A pandas Styler object containing the DataFrame styling.

    Returns:
        None
    """
    with pd.ExcelWriter(f"{FOLDER}/pd_styled.xlsx",
                        engine=WRITER_ENGINE) as writer:
        styler.to_excel(excel_writer=writer,
                        sheet_name=SHEET_NAME,
                        header=False,
                        index=False,
                        startrow=1
                        )
        workbook: xlsxwriter.workbook.Workbook = writer.book
        worksheet: xlsxwriter.worksheet.Worksheet = writer.sheets[SHEET_NAME]
        # Initialize formatting as an empty dictionary if no table styles are
        # defined. Then extract the last property from the created list. If
        # the list is empty, it defaults to [[]].
        formatting: typing.Dict[str, str] = (
            {} if not styler.table_styles else dict(
                functools.reduce(
                    list.pop, [s["props"] for s in styler.table_styles
                               if s["selector"] == "th.col_heading"] or [[]])))
        logger.debug(f"{formatting=}")
        header_format: xlsxwriter.format.Format = workbook.add_format({
            "bg_color": formatting.get("background-color", "#FFFFFF"),
            "font_color": formatting.get("color", "black")
        })
        logger.debug(f"{header_format=}")
        for idx, value in enumerate(styler.columns.values):
            logger.debug(f"Writing header for column {idx} {value}")
            worksheet.write(0, idx, value, header_format)
        logger.info("File saved successfully with styling")


def save_combined_formatting(
        dataframe: typing.Union[pd.DataFrame, style.Styler]) -> None:
    """
    Saves a DataFrame or Styler to an Excel file with combined formatting.

    Parameters:
        dataframe : The DataFrame or Styler object to save.

    Returns:
        None
    """
    def apply_formatting(
        formatting: typing.Optional[typing.Dict[str, str]] = None
            ) -> None:
        """
        Applies formatting to the Excel worksheet based on the provided
        formatting dictionary.

        Parameters:
            formatting : An optional dictionary containing formatting options.

        Returns:
            None
        """
        if formatting is not None:
            header_format: xlsxwriter.format.Format = workbook.add_format({
                "bg_color": formatting.get("background-color", "#FFFFFF"),
                "font_color": formatting.get("color", "black")
            })
            logger.debug(f"{header_format=}")
        for idx, column_name in enumerate(dataframe.columns):
            if formatting is not None:
                worksheet.write(0, idx, column_name, header_format)
            series: pd.Series = dataframe[column_name]
            format: xlsxwriter.format.Format = workbook.add_format()
            column_width: int = min(
                MAX_COLUMN_WIDTH_PIXELS,
                column_width_needed := functools.reduce(
                    max,
                    map(xlsxwriter.utility.cell_autofit_width,
                        [column_name] + series.fillna("").astype(str).to_list()
                        )))
            if column_width_needed >= MAX_COLUMN_WIDTH_PIXELS:
                format.set_text_wrap(True)
                logger.debug(f"Setting text wrap for column {idx} {format}")
            result: int = worksheet.set_column_pixels(
                idx, idx, column_width, format)
            logger.debug((
                f"{column_name[:10].ljust(10, ' ')} "
                f"{column_width} successfull: {result == 0}"))

    match dataframe:
        case pd.DataFrame():
            logger.debug("A Dataframe was provided")
            with pd.ExcelWriter(f"{FOLDER}/pd_combined_dataframe.xlsx",
                                engine=WRITER_ENGINE) as writer:
                dataframe.to_excel(
                    excel_writer=writer, sheet_name=SHEET_NAME, index=False)
                workbook: xlsxwriter.workbook.Workbook = writer.book
                worksheet: xlsxwriter.worksheet.Worksheet =\
                    writer.sheets[SHEET_NAME]
                apply_formatting()
        case style.Styler():
            logger.debug("A Styler was provided")
            with pd.ExcelWriter(f"{FOLDER}/pd_combined_styler.xlsx",
                                engine=WRITER_ENGINE) as writer:
                dataframe.to_excel(
                    excel_writer=writer,
                    sheet_name=SHEET_NAME,
                    header=False,
                    index=False,
                    startrow=1)
                workbook: xlsxwriter.workbook.Workbook = writer.book
                worksheet: xlsxwriter.worksheet.Worksheet =\
                    writer.sheets[SHEET_NAME]
                formatting: typing.Dict[str, str] = (
                    {} if not dataframe.table_styles else dict(
                        functools.reduce(
                            list.pop,
                            [s["props"] for s in dataframe.table_styles
                             if s["selector"] == "th.col_heading"] or [[]])))
                logger.debug(f"{formatting=}")
                dataframe = dataframe.data
                apply_formatting(formatting)
    logger.info(
        "The DataFrame or Styler object was successfully formatted and saved.")


def demo():
    """
    This function imports a demo DataFrame and applies various formatting and
    styling functions to it. It sets the column width, applies text wrapping,
    sets the column data types, and saves the styled DataFrame.
    """
    from data.demo_dataframe import df, df_styled
    # Apply formatting and styling to the DataFrame
    set_column_width(df)
    set_textwrap(df)
    set_column_datatype(df)
    save_styling(df_styled)
    save_combined_formatting(df)
    save_combined_formatting(df_styled)


if __name__ == "__main__":
    logging.basicConfig(
        filename='log.log', filemode="w",
        format="%(levelname)-8s|%(funcName)-20s|%(lineno)3d| %(message)s",
        level=logging.DEBUG, encoding="utf-8")
    logging.getLogger("faker").setLevel(logging.WARNING)
    logging.getLogger("pandas").setLevel(logging.WARNING)
    logger.info(f"Pandas version: {pd.__version__}")
    demo()
